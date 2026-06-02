'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { toast } from 'sonner';

import {
  getJobStatus,
  getResults,
  startTraining as startBackendTraining,
} from '@/lib/backend';
import type {
  DatasetMeta,
  ModelConfig,
  TrainingConfig,
  TrainingResults,
} from '@/app/dashboard/components/types';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const SLOW_RESULTS_TOAST_DELAY_MS = 120_000;
const MAX_TRAINING_WAIT_MS = 2 * 60 * 60 * 1000;
const POLL_INTERVAL_MS = 3000;
const SLOW_RESULTS_MESSAGE =
  'The results may take a few more minutes. You can wait, or receive the report directly in your email inbox when it is ready.';

interface TrainingStepProps {
  datasetMeta: DatasetMeta | null;
  modelConfig: ModelConfig;
  onTrainingComplete: (results: TrainingResults) => void;
  onComplete: () => void;
}

export default function TrainingStep({
  datasetMeta,
  modelConfig,
  onTrainingComplete,
  onComplete,
}: TrainingStepProps) {
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('Ready to start training.');
  const [error, setError] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const pollRef = useRef<number | null>(null);
  const slowResultsTimerRef = useRef<number | null>(null);
  const slowResultsToastShownRef = useRef(false);
  const trainingStartedAtRef = useRef<number | null>(null);

  const selectedModels = useMemo(() => {
    const models: string[] = [];
    if (modelConfig.selectedRNN) models.push('Classical RNN / MLP');
    if (modelConfig.selectedQRNN) models.push('Quantum QNN');
    return models.length ? models.join(' + ') : 'No model selected';
  }, [modelConfig]);

  const summaryCards = useMemo(() => {
    const cards: Array<[string, string | number]> = [
      ['Dataset', datasetMeta?.filename || 'No dataset'],
      ['Selected Models', selectedModels],
    ];

    if (modelConfig.selectedRNN) {
      cards.push(['RNN Epochs', modelConfig.rnnEpochs]);
      cards.push(['RNN Batch', modelConfig.rnnBatchSize]);
    }

    if (modelConfig.selectedQRNN) {
      cards.push(['QNN Epochs', modelConfig.qrnnEpochs]);
      cards.push(['QNN Batch', modelConfig.qrnnBatchSize]);
    }

    return cards;
  }, [datasetMeta?.filename, modelConfig, selectedModels]);

  const backendPayloadRows = useMemo(() => {
    const rows: Array<[string, string | number]> = [
      ['Comparison', modelConfig.comparisonMode.toUpperCase()],
    ];

    if (modelConfig.selectedRNN) {
      rows.push(['RNN Epochs', modelConfig.rnnEpochs]);
      rows.push(['RNN Batch Size', modelConfig.rnnBatchSize]);
    }

    if (modelConfig.selectedQRNN) {
      rows.push(['QNN Epochs', modelConfig.qrnnEpochs]);
      rows.push(['QNN Batch Size', modelConfig.qrnnBatchSize]);
      rows.push(['QNN Backend', modelConfig.backend]);
      rows.push(['Noise', modelConfig.encoding === 'Noisy' ? `${modelConfig.noiseLevel}` : 'clean']);
      rows.push([
        'Mitigation',
        modelConfig.encoding === 'Noisy' && modelConfig.mitigationEnabled
          ? `${modelConfig.mitigationRuns} runs`
          : 'disabled',
      ]);
    }

    return rows;
  }, [modelConfig]);

  useEffect(() => {
    return () => {
      clearPolling();
      clearSlowResultsTimer();
    };
  }, []);

  const saveTraining = async () => {
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) return;

    await supabase.from('trainings').insert({
      user_id: user.id,
      dataset_name: datasetMeta?.filename || 'dataset',
    });
  };

  const clearPolling = () => {
    if (pollRef.current) {
      window.clearInterval(pollRef.current);
      pollRef.current = null;
    }
  };

  const clearSlowResultsTimer = () => {
    if (slowResultsTimerRef.current) {
      window.clearTimeout(slowResultsTimerRef.current);
      slowResultsTimerRef.current = null;
    }
  };

  const showSlowResultsToast = () => {
    if (slowResultsToastShownRef.current) return;

    slowResultsToastShownRef.current = true;
    toast.info(SLOW_RESULTS_MESSAGE, { duration: 12000 });
  };

  const getTrainingElapsedMs = () =>
    trainingStartedAtRef.current ? Date.now() - trainingStartedAtRef.current : 0;

  const hasReachedMaxTrainingWait = () => getTrainingElapsedMs() >= MAX_TRAINING_WAIT_MS;

  const stopAfterMaxTrainingWait = () => {
    clearPolling();
    clearSlowResultsTimer();
    setRunning(false);
    setProgress((currentProgress) => Math.max(currentProgress, 95));
    setStatus('Training wait time expired.');
    setError(
      'Training is still not available after 2 hours. Please check Colab or your backend connection.'
    );
  };

  const startTraining = async () => {
    setError(null);
    clearPolling();
    clearSlowResultsTimer();
    slowResultsToastShownRef.current = false;
    trainingStartedAtRef.current = null;

    if (!datasetMeta) {
      setError('No uploaded dataset found.');
      return;
    }

    if (!modelConfig.selectedRNN && !modelConfig.selectedQRNN) {
      setError('Select at least one model.');
      return;
    }

    const modelTypes = [
        ...(modelConfig.selectedRNN ? (['rnn'] as const) : []),
        ...(modelConfig.selectedQRNN ? (['qrnn'] as const) : []),
    ];

    const batchSize = modelConfig.selectedRNN
      ? modelConfig.rnnBatchSize
      : modelConfig.qrnnBatchSize;

    const payload: TrainingConfig = {
      user_preferences: {
        model_types: modelTypes,
        comparison_mode: modelConfig.comparisonMode,
        feature_selector: modelConfig.featureSelector || modelConfig.comparisonMode,
        qrnn_backend: modelConfig.backend.toLowerCase() as 'pennylane' | 'qiskit',
        noise_enabled: modelConfig.encoding === 'Noisy',
        noise_level: modelConfig.encoding === 'Noisy' ? modelConfig.noiseLevel : 0,
        mitigation_enabled:
          modelConfig.encoding === 'Noisy' && modelConfig.mitigationEnabled,
        mitigation_runs:
          modelConfig.encoding === 'Noisy' && modelConfig.mitigationEnabled
            ? modelConfig.mitigationRuns
            : 1,
      },
      manual_overrides: {
        rnn_epochs: modelConfig.rnnEpochs || 30,
        qrnn_epochs: modelConfig.qrnnEpochs || 20,
        batch_size: batchSize || 32,
        rnn_batch_size: modelConfig.rnnBatchSize || batchSize || 32,
        qrnn_batch_size: modelConfig.qrnnBatchSize || batchSize || 32,
      },
    };

    try {
      setRunning(true);
      setProgress(10);
      setStatus('Starting backend job...');
      trainingStartedAtRef.current = Date.now();
      slowResultsTimerRef.current = window.setTimeout(() => {
        showSlowResultsToast();
      }, SLOW_RESULTS_TOAST_DELAY_MS);

      await saveTraining();

      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session?.access_token) {
        throw new Error('Authentication required');
      }

      const response = await startBackendTraining(
        datasetMeta.uploadId,
        {
          config: payload,
          dataset_info: {
            samples: datasetMeta.rows,
            features: datasetMeta.columns,
            classes: datasetMeta.numClasses,
            target_column: datasetMeta.targetColumn,
          },
        },
        session.access_token
      );
      setJobId(response.job_id);
      setStatus('Backend job queued.');
      toast.success(
        'Your training has started. Your report will be sent automatically to your account email when it is ready.'
      );

      pollRef.current = window.setInterval(async () => {
        if (hasReachedMaxTrainingWait()) {
          stopAfterMaxTrainingWait();
          return;
        }

        try {
          const job = await getJobStatus(response.job_id);
          setProgress(
            job.progress ?? (job.status === 'running' || job.status === 'processing' ? 50 : 20)
          );
          setStatus(job.message || `Job ${job.status}`);

          if (job.status === 'completed') {
            try {
              const results = await getResults<TrainingResults>(response.job_id);
              const completedResults = { ...results, job_id: response.job_id };
              clearPolling();
              clearSlowResultsTimer();
              onTrainingComplete(completedResults);
              setProgress(100);
              setRunning(false);
              setStatus('Training completed.');
              onComplete();
            } catch {
              if (getTrainingElapsedMs() >= SLOW_RESULTS_TOAST_DELAY_MS) {
                showSlowResultsToast();
              }

              setProgress(95);
              setStatus('Training finished; waiting for results files...');
            }
          }

          if (job.status === 'failed') {
            clearPolling();
            clearSlowResultsTimer();
            setRunning(false);
            setError(job.error || job.detail || 'Backend training failed.');
            setStatus('Training failed.');
          }
        } catch {
          if (hasReachedMaxTrainingWait()) {
            stopAfterMaxTrainingWait();
            return;
          }

          if (getTrainingElapsedMs() >= SLOW_RESULTS_TOAST_DELAY_MS) {
            showSlowResultsToast();
          }

          setProgress((currentProgress) => Math.max(currentProgress, 50));
          setStatus('Still waiting for Colab results...');
          setError(null);
        }
      }, POLL_INTERVAL_MS);
    } catch (err) {
      clearSlowResultsTimer();
      setRunning(false);
      setError(err instanceof Error ? err.message : 'Training failed.');
      setStatus('Training error.');
    }
  };

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h2 className="font-mono font-black text-2xl text-text-primary mb-2">Model Training</h2>
        <p className="font-sans text-text-secondary text-sm">
          Start one backend job and poll FastAPI until results are ready.
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {summaryCards.map(([label, value]) => (
          <div key={label} className="glass rounded-xl p-4 border border-quantum-purple/10">
            <div className="font-mono text-[10px] text-text-muted uppercase tracking-wider mb-2">
              {label}
            </div>
            <div className="font-mono font-bold text-lg text-text-primary break-words">{value}</div>
          </div>
        ))}
      </div>

      {error && (
        <div className="mb-4 rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      <div className="glass rounded-xl p-4 mb-6">
        <div className="flex justify-between mb-2">
          <span className="font-mono text-xs text-text-muted">{status}</span>
          <span className="font-mono text-xs text-quantum-cyan">{progress}%</span>
        </div>
        <div className="progress-bar">
          <div
            className="progress-fill transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        {jobId && <div className="mt-3 font-mono text-[10px] text-text-muted">Job ID: {jobId}</div>}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="glass rounded-2xl p-6 border border-quantum-purple/10">
          <h3 className="font-mono font-bold text-sm text-text-primary mb-4">Dataset Summary</h3>
          <div className="space-y-3 text-sm font-mono text-text-secondary">
            <div>Target: {datasetMeta?.targetColumn ?? '-'}</div>
            <div>Classes: {datasetMeta?.numClasses ?? '-'}</div>
            <div>
              Shape:{' '}
              {datasetMeta ? `${datasetMeta.rows} x ${datasetMeta.columns}` : 'Upload required'}
            </div>
          </div>
        </div>

        <div className="glass rounded-2xl p-6 border border-quantum-purple/10">
          <h3 className="font-mono font-bold text-sm text-text-primary mb-4">Backend Payload</h3>
          <div className="space-y-3 text-sm font-mono text-text-secondary">
            {backendPayloadRows.map(([label, value]) => (
              <div key={label}>
                {label}: {value}
              </div>
            ))}
          </div>
        </div>
      </div>

      <button
        onClick={startTraining}
        disabled={running}
        className="btn-quantum px-8 py-4 rounded-xl font-mono text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {running ? 'Training...' : 'Start Training'}
      </button>
    </div>
  );
}
