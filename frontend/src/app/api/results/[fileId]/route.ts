import { NextResponse } from 'next/server';

import { findJobByFileId } from '@/lib/jobs/trainingJobs';

export const runtime = 'nodejs';

const UNKNOWN_DATASET_NAME = 'Unknown Dataset';

function getDatasetName(job: Awaited<ReturnType<typeof findJobByFileId>>) {
  const results = job?.results;
  if (results && typeof results === 'object' && !Array.isArray(results)) {
    const name = (results as Record<string, unknown>).dataset_name;
    if (typeof name === 'string' && name.trim()) return name.trim();
  }

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

  if (!job || job.status !== 'completed') {
    return NextResponse.json({ error: 'Results not available' }, { status: 404 });
  }

  return NextResponse.json({
    ...(typeof job.results === 'object' && job.results ? job.results : {}),
    job_id: job.file_id,
    dataset_name: getDatasetName(job),
  });
}
