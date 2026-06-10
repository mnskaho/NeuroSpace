import { supabaseAdmin } from '@/lib/supabase/admin';

export type TrainingJobData = {
  file_id: string;
  user_id: string;
  user_email: string;
  user_name?: string | null;
  status: string;
  dataset_name?: string | null;
  config?: Record<string, unknown> | null;
  dataset_info?: Record<string, unknown> | null;
};

export type TrainingJob = TrainingJobData & {
  id?: string;
  filename?: string | null;
  file_path?: string | null;
  results?: unknown;
  pdf_path?: string | null;
  json_path?: string | null;
  email_sent?: boolean | null;
  email_sent_to?: string | null;
  email_sent_at?: string | null;
  email_error?: string | null;
  error_message?: string | null;
  created_at?: string;
  started_at?: string | null;
  completed_at?: string | null;
  updated_at?: string | null;
};

export async function createTrainingJob(data: TrainingJobData) {
  const { data: job, error } = await supabaseAdmin
    .from('training_jobs')
    .insert({
      file_id: data.file_id,
      user_id: data.user_id,
      user_email: data.user_email,
      user_name: data.user_name ?? null,
      status: data.status,
      dataset_name: data.dataset_name ?? null,
      config: data.config ?? null,
      dataset_info: data.dataset_info ?? null,
      email_sent: false,
      email_sent_to: null,
      email_sent_at: null,
      email_error: null,
    })
    .select('*')
    .single();

  if (error) throw error;
  return job as TrainingJob;
}

export async function findJobByFileId(fileId: string) {
  const { data, error } = await supabaseAdmin
    .from('training_jobs')
    .select('*')
    .eq('file_id', fileId)
    .single();

  if (error) {
    if (error.code === 'PGRST116') return null;
    throw error;
  }

  return data as TrainingJob;
}

export async function updateJobByFileId(fileId: string, data: Record<string, unknown>) {
  const { data: job, error } = await supabaseAdmin
    .from('training_jobs')
    .update({
      ...data,
      updated_at: new Date().toISOString(),
    })
    .eq('file_id', fileId)
    .select('*')
    .single();

  if (error) throw error;
  return job as TrainingJob;
}

export async function getNextQueuedJob() {
  const { data, error } = await supabaseAdmin
    .from('training_jobs')
    .select('*')
    .eq('status', 'queued')
    .order('created_at', { ascending: true })
    .limit(1)
    .maybeSingle();

  if (error) throw error;
  return data as TrainingJob | null;
}
