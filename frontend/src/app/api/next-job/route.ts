import { NextResponse } from 'next/server';

import { getNextQueuedJob, updateJobByFileId } from '@/lib/jobs/trainingJobs';

export const runtime = 'nodejs';
const UNKNOWN_DATASET_NAME = 'Unknown Dataset';

function asObject(value: unknown): Record<string, unknown> {
  return value && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

function asNumber(value: unknown, fallback: number) {
  return typeof value === 'number' && Number.isFinite(value) ? value : fallback;
}

function getDatasetName(job: NonNullable<Awaited<ReturnType<typeof getNextQueuedJob>>>) {
  const datasetInfo = asObject(job.dataset_info);
  const name = datasetInfo.dataset_name || datasetInfo.filename || datasetInfo.name || job.filename;
  return typeof name === 'string' && name.trim() ? name.trim() : UNKNOWN_DATASET_NAME;
}

function normalizeTrainingConfig(rawConfig: unknown) {
  let config = asObject(rawConfig);

  if ('config' in config && !('user_preferences' in config) && !('manual_overrides' in config)) {
    config = asObject(config.config);
  }

  const userPreferences = asObject(config.user_preferences);
  const manualOverrides = asObject(config.manual_overrides);
  const comparisonMode = String(
    userPreferences.comparison_mode || config.comparison_mode || 'pca'
  );
  const batchSize = asNumber(manualOverrides.batch_size || config.batch_size, 32);

  return {
    user_preferences: {
      model_types: Array.isArray(userPreferences.model_types)
        ? userPreferences.model_types
        : Array.isArray(config.model_types)
          ? config.model_types
          : ['rnn', 'qrnn'],
      comparison_mode: comparisonMode,
      feature_selector: String(
        userPreferences.feature_selector || config.feature_selector || comparisonMode
      ),
      qrnn_backend: String(userPreferences.qrnn_backend || config.qrnn_backend || 'pennylane'),
      noise_enabled: Boolean(userPreferences.noise_enabled || config.noise_enabled || false),
      noise_level: asNumber(userPreferences.noise_level || config.noise_level, 0),
      mitigation_enabled: Boolean(
        userPreferences.mitigation_enabled || config.mitigation_enabled || false
      ),
      mitigation_runs: asNumber(userPreferences.mitigation_runs || config.mitigation_runs, 1),
    },
    manual_overrides: {
      rnn_epochs: asNumber(manualOverrides.rnn_epochs || config.rnn_epochs, 30),
      qrnn_epochs: asNumber(manualOverrides.qrnn_epochs || config.qrnn_epochs, 20),
      batch_size: batchSize,
      rnn_batch_size: asNumber(manualOverrides.rnn_batch_size || config.rnn_batch_size, batchSize),
      qrnn_batch_size: asNumber(
        manualOverrides.qrnn_batch_size || config.qrnn_batch_size,
        batchSize
      ),
    },
  };
}

export async function GET() {
  try {
    const job = await getNextQueuedJob();

    if (!job) {
      return NextResponse.json({ status: 'no_job', message: 'No queued job' }, { status: 404 });
    }

    const normalizedConfig = normalizeTrainingConfig(job.config);
    const datasetName = getDatasetName(job);
    const datasetInfo = {
      ...asObject(job.dataset_info),
      dataset_name: datasetName,
    };

    await updateJobByFileId(job.file_id, {
      status: 'processing',
      config: normalizedConfig,
      dataset_info: datasetInfo,
      started_at: new Date().toISOString(),
    });

    console.log('Next job picked');
    console.log('file_id', job.file_id);
    console.log('Job processing');

    return NextResponse.json({
      status: 'success',
      job_id: job.file_id,
      file_id: job.file_id,
      dataset_name: datasetName,
      config: normalizedConfig,
      job: {
        file_id: job.file_id,
        dataset_name: datasetName,
        dataset_info: datasetInfo,
        ...normalizedConfig,
      },
      dataset_info: datasetInfo,
      user_preferences: normalizedConfig.user_preferences,
      manual_overrides: normalizedConfig.manual_overrides,
    });
  } catch (error) {
    console.error('Next job error:', error);
    return NextResponse.json({ error: 'Failed to get next job' }, { status: 500 });
  }
}
