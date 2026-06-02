import type { TrainingMetricBlock, TrainingResults } from '@/app/dashboard/components/types';

type QrnnVariants = {
  clean?: TrainingMetricBlock;
  noisy?: TrainingMetricBlock;
  mitigated?: TrainingMetricBlock;
  history?: TrainingMetricBlock['history'];
};

const getNumericSeconds = (value: unknown) =>
  typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null;

const hasQrnnVariants = (qrnn: TrainingResults['qrnn']): qrnn is QrnnVariants =>
  Boolean(
    qrnn &&
      typeof qrnn === 'object' &&
      ('clean' in qrnn || 'noisy' in qrnn || 'mitigated' in qrnn)
  );

export const formatTrainingTime = (
  trainingTimeFormatted?: unknown,
  trainingTimeSeconds?: unknown
) => {
  if (typeof trainingTimeFormatted === 'string' && trainingTimeFormatted.trim()) {
    return trainingTimeFormatted;
  }

  const seconds = getNumericSeconds(trainingTimeSeconds);
  if (seconds === null) return '-';

  const totalSeconds = Math.round(seconds);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const remainingSeconds = totalSeconds % 60;

  if (hours > 0) return `${hours}h ${minutes}m ${remainingSeconds}s`;
  if (minutes > 0) return `${minutes}m ${remainingSeconds}s`;
  return `${remainingSeconds}s`;
};

const withFormattedTrainingTime = (block: TrainingMetricBlock): TrainingMetricBlock => {
  if (typeof block.training_time_formatted === 'string' && block.training_time_formatted.trim()) {
    return block;
  }

  const formatted = formatTrainingTime(block.training_time_formatted, block.training_time_seconds);
  if (formatted === '-') return block;

  return {
    ...block,
    training_time_formatted: formatted,
  };
};

export const addFormattedTrainingTimes = (results: TrainingResults): TrainingResults => {
  const nextResults: TrainingResults = { ...results };

  if (results.rnn) {
    nextResults.rnn = withFormattedTrainingTime(results.rnn);
  }

  const qrnn = results.qrnn;
  if (!qrnn) return nextResults;

  if (hasQrnnVariants(qrnn)) {
    nextResults.qrnn = {
      ...qrnn,
      clean: qrnn.clean ? withFormattedTrainingTime(qrnn.clean) : qrnn.clean,
      noisy: qrnn.noisy ? withFormattedTrainingTime(qrnn.noisy) : qrnn.noisy,
      mitigated: qrnn.mitigated ? withFormattedTrainingTime(qrnn.mitigated) : qrnn.mitigated,
    };
  } else {
    nextResults.qrnn = withFormattedTrainingTime(qrnn);
  }

  return nextResults;
};
