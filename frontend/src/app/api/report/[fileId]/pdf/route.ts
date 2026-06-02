import fs from 'fs/promises';
import { NextResponse } from 'next/server';

import { findJobByFileId } from '@/lib/jobs/trainingJobs';

export const runtime = 'nodejs';

export async function GET(_req: Request, { params }: { params: Promise<{ fileId: string }> }) {
  const { fileId } = await params;
  const job = await findJobByFileId(fileId);

  if (!job?.pdf_path) {
    return NextResponse.json({ error: 'PDF report not found' }, { status: 404 });
  }

  const pdf = await fs.readFile(job.pdf_path);
  return new NextResponse(pdf, {
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="${fileId}_report.pdf"`,
    },
  });
}
