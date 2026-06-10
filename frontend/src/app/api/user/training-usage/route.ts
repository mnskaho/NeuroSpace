import { NextRequest, NextResponse } from 'next/server';

import { supabaseAdmin } from '@/lib/supabase/admin';

export const runtime = 'nodejs';

type NormalizedPlan = 'free' | 'pro' | 'pro_plus';

const PLAN_LIMITS: Record<NormalizedPlan, number> = {
  free: 1,
  pro: 5,
  pro_plus: 25,
};

function normalizePlan(value: unknown): NormalizedPlan {
  const plan = String(value || 'free')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '_');

  if (plan === 'pro+' || plan === 'pro_plus' || plan === 'pro-plus') return 'pro_plus';
  if (plan === 'pro') return 'pro';
  return 'free';
}

async function getCurrentUser(req: NextRequest) {
  const authHeader = req.headers.get('authorization') || '';
  const token = authHeader.toLowerCase().startsWith('bearer ')
    ? authHeader.slice(7).trim()
    : '';

  if (!token) return null;

  const { data, error } = await supabaseAdmin.auth.getUser(token);
  if (error || !data.user?.id) return null;
  return data.user;
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

export async function GET(req: NextRequest) {
  try {
    const user = await getCurrentUser(req);

    if (!user) {
      return NextResponse.json({ error: 'Authentication required' }, { status: 401 });
    }

    const plan = await getLatestPlan(user.id);
    const limit = PLAN_LIMITS[plan];
    const used = await getMonthlyCompletedCount(user.id);

    return NextResponse.json({
      plan,
      used,
      limit,
    });
  } catch (error) {
    console.error('Training usage error:', error);
    return NextResponse.json({ error: 'Failed to load training usage' }, { status: 500 });
  }
}
