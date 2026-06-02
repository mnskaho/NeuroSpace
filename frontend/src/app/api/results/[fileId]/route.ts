import { NextResponse } from 'next/server';

import { findJobByFileId } from '@/lib/jobs/trainingJobs';

export const runtime = 'nodejs';

export async function GET(_req: Request, { params }: { params: Promise<{ fileId: string }> }) {
  const { fileId } = await params;
  const job = await findJobByFileId(fileId);

  if (!job || job.status !== 'completed') {
    return NextResponse.json({ error: 'Results not available' }, { status: 404 });
  }

  return NextResponse.json({
    ...(typeof job.results === 'object' && job.results ? job.results : {}),
    job_id: job.file_id,
  });
}
