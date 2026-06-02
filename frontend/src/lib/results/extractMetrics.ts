type ResultBlock = {
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1_score?: number;
  loss?: number;
  training_time_seconds?: number;
  training_time_formatted?: string;
  train_accuracy?: number;
  val_accuracy?: number;
};

type TrainingResultsLike = {
  comparison?: {
    better_model?: string;
    qrnn_accuracy?: number;
    rnn_accuracy?: number;
  };
  rnn?: ResultBlock;
  qrnn?:
    | ResultBlock
    | {
        clean?: ResultBlock;
        noisy?: ResultBlock;
        mitigated?: ResultBlock;
      };
};

const formatAccuracy = (value?: number) =>
  typeof value === 'number' ? `${(value * 100).toFixed(2)}%` : 'N/A';

export function extractAccuracy(results: TrainingResultsLike) {
  return (
    formatAccuracy(results.comparison?.qrnn_accuracy) !== 'N/A'
      ? formatAccuracy(results.comparison?.qrnn_accuracy)
      : formatAccuracy(results.comparison?.rnn_accuracy) !== 'N/A'
        ? formatAccuracy(results.comparison?.rnn_accuracy)
        : formatAccuracy(results.rnn?.accuracy) !== 'N/A'
          ? formatAccuracy(results.rnn?.accuracy)
          : typeof results.qrnn === 'object' && results.qrnn && 'clean' in results.qrnn
            ? formatAccuracy(
                results.qrnn.clean?.accuracy ??
                  results.qrnn.noisy?.accuracy ??
                  results.qrnn.mitigated?.accuracy
              )
            : formatAccuracy((results.qrnn as ResultBlock | undefined)?.accuracy)
  );
}

export function extractModelName(results: TrainingResultsLike) {
  if (results.comparison?.better_model) return results.comparison.better_model;
  if (results.rnn) return 'RNN / MLP';
  if (results.qrnn) return 'QNN';
  return 'Training Model';
}

export function getResultBlocks(results: TrainingResultsLike) {
  const blocks: Array<[string, ResultBlock]> = [];
  if (results.rnn) blocks.push(['RNN / MLP', results.rnn]);

  const qrnn = results.qrnn;
  if (qrnn && 'clean' in qrnn) {
    if (qrnn.clean) blocks.push(['QNN Clean', qrnn.clean]);
    if (qrnn.noisy) blocks.push(['QNN Noisy', qrnn.noisy]);
    if (qrnn.mitigated) blocks.push(['QNN Mitigated', qrnn.mitigated]);
  } else if (qrnn) {
    blocks.push(['QNN', qrnn as ResultBlock]);
  }

  return blocks;
}
