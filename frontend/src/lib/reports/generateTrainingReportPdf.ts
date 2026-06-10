import fs from 'fs/promises';
import path from 'path';

import type { TrainingResults } from '@/app/dashboard/components/types';
import { extractAccuracy, extractModelName, getResultBlocks } from '@/lib/results/extractMetrics';
import { formatTrainingTime } from '@/lib/results/trainingTime';

type GenerateTrainingReportPdfParams = {
  fileId: string;
  results: TrainingResults;
  outputPath: string;
};

const escapePdfText = (value: unknown) =>
  String(value ?? '-')
    .replace(/\\/g, '\\\\')
    .replace(/\(/g, '\\(')
    .replace(/\)/g, '\\)');

const formatPercent = (value?: number) =>
  typeof value === 'number' ? `${(value * 100).toFixed(2)}%` : '-';

const formatNumber = (value?: number) => (typeof value === 'number' ? value.toFixed(4) : '-');

export async function generateTrainingReportPdf({
  fileId,
  results,
  outputPath,
}: GenerateTrainingReportPdfParams) {
  await fs.mkdir(path.dirname(outputPath), { recursive: true });

  const blocks = getResultBlocks(results);
  const datasetName = results.dataset_name || 'Unknown Dataset';
  const lines = [
    'NeuroSpace Training Report',
    '',
    `Dataset: ${datasetName}`,
    `Job ID: ${fileId}`,
    `Date: ${new Date().toISOString()}`,
    `Status: ${String(results.status ?? 'completed')}`,
    `Model: ${extractModelName(results)}`,
    `Accuracy: ${extractAccuracy(results)}`,
    '',
    'Summary',
  ];

  for (const [title, block] of blocks) {
    lines.push(
      '',
      title,
      `Accuracy: ${formatPercent(block.accuracy)}`,
      `Precision: ${formatPercent(block.precision)}`,
      `Recall: ${formatPercent(block.recall)}`,
      `F1-score: ${formatPercent(block.f1_score)}`,
      `Loss: ${formatNumber(block.loss)}`,
      `Training Time: ${formatTrainingTime(
        block.training_time_formatted,
        block.training_time_seconds
      )}`,
      `Train accuracy: ${formatPercent(block.train_accuracy)}`,
      `Validation accuracy: ${formatPercent(block.val_accuracy)}`
    );
  }

  if (results.comparison) {
    lines.push('', 'Comparison', JSON.stringify(results.comparison, null, 2));
  }

  const contentLines = lines.flatMap((line) => String(line).split('\n'));
  const stream = [
    'BT',
    '/F1 18 Tf',
    '50 790 Td',
    `(${escapePdfText(contentLines[0])}) Tj`,
    '/F1 10 Tf',
    '0 -24 Td',
    ...contentLines.slice(1).map((line) => `0 -14 Td (${escapePdfText(line)}) Tj`),
    'ET',
  ].join('\n');

  const objects = [
    '1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj',
    '2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj',
    '3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj',
    '4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj',
    `5 0 obj << /Length ${Buffer.byteLength(stream)} >> stream\n${stream}\nendstream endobj`,
  ];

  let pdf = '%PDF-1.4\n';
  const offsets = [0];
  for (const object of objects) {
    offsets.push(Buffer.byteLength(pdf));
    pdf += `${object}\n`;
  }

  const xrefOffset = Buffer.byteLength(pdf);
  pdf += `xref\n0 ${objects.length + 1}\n`;
  pdf += '0000000000 65535 f \n';
  for (const offset of offsets.slice(1)) {
    pdf += `${String(offset).padStart(10, '0')} 00000 n \n`;
  }
  pdf += `trailer << /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`;

  await fs.writeFile(outputPath, pdf, 'binary');
  return outputPath;
}
