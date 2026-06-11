import { NextRequest, NextResponse } from 'next/server';

import { findJobByFileId, updateJobByFileId } from '@/lib/jobs/trainingJobs';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const runtime = 'nodejs';

const CANCELLABLE_STATUSES = new Set(['queued', 'processing']);

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

export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ fileId: string }> }
) {
  try {
    const { fileId } = await params;
    const user = await getCurrentUser(req);

    if (!user?.id) {
      return NextResponse.json({ error: 'Authentication required' }, { status: 401 });
    }

    const job = await findJobByFileId(fileId);

    if (!job) {
      return NextResponse.json({ error: 'Job not found' }, { status: 404 });
    }

    if (job.user_id !== user.id) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    if (!CANCELLABLE_STATUSES.has(job.status)) {
      return NextResponse.json(
        {
          error: `Cannot cancel job with status: ${job.status}`,
          status: job.status,
        },
        { status: 409 }
      );
    }

    await updateJobByFileId(fileId, {
      status: 'cancelled',
      error_message: null,
      completed_at: null,
    });

    return NextResponse.json({
      success: true,
      job_id: fileId,
      status: 'cancelled',
      message: 'Training canceled.',
    });
  } catch (error) {
    console.error('Cancel training job error:', error);
    const detail = error instanceof Error ? error.message : 'Failed to cancel training';
    return NextResponse.json({ error: detail }, { status: 500 });
  }
}
