import { NextRequest, NextResponse } from 'next/server';

import { createTrainingJob } from '@/lib/jobs/trainingJobs';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const runtime = 'nodejs';

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

    const datasetInfo = body.dataset_info || null;
    const config = body.config || body;
    const userName = user.user_metadata?.full_name || user.user_metadata?.name || null;

    const job = await createTrainingJob({
      file_id: fileId,
      user_id: user.id,
      user_email: user.email,
      user_name: userName,
      status: 'queued',
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
      status: job.status,
    });
  } catch (error) {
    console.error('Create training job error:', error);
    return NextResponse.json({ error: 'Failed to create training job' }, { status: 500 });
  }
}
