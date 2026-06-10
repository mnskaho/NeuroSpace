'use client';

import { useRef, useState } from 'react';
import { toast } from 'sonner';

import Icon from '@/components/ui/AppIcon';
import { uploadDataset } from '@/lib/backend';
import { getUserPlan } from '@/lib/getUserPlan';
import { getTrainingCount } from '@/lib/getUserTrainings';
import { PLAN_LIMITS } from '@/lib/plans';
import { validateDataset } from '@/lib/validateDataset';
import type { DatasetMeta } from '@/app/dashboard/components/types';

interface UploadStepProps {
  onComplete: (metadata: DatasetMeta) => void;
}

const datasetRequirements = [
  { icon: 'CalculatorIcon', label: 'Numeric dataset only' },
  { icon: 'SparklesIcon', label: 'Preprocessed data' },
  { icon: 'NoSymbolIcon', label: 'No missing values' },
  { icon: 'DocumentTextIcon', label: 'Max size: 100MB' },
  { icon: 'DocumentIcon', label: 'Format: CSV' },
  { icon: 'Squares2X2Icon', label: 'Sequences x Features structure' },
];

export default function UploadStep({ onComplete }: UploadStepProps) {
  const [dragOver, setDragOver] = useState(false);
  const [uploaded, setUploaded] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [datasetMeta, setDatasetMeta] = useState<DatasetMeta | null>(null);
  const [datasetInfo, setDatasetInfo] = useState<{
    records: number;
    features: number;
    size: string;
  } | null>(null);

  const fileRef = useRef<HTMLInputElement>(null);

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  const updateProgress = async (target: number) => {
    return new Promise<void>((resolve) => {
      const interval = window.setInterval(() => {
        setProgress((current) => {
          if (current >= target) {
            window.clearInterval(interval);
            resolve();
            return target;
          }
          return Math.min(current + 10, target);
        });
      }, 80);
    });
  };

  const handleFile = async (file: File) => {
    setUploaded(null);
    setError(null);
    setDatasetMeta(null);
    setDatasetInfo(null);
    setProcessing(true);
    setProgress(0);

    try {
      const validation = await validateDataset(file);

      if (!validation.isValid) {
        toast.error(validation.error || 'Invalid dataset');
        return;
      }

      const text = await file.text();
      const lines = text.trim().split('\n');
      const features = lines[0]?.split(',').length ?? 0;

      setUploaded(file.name);
      setDatasetInfo({
        records: Math.max(lines.length - 1, 0),
        features,
        size: formatBytes(file.size),
      });

      await updateProgress(30);
      const response = await uploadDataset(file);
      await updateProgress(100);

      const metadata: DatasetMeta = {
        uploadId: response.file_id,
        filename: response.dataset_name || response.filename || file.name,
        filePath: response.file_path,
        rows: response.dataset_info.samples,
        columns: response.dataset_info.features,
        targetColumn: response.dataset_info.target_column,
        numClasses: response.dataset_info.classes,
        recommendedQubits: response.dataset_info.recommended_qubits ?? null,
      };

      setDatasetMeta(metadata);
      toast.success('Dataset uploaded successfully');
    } catch (err) {
      console.error(err);
      const message = err instanceof Error ? err.message : 'Backend upload failed';
      setError(message);
      toast.error(message);
    } finally {
      setProcessing(false);
    }
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    setDragOver(false);

    const file = event.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const handleContinue = async () => {
    if (!datasetMeta) {
      toast.error('Dataset metadata missing');
      return;
    }

    const plan = (await getUserPlan()) as keyof typeof PLAN_LIMITS;
    const trainings = await getTrainingCount();
    const limit = PLAN_LIMITS[plan];

    if (trainings >= limit) {
      toast.error('Training limit reached. Upgrade to premium');
      return;
    }

    onComplete(datasetMeta);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h2 className="font-mono font-black text-2xl text-text-primary mb-2">Dataset Upload</h2>
        <p className="font-sans text-text-secondary text-sm">
          Import your structured sequences. Supported format: CSV
        </p>
      </div>

      <div className="flex flex-col md:flex-row gap-6 mb-6">
        <div className="md:flex-[0_0_50%]">
          <div
            className={`upload-zone rounded-2xl p-12 text-center cursor-pointer transition-all ${
              dragOver ? 'dragover' : ''
            }`}
            onDragOver={(event) => {
              event.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileRef.current?.click()}
          >
            <input
              ref={fileRef}
              type="file"
              accept=".csv"
              className="hidden"
              onChange={(event) => {
                if (event.target.files?.[0]) handleFile(event.target.files[0]);
              }}
            />

            {uploaded ? (
              <div className="flex flex-col items-center gap-3">
                <div className="w-16 h-16 rounded-2xl bg-quantum-teal/10 border border-quantum-teal/30 flex items-center justify-center">
                  <Icon name="DocumentCheckIcon" size={32} className="text-quantum-teal" />
                </div>
                <div className="font-mono font-bold text-text-primary break-words">
                  Dataset: {uploaded}
                </div>
                {datasetInfo && (
                  <div className="text-xs text-text-muted">
                    Records: {datasetInfo.records} | Features: {datasetInfo.features} | Size:{' '}
                    {datasetInfo.size}
                  </div>
                )}
                {processing ? (
                  <div className="w-full max-w-xs mt-2">
                    <div className="flex justify-between mb-1">
                      <span className="font-mono text-xs text-text-muted">Uploading...</span>
                      <span className="font-mono text-xs text-quantum-cyan">{progress}%</span>
                    </div>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${progress}%` }} />
                    </div>
                  </div>
                ) : (
                  <span className="badge-success px-3 py-1 rounded-full font-mono text-xs">
                    Ready
                  </span>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-quantum-purple/10 border border-quantum-purple/20 flex items-center justify-center">
                  <Icon name="ArrowUpTrayIcon" size={32} className="text-quantum-violet" />
                </div>
                <div>
                  <div className="font-mono font-bold text-text-primary">
                    Drop your dataset here
                  </div>
                  <div className="font-mono text-xs text-text-muted">or click to browse - CSV</div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="md:flex-[0_0_29%] glass rounded-2xl p-6 bg-panel-2">
          <h3 className="font-mono font-bold text-sm text-text-primary mb-4">
            Dataset Requirements
          </h3>
          <ul className="flex flex-col gap-3">
            {datasetRequirements.map((req) => (
              <li
                key={req.label}
                className="flex items-center gap-2 font-mono text-xs text-text-secondary"
              >
                <Icon name={req.icon} size={16} className="text-quantum-cyan" />
                {req.label}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {error && (
        <div className="mb-6 rounded-2xl border border-red-500/30 bg-red-500/10 p-4">
          <div className="font-mono text-sm text-red-400">{error}</div>
        </div>
      )}

      {datasetMeta && !processing && (
        <div className="glass rounded-2xl p-6 mb-8 bg-panel-2">
          <h3 className="font-mono font-bold text-sm text-text-primary mb-4">Dataset Ready</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              ['Dataset', datasetMeta.filename],
              ['Dimensions', `${datasetMeta.rows} x ${datasetMeta.columns}`],
              ['Target', datasetMeta.targetColumn],
              ['Classes', datasetMeta.numClasses],
            ].map(([label, value]) => (
              <div key={label} className="bg-panel-1 rounded-xl p-4">
                <div className="font-mono text-[10px] text-text-muted uppercase">{label}</div>
                <div className="font-mono font-bold text-sm text-text-primary break-words">
                  {value}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={handleContinue}
        disabled={!uploaded || processing || !datasetMeta}
        className="btn-quantum px-8 py-4 rounded-xl font-mono text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed"
      >
        Continue to Model Config
      </button>
    </div>
  );
}
