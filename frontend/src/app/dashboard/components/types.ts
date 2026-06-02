export type PipelineStep = 'upload' | 'model' | 'training' | 'evaluation' | 'visualization';
export type ModelType = 'rnn' | 'qrnn';

export interface DatasetMeta {
  uploadId: string;
  filename: string;
  rows: number;
  columns: number;
  targetColumn: string;
  numClasses: number;
  recommendedQubits: number | null;
}

export interface ModelConfig {
  selectedRNN: boolean;
  selectedQRNN: boolean;
  comparisonMode: 'pca' | 'mi';
  featureSelector: 'pca' | 'mi';
  backend: 'PennyLane' | 'Qiskit';
  encoding: 'Ideal' | 'Noisy';
  noiseLevel: number;
  mitigationEnabled: boolean;
  mitigationRuns: number;
  rnnBatchSize: number;
  qrnnBatchSize: number;
  rnnEpochs: number;
  qrnnEpochs: number;
}

export interface TrainingConfig {
  [key: string]: unknown;
  model_types?: ModelType[];
  comparison_mode?: 'pca' | 'mi';
  feature_selector?: 'pca' | 'mi';
  rnn_epochs?: number;
  rnn_batch_size?: number;
  qrnn_epochs?: number;
  qrnn_batch_size?: number;
  qrnn_backend?: 'pennylane' | 'qiskit';
  noise_enabled?: boolean;
  noise_level?: number;
  mitigation_enabled?: boolean;
  mitigation_runs?: number;
  user_preferences?: {
    model_types: ModelType[];
    comparison_mode: 'pca' | 'mi';
    feature_selector: 'pca' | 'mi';
    qrnn_backend: 'pennylane' | 'qiskit';
    noise_enabled: boolean;
    noise_level: number;
    mitigation_enabled: boolean;
    mitigation_runs: number;
  };
  manual_overrides?: {
    rnn_epochs: number;
    qrnn_epochs: number;
    batch_size: number;
    rnn_batch_size: number;
    qrnn_batch_size: number;
  };
}

export interface TrainingMetricBlock {
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1_score?: number;
  loss?: number;
  training_time_seconds?: number;
  training_time_formatted?: string;
  confusion_matrix?: number[][];
  classification_report?: Record<string, unknown>;
  history?: {
    train_loss?: number[];
    val_loss?: number[];
    train_acc?: number[];
    val_acc?: number[];
    loss?: number[];
    accuracy?: number[];
  };
  [key: string]: unknown;
}

export interface TrainingResults {
  job_id?: string;
  status?: string;
  timestamp?: string;
  rnn?: TrainingMetricBlock;
  qrnn?:
    | TrainingMetricBlock
    | {
        clean?: TrainingMetricBlock;
        noisy?: TrainingMetricBlock;
        mitigated?: TrainingMetricBlock;
        history?: TrainingMetricBlock['history'];
      };
  comparison?: {
    better_model?: 'rnn' | 'qrnn' | string;
    rnn_accuracy?: number;
    qrnn_accuracy?: number;
    improvement?: number;
  };
}
