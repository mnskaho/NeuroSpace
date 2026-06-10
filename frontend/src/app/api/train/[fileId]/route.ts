import { NextRequest, NextResponse } from 'next/server';

import { createTrainingJob } from '@/lib/jobs/trainingJobs';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const runtime = 'nodejs';

const UNKNOWN_DATASET_NAME = 'Unknown Dataset';
const PLAN_LIMITS = {
  free: 1,
  pro: 5,
  pro_plus: 25,
} as const;

type NormalizedPlan = keyof typeof PLAN_LIMITS;

function cleanDatasetName(value: unknown) {
  if (typeof value !== 'string') return UNKNOWN_DATASET_NAME;
  const name = value.replace(/\\/g, '/').split('/').pop()?.trim();
  return name || UNKNOWN_DATASET_NAME;
}

function getDatasetName(body: Record<string, unknown>) {
  const datasetInfo =
    body.dataset_info && typeof body.dataset_info === 'object' && !Array.isArray(body.dataset_info)
      ? (body.dataset_info as Record<string, unknown>)
      : {};

  return cleanDatasetName(
    body.dataset_name ||
      datasetInfo.dataset_name ||
      body.filename ||
      datasetInfo.filename ||
      datasetInfo.name
  );
}

function normalizePlan(value: unknown): NormalizedPlan {
  const plan = String(value || 'free')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '_');

  if (plan === 'pro+' || plan === 'pro_plus' || plan === 'pro-plus') return 'pro_plus';
  if (plan === 'pro') return 'pro';
  return 'free';
}

function currentMonthRange() {
  const now = new Date();
  const start = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), 1));
  const end = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1));

  return {
    startIso: start.toISOString(),
    endIso: end.toISOString(),
  };
}

async function getLatestPlan(userId: string) {
  const { data, error } = await supabaseAdmin
    .from('payments')
    .select('plan')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
    .limit(1)
    .maybeSingle();

  if (error || !data?.plan) return 'free' as const;
  return normalizePlan(data.plan);
}

async function countCompletedTrainings(userId: string, dateColumn: string) {
  const { startIso, endIso } = currentMonthRange();
  const { count, error } = await supabaseAdmin
    .from('training_jobs')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId)
    .eq('status', 'completed')
    .gte(dateColumn, startIso)
    .lt(dateColumn, endIso);

  if (error) throw error;
  return count || 0;
}

async function getMonthlyCompletedCount(userId: string) {
  for (const dateColumn of ['completed_at', 'updated_at', 'created_at']) {
    try {
      return await countCompletedTrainings(userId, dateColumn);
    } catch {
      continue;
    }
  }

  return 0;
}

async function getCurrentUser(req: NextRequest) {
  const authHeader = req.headers.get('authorization') || '';
  const token = authHeader.toLowerCase().startsWith('bearer ')
    ? authHeader.slice(7).trim()
    : '';

  if (!token) return null;

  const { data, error } = await supabaseAdmin.auth.getUser(token);
  if (error || !data.user?.id || !data.user.email) return null;
  return data.user;
}

export async function POST(req: NextRequest, { params }: { params: Promise<{ fileId: string }> }) {
  try {
    const { fileId } = await params;
    const body = await req.json();
    const user = await getCurrentUser(req);

    if (!user?.id || !user.email) {
      return NextResponse.json({ error: 'Authentication required' }, { status: 401 });
    }

    const plan = await getLatestPlan(user.id);
    const limit = PLAN_LIMITS[plan];
    const used = await getMonthlyCompletedCount(user.id);

    if (Math.min(used, limit) >= limit) {
      return NextResponse.json(
        { error: 'Monthly training limit reached. Please upgrade your plan.', plan, used, limit },
        { status: 403 }
      );
    }

    const datasetName = getDatasetName(body);
    const datasetInfo = {
      ...(body.dataset_info && typeof body.dataset_info === 'object' ? body.dataset_info : {}),
      dataset_name: datasetName,
    };
    const config = body.config || body;
    const userName = user.user_metadata?.full_name || user.user_metadata?.name || null;

    const job = await createTrainingJob({
      file_id: fileId,
      user_id: user.id,
      user_email: user.email,
      user_name: userName,
      status: 'queued',
      dataset_name: datasetName,
      config,
      dataset_info: datasetInfo,
    });

    console.log('Job created');
    console.log('file_id', fileId);
    console.log('user_id', user.id);
    console.log('user_email', user.email);

    return NextResponse.json({
      success: true,
      job_id: fileId,
      file_id: fileId,
      dataset_name: datasetName,
      status: job.status,
    });
  } catch (error) {
    console.error('Create training job error:', error);
    const detail = error instanceof Error ? error.message : 'Unknown create training job error';
    return NextResponse.json({ error: 'Failed to create training job', detail }, { status: 500 });
  }
}
