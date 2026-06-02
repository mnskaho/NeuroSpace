import fs from 'fs/promises';
import path from 'path';
import { NextRequest, NextResponse } from 'next/server';

import { findJobByFileId, updateJobByFileId } from '@/lib/jobs/trainingJobs';
import { sendTrainingReportEmail } from '@/lib/mail/sendTrainingReportEmail';
import { generateTrainingReportPdf } from '@/lib/reports/generateTrainingReportPdf';
import { extractAccuracy, extractModelName } from '@/lib/results/extractMetrics';
import { addFormattedTrainingTimes } from '@/lib/results/trainingTime';
import type { TrainingResults } from '@/app/dashboard/components/types';

export const runtime = 'nodejs';

export async function POST(req: NextRequest, { params }: { params: Promise<{ fileId: string }> }) {
  try {
    const { fileId } = await params;
    const results = addFormattedTrainingTimes((await req.json()) as TrainingResults);
    const job = await findJobByFileId(fileId);

    if (!job) {
      return NextResponse.json({ error: 'Job not found' }, { status: 404 });
    }

    const userEmail = job.user_email;
    if (!userEmail) {
      return NextResponse.json({ error: 'User email not found' }, { status: 400 });
    }

    const resultDir = path.join(process.cwd(), 'public', 'results', fileId);
    await fs.mkdir(resultDir, { recursive: true });

    const jsonPath = path.join(resultDir, 'results.json');
    const pdfPath = path.join(resultDir, 'report.pdf');

    await fs.writeFile(jsonPath, JSON.stringify(results, null, 2), 'utf-8');
    console.log('Results JSON saved');

    await generateTrainingReportPdf({ fileId, results, outputPath: pdfPath });
    console.log('PDF generated');
    console.log('PDF path', pdfPath);

    const completedAt = new Date().toISOString();
    await updateJobByFileId(fileId, {
      status: 'completed',
      results,
      pdf_path: pdfPath,
      json_path: jsonPath,
      completed_at: completedAt,
    });

    console.log('Job completed');
    console.log('Brevo email sending started');

    const emailResult = await sendTrainingReportEmail({
      toEmail: userEmail,
      toName: job.user_name || 'User',
      fileId,
      pdfPath,
      jsonPath,
      modelName: extractModelName(results),
      accuracy: extractAccuracy(results),
      createdAt: results?.timestamp || completedAt,
    });

    if (emailResult.success) {
      console.log('Brevo email sent successfully');
    } else {
      console.error('Brevo email failed');
      console.error('email_error', emailResult.error);
    }

    await updateJobByFileId(fileId, {
      email_sent: emailResult.success,
      email_sent_to: userEmail,
      email_sent_at: emailResult.success ? new Date().toISOString() : null,
      email_error: emailResult.success ? null : emailResult.error,
    });

    return NextResponse.json({
      success: true,
      fileId,
      email_sent: emailResult.success,
      email_error: emailResult.success ? null : emailResult.error,
    });
  } catch (error) {
    console.error('Complete job error:', error);
    return NextResponse.json({ error: 'Failed to complete job' }, { status: 500 });
  }
}
