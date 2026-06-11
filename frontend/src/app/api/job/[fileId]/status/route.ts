import { NextResponse } from 'next/server';

import { findJobByFileId } from '@/lib/jobs/trainingJobs';

export const runtime = 'nodejs';

const UNKNOWN_DATASET_NAME = 'Unknown Dataset';

function getDatasetName(job: Awaited<ReturnType<typeof findJobByFileId>>) {
  const datasetInfo = job?.dataset_info;
  if (datasetInfo && typeof datasetInfo === 'object' && !Array.isArray(datasetInfo)) {
    const name = datasetInfo.dataset_name || datasetInfo.filename || datasetInfo.name;
    if (typeof name === 'string' && name.trim()) return name.trim();
  }
  return job?.filename || UNKNOWN_DATASET_NAME;
}

export async function GET(_req: Request, { params }: { params: Promise<{ fileId: string }> }) {
  const { fileId } = await params;
  const job = await findJobByFileId(fileId);

  if (!job) {
    return NextResponse.json({ error: 'Job not found' }, { status: 404 });
  }

  return NextResponse.json({
    job_id: job.file_id,
    dataset_name: getDatasetName(job),
    status: job.status,
    progress:
      job.status === 'completed' ? 100 : job.status === 'cancelled' ? 0 : job.status === 'processing' ? 50 : 20,
    message: job.status,
    error: job.error_message || job.email_error,
  });
}
