const BACKEND_BASE_URL = (
  process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:7000/api'
).replace(/\/+$/, '');

async function backendFetch<T>(path: string, options: RequestInit = {}) {
  const requestOptions = {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
    },
  };

  const response = await fetch(`${BACKEND_BASE_URL}${path}`, requestOptions);

  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const message = payload?.detail || payload?.error || payload?.message || response.statusText;
    throw new Error(message);
  }

  return payload as T;
}

async function appFetch<T>(path: string, options: RequestInit = {}) {
  const requestOptions = {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
    },
  };

  const response = await fetch(path, requestOptions);
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const message = payload?.detail || payload?.error || payload?.message || response.statusText;
    throw new Error(message);
  }

  return payload as T;
}

export interface UploadDatasetResponse {
  file_id: string;
  filename: string;
  dataset_info: {
    samples: number;
    features: number;
    target_column: string;
    classes: number;
    recommended_qubits?: number | null;
  };
}

export interface StartTrainingResponse {
  job_id: string;
  status: string;
}

export interface JobStatusResponse {
  job_id: string;
  status: 'uploaded' | 'queued' | 'processing' | 'running' | 'completed' | 'failed';
  progress?: number;
  message?: string;
  error?: string;
  detail?: string;
}

export function uploadDataset(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  return backendFetch<UploadDatasetResponse>('/upload', {
    method: 'POST',
    body: formData,
  });
}

export function startTraining(fileId: string, payload: Record<string, unknown>, accessToken?: string) {
  return appFetch<StartTrainingResponse>(`/api/train/${fileId}`, {
    method: 'POST',
    headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
    body: JSON.stringify(payload),
  });
}

export function getJobStatus(jobId: string) {
  return appFetch<JobStatusResponse>(`/api/job/${jobId}/status`);
}

export function getResults<T>(jobId: string) {
  return appFetch<T>(`/api/results/${jobId}`);
}

export function getReportPdfUrl(jobId: string) {
  return `/api/report/${jobId}/pdf`;
}
