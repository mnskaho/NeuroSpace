'use client';

import type { TrainingMetricBlock, TrainingResults } from '@/app/dashboard/components/types';
import { formatTrainingTime } from '@/lib/results/trainingTime';

interface EvaluationStepProps {
  trainingResults: TrainingResults;
  onComplete: () => void;
}

const getQrnnMain = (qrnn: TrainingResults['qrnn']): TrainingMetricBlock | null => {
  if (!qrnn) return null;
  const qrnnVariants = qrnn as {
    clean?: TrainingMetricBlock;
    noisy?: TrainingMetricBlock;
    mitigated?: TrainingMetricBlock;
  };
  if (qrnnVariants.mitigated) return qrnnVariants.mitigated;
  if (qrnnVariants.noisy) return qrnnVariants.noisy;
  if (qrnnVariants.clean) return qrnnVariants.clean;
  return qrnn as TrainingMetricBlock;
};

const getQrnnBlocks = (qrnn: TrainingResults['qrnn']) => {
  if (!qrnn) return [];
  const qrnnVariants = qrnn as {
    clean?: TrainingMetricBlock;
    noisy?: TrainingMetricBlock;
    mitigated?: TrainingMetricBlock;
  };
  const blocks: Array<{ title: string; metrics: TrainingMetricBlock }> = [];
  if (qrnnVariants.clean) blocks.push({ title: 'QNN Clean', metrics: qrnnVariants.clean });
  if (qrnnVariants.noisy) blocks.push({ title: 'QNN Noisy', metrics: qrnnVariants.noisy });
  if (qrnnVariants.mitigated) {
    blocks.push({ title: 'QNN Mitigated', metrics: qrnnVariants.mitigated });
  }
  if (!blocks.length) blocks.push({ title: 'QNN', metrics: qrnn as TrainingMetricBlock });
  return blocks;
};

const formatPercent = (value?: number) =>
  typeof value === 'number' ? `${(value * 100).toFixed(2)}%` : '-';

const formatNumber = (value?: number) => (typeof value === 'number' ? value.toFixed(4) : '-');

function MetricCard({
  title,
  metrics,
  accent,
}: {
  title: string;
  metrics: TrainingMetricBlock;
  accent: 'purple' | 'cyan';
}) {
  const accentClass = accent === 'cyan' ? 'text-quantum-cyan' : 'text-quantum-violet';

  return (
    <div className="glass rounded-2xl p-6 border border-quantum-purple/10">
      <div className="font-mono text-[10px] text-text-muted uppercase tracking-wider mb-3">
        {title}
      </div>
      <div className={`font-mono font-black text-3xl mb-4 ${accentClass}`}>
        {formatPercent(metrics.accuracy)}
      </div>
      <div className="grid grid-cols-2 gap-3 text-sm font-mono text-text-secondary">
        <div>Precision: {formatPercent(metrics.precision)}</div>
        <div>Recall: {formatPercent(metrics.recall)}</div>
        <div>F1 score: {formatPercent(metrics.f1_score)}</div>
        <div>Loss: {formatNumber(metrics.loss)}</div>
      </div>
    </div>
  );
}

function ConfusionMatrix({ matrix, title }: { matrix?: number[][]; title: string }) {
  if (!matrix?.length) return null;

  return (
    <div className="glass rounded-2xl p-6 border border-quantum-purple/10">
      <h3 className="font-mono font-bold text-sm text-text-primary mb-4">
        {title} Confusion Matrix
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full max-w-md">
          <tbody>
            {matrix.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((value, colIndex) => (
                  <td
                    key={`${rowIndex}-${colIndex}`}
                    className={`border border-quantum-purple/10 p-4 text-center font-mono text-sm ${
                      rowIndex === colIndex
                        ? 'bg-quantum-cyan/10 text-quantum-cyan'
                        : 'bg-panel-2 text-text-secondary'
                    }`}
                  >
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

type ClassReportMetric = {
  precision?: number;
  recall?: number;
  'f1-score'?: number;
  support?: number;
};

const isClassReportMetric = (value: unknown): value is ClassReportMetric =>
  Boolean(value) &&
  typeof value === 'object' &&
  ('precision' in value || 'recall' in value || 'f1-score' in value || 'support' in value);

const sortReportRows = ([leftLabel]: [string, ClassReportMetric], [rightLabel]: [string, ClassReportMetric]) => {
  const summaryOrder: Record<string, number> = {
    'macro avg': 1,
    'weighted avg': 2,
  };
  const leftSummary = summaryOrder[leftLabel];
  const rightSummary = summaryOrder[rightLabel];

  if (leftSummary && rightSummary) return leftSummary - rightSummary;
  if (leftSummary) return 1;
  if (rightSummary) return -1;

  const leftNumber = Number(leftLabel);
  const rightNumber = Number(rightLabel);

  if (Number.isFinite(leftNumber) && Number.isFinite(rightNumber)) {
    return leftNumber - rightNumber;
  }

  return leftLabel.localeCompare(rightLabel, undefined, { numeric: true });
};

function ClassificationReport({
  report,
  title,
}: {
  report?: TrainingMetricBlock['classification_report'];
  title: string;
}) {
  const rows = Object.entries(report ?? {})
    .filter((entry): entry is [string, ClassReportMetric] => isClassReportMetric(entry[1]))
    .sort(sortReportRows);

  if (!rows.length) return null;

  return (
    <div className="glass rounded-2xl p-6 border border-quantum-purple/10">
      <h3 className="font-mono font-bold text-sm text-text-primary mb-4">
        {title} Classification Report
      </h3>
      <div className="responsive-table">
        <table className="w-full">
          <thead>
            <tr className="border-b border-quantum-purple/10">
              {['Class', 'Precision', 'Recall', 'F1 score', 'Support'].map((heading) => (
                <th
                  key={heading}
                  className="font-mono text-xs text-text-muted uppercase text-left py-3"
                >
                  {heading}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map(([className, metrics]) => (
              <tr
                key={className}
                className="border-b border-quantum-purple/5 hover:bg-panel/30 transition-colors"
              >
                <td className="font-mono text-sm text-text-primary py-3">{className}</td>
                <td className="font-mono text-sm text-text-secondary py-3">
                  {formatPercent(metrics.precision)}
                </td>
                <td className="font-mono text-sm text-text-secondary py-3">
                  {formatPercent(metrics.recall)}
                </td>
                <td className="font-mono text-sm text-text-secondary py-3">
                  {formatPercent(metrics['f1-score'])}
                </td>
                <td className="font-mono text-sm text-text-secondary py-3">
                  {typeof metrics.support === 'number' ? metrics.support : '-'}
                </td>
              </tr>
            ))}
            {typeof report?.accuracy === 'number' && (
              <tr className="border-b border-quantum-purple/5">
                <td className="font-mono text-sm text-text-primary py-3">accuracy</td>
                <td className="font-mono text-sm text-text-secondary py-3">-</td>
                <td className="font-mono text-sm text-text-secondary py-3">-</td>
                <td className="font-mono text-sm text-text-secondary py-3">
                  {formatPercent(report.accuracy)}
                </td>
                <td className="font-mono text-sm text-text-secondary py-3">-</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function EvaluationStep({ trainingResults, onComplete }: EvaluationStepProps) {
  const rnn = trainingResults.rnn ?? null;
  const qrnn = getQrnnMain(trainingResults.qrnn);
  const qrnnBlocks = getQrnnBlocks(trainingResults.qrnn);
  const hasResults = Boolean(rnn || qrnn);

  const comparisonRows = [
    { label: 'Accuracy', rnnValue: rnn?.accuracy, qrnnValue: qrnn?.accuracy, format: 'percent' },
    { label: 'Precision', rnnValue: rnn?.precision, qrnnValue: qrnn?.precision, format: 'percent' },
    { label: 'Recall', rnnValue: rnn?.recall, qrnnValue: qrnn?.recall, format: 'percent' },
    { label: 'F1 score', rnnValue: rnn?.f1_score, qrnnValue: qrnn?.f1_score, format: 'percent' },
    { label: 'Loss', rnnValue: rnn?.loss, qrnnValue: qrnn?.loss, format: 'number' },
    {
      label: 'Training Time',
      rnnValue: formatTrainingTime(rnn?.training_time_formatted, rnn?.training_time_seconds),
      qrnnValue: formatTrainingTime(qrnn?.training_time_formatted, qrnn?.training_time_seconds),
      format: 'text',
    },
  ] as const;

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h2 className="font-mono font-black text-2xl text-text-primary mb-2">
          Evaluation & Benchmarks
        </h2>
        <p className="font-sans text-text-secondary text-sm">
          Metrics returned by the FastAPI job.
        </p>
      </div>

      {!hasResults ? (
        <div className="glass rounded-2xl p-8 border border-quantum-purple/10 text-center">
          <p className="font-mono text-sm text-text-primary">No training results available.</p>
          <p className="font-mono text-xs text-text-muted mt-2">
            Please run the training step first.
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {rnn && <MetricCard title="Classical RNN" metrics={rnn} accent="purple" />}
            {qrnnBlocks.map(({ title, metrics }) => (
              <MetricCard key={title} title={title} metrics={metrics} accent="cyan" />
            ))}
          </div>

          {rnn && qrnn && trainingResults.comparison && (
            <div className="glass rounded-2xl p-6 border border-quantum-purple/10 mb-8">
              <h3 className="font-mono font-bold text-sm text-text-primary mb-4">Best Model</h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-panel-2 rounded-xl p-4">
                  <div className="font-mono text-[10px] text-text-muted uppercase">Winner</div>
                  <div className="font-mono font-bold text-lg text-text-primary uppercase">
                    {trainingResults.comparison.better_model ?? '-'}
                  </div>
                </div>
                <div className="bg-panel-2 rounded-xl p-4">
                  <div className="font-mono text-[10px] text-text-muted uppercase">
                    RNN Accuracy
                  </div>
                  <div className="font-mono font-bold text-lg text-text-primary">
                    {formatPercent(trainingResults.comparison.rnn_accuracy)}
                  </div>
                </div>
                <div className="bg-panel-2 rounded-xl p-4">
                  <div className="font-mono text-[10px] text-text-muted uppercase">
                    QNN Accuracy
                  </div>
                  <div className="font-mono font-bold text-lg text-text-primary">
                    {formatPercent(trainingResults.comparison.qrnn_accuracy)}
                  </div>
                </div>
                <div className="bg-panel-2 rounded-xl p-4">
                  <div className="font-mono text-[10px] text-text-muted uppercase">Improvement</div>
                  <div className="font-mono font-bold text-lg text-text-primary">
                    {formatPercent(trainingResults.comparison.improvement)}
                  </div>
                </div>
              </div>
            </div>
          )}

          {rnn && qrnn && (
            <div className="glass rounded-2xl p-6 mb-8 border border-quantum-purple/10">
              <h3 className="font-mono font-bold text-sm text-text-primary mb-4">RNN vs QNN</h3>
              <div className="responsive-table">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-quantum-purple/10">
                      <th className="font-mono text-xs text-text-muted uppercase text-left py-3">
                        Metric
                      </th>
                      <th className="font-mono text-xs text-quantum-violet uppercase text-center py-3">
                        RNN
                      </th>
                      <th className="font-mono text-xs text-quantum-cyan uppercase text-center py-3">
                        QNN
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparisonRows.map(({ label, rnnValue, qrnnValue, format }) => (
                      <tr
                        key={label}
                        className="border-b border-quantum-purple/5 hover:bg-panel/30 transition-colors"
                      >
                        <td className="font-mono text-sm text-text-secondary py-3">{label}</td>
                        <td className="font-mono text-sm text-text-primary text-center py-3">
                          {format === 'text'
                            ? rnnValue
                            : format === 'number'
                              ? formatNumber(rnnValue)
                              : formatPercent(rnnValue)}
                        </td>
                        <td className="font-mono text-sm text-quantum-cyan text-center py-3 font-bold">
                          {format === 'text'
                            ? qrnnValue
                            : format === 'number'
                              ? formatNumber(qrnnValue)
                              : formatPercent(qrnnValue)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {rnn && <ConfusionMatrix matrix={rnn.confusion_matrix} title="Classical RNN" />}
            {qrnnBlocks.map(({ title, metrics }) => (
              <ConfusionMatrix key={title} matrix={metrics.confusion_matrix} title={title} />
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {rnn && (
              <ClassificationReport report={rnn.classification_report} title="Classical RNN" />
            )}
            {qrnnBlocks.map(({ title, metrics }) => (
              <ClassificationReport
                key={title}
                report={metrics.classification_report}
                title={title}
              />
            ))}
          </div>

          <button
            onClick={onComplete}
            className="btn-quantum px-8 py-4 rounded-xl font-mono text-sm font-semibold"
          >
            Visualize & Export
          </button>
        </>
      )}
    </div>
  );
}
