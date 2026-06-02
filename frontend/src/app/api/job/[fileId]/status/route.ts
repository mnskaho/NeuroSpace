import { NextResponse } from 'next/server';

import { findJobByFileId } from '@/lib/jobs/trainingJobs';

export const runtime = 'nodejs';

export async function GET(_req: Request, { params }: { params: Promise<{ fileId: string }> }) {
  const { fileId } = await params;
  const job = await findJobByFileId(fileId);

  if (!job) {
    return NextResponse.json({ error: 'Job not found' }, { status: 404 });
  }

  return NextResponse.json({
    job_id: job.file_id,
    status: job.status,
    progress: job.status === 'completed' ? 100 : job.status === 'processing' ? 50 : 20,
    message: job.status,
    error: job.error_message || job.email_error,
  });
}
