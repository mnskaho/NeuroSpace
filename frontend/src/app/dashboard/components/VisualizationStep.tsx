'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import { getReportPdfUrl } from '@/lib/backend';
import { submitUserComment } from '@/lib/comments';
import { exportResultsAsJson } from '@/lib/exportResults';
import { addFormattedTrainingTimes } from '@/lib/results/trainingTime';
import { supabase } from '@/lib/supabase';
import type { TrainingMetricBlock, TrainingResults } from '@/app/dashboard/components/types';

interface VisualizationStepProps {
  trainingResults: TrainingResults;
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

const getHistory = (result: TrainingMetricBlock | null | undefined) => result?.history ?? null;

const buildLearningData = (trainingResults: TrainingResults) => {
  const rnnHistory = getHistory(trainingResults.rnn);
  const qrnnHistory = getHistory(getQrnnMain(trainingResults.qrnn));

  const epochs = Math.max(
    rnnHistory?.train_acc?.length ?? rnnHistory?.accuracy?.length ?? 0,
    rnnHistory?.val_acc?.length ?? 0,
    rnnHistory?.train_loss?.length ?? rnnHistory?.loss?.length ?? 0,
    qrnnHistory?.train_acc?.length ?? qrnnHistory?.accuracy?.length ?? 0,
    qrnnHistory?.val_acc?.length ?? 0,
    qrnnHistory?.train_loss?.length ?? qrnnHistory?.loss?.length ?? 0
  );

  return Array.from({ length: epochs }, (_, index) => ({
    epoch: index + 1,
    rnn_loss:
      rnnHistory?.val_loss?.[index] ??
      rnnHistory?.train_loss?.[index] ??
      rnnHistory?.loss?.[index] ??
      null,
    qrnn_loss:
      qrnnHistory?.val_loss?.[index] ??
      qrnnHistory?.train_loss?.[index] ??
      qrnnHistory?.loss?.[index] ??
      null,
    rnn_acc:
      rnnHistory?.val_acc?.[index] ??
      rnnHistory?.train_acc?.[index] ??
      rnnHistory?.accuracy?.[index] ??
      null,
    qrnn_acc:
      qrnnHistory?.val_acc?.[index] ??
      qrnnHistory?.train_acc?.[index] ??
      qrnnHistory?.accuracy?.[index] ??
      null,
  }));
};

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="glass rounded-xl p-3 border border-quantum-purple/20">
      <p className="font-mono text-xs text-text-muted mb-1">Epoch {label}</p>
      {payload.map((p: any) => (
        <p key={p.name} className="font-mono text-xs" style={{ color: p.stroke || p.fill }}>
          {p.name}: {typeof p.value === 'number' ? p.value.toFixed(4) : p.value}
        </p>
      ))}
    </div>
  );
};

export default function VisualizationStep({ trainingResults }: VisualizationStepProps) {
  const [activeTab, setActiveTab] = useState<'curves' | 'export'>('curves');
  const [comment, setComment] = useState('');
  const [commentLoading, setCommentLoading] = useState(false);
  const [commentStatus, setCommentStatus] = useState<{ type: 'success' | 'error'; text: string } | null>(
    null
  );
  const [isSignedIn, setIsSignedIn] = useState(false);
  const [authChecked, setAuthChecked] = useState(false);

  const learningCurveData = useMemo(() => buildLearningData(trainingResults), [trainingResults]);
  const rnnHistory = getHistory(trainingResults.rnn);
  const qrnnHistory = getHistory(getQrnnMain(trainingResults.qrnn));

  const hasCurves = learningCurveData.length > 0;
  const hasRnnCurves = Boolean(rnnHistory);
  const hasQrnnCurves = Boolean(qrnnHistory);
  const jobId = trainingResults.job_id;
  const datasetName = trainingResults.dataset_name || 'Unknown Dataset';

  const tabs = [
    { id: 'curves', label: 'Learning Curves' },
    { id: 'export', label: 'Export Report' },
  ] as const;

  useEffect(() => {
    let isMounted = true;

    supabase.auth.getUser().then(({ data, error }) => {
      if (!isMounted) return;
      setIsSignedIn(Boolean(data.user && !error));
      setAuthChecked(true);
    });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleSubmitComment = async () => {
    if (!comment.trim() || !isSignedIn || commentLoading) return;

    setCommentLoading(true);
    setCommentStatus(null);

    try {
      await submitUserComment(comment);
      setComment('');
      setCommentStatus({ type: 'success', text: 'Comment submitted successfully.' });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Unable to submit your comment right now.';
      setCommentStatus({ type: 'error', text: message });
    } finally {
      setCommentLoading(false);
    }
  };

  const isCommentDisabled = !comment.trim() || !isSignedIn || commentLoading;

  return (
    <div className="max-w-7xl">
      <div className="mb-8">
        <h2 className="mb-3 font-mono text-4xl font-black tracking-tight text-white">
          Visualization & Export
        </h2>
        <p className="max-w-2xl text-sm text-slate-400">
          Visualize backend curves when available and export the completed job.
        </p>
      </div>

      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-2">
        {[
          ['Dataset', datasetName],
          ['Job ID', jobId || '-'],
        ].map(([label, value]) => (
          <div key={label} className="glass rounded-xl border border-quantum-purple/10 p-4">
            <div className="mb-2 font-mono text-[10px] uppercase tracking-wider text-text-muted">
              {label}
            </div>
            <div className="break-words font-mono text-sm font-bold text-text-primary">
              {value}
            </div>
          </div>
        ))}
      </div>

      <div className="mb-10 flex gap-2 rounded-3xl border border-white/10 bg-[#071126] p-2 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`relative flex-1 rounded-2xl px-5 py-3 font-mono text-xs font-bold tracking-wide transition-all duration-300 whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-gradient-to-r from-violet-500 to-cyan-400 text-white shadow-[0_0_25px_rgba(139,92,246,0.35)]'
                : 'text-slate-500 hover:bg-white/[0.03] hover:text-slate-300'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'curves' && (
        <div className="space-y-6">
          {hasCurves ? (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <div className="glass rounded-2xl p-6 border border-quantum-purple/10">
                <h3 className="font-mono font-bold text-sm text-text-primary mb-6">
                  Accuracy Curves
                </h3>
                <ResponsiveContainer width="100%" height={320}>
                  <AreaChart data={learningCurveData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="epoch" stroke="#64748B" />
                    <YAxis domain={[0, 1]} stroke="#64748B" />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    {hasRnnCurves && (
                      <Area
                        type="monotone"
                        dataKey="rnn_acc"
                        stroke="#A78BFA"
                        fill="#A78BFA"
                        fillOpacity={0.16}
                        strokeWidth={3}
                        name="RNN Accuracy"
                      />
                    )}
                    {hasQrnnCurves && (
                      <Area
                        type="monotone"
                        dataKey="qrnn_acc"
                        stroke="#06B6D4"
                        fill="#06B6D4"
                        fillOpacity={0.16}
                        strokeWidth={3}
                        name="QNN Accuracy"
                      />
                    )}
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="glass rounded-2xl p-6 border border-quantum-purple/10">
                <h3 className="font-mono font-bold text-sm text-text-primary mb-6">Loss Curves</h3>
                <ResponsiveContainer width="100%" height={320}>
                  <AreaChart data={learningCurveData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="epoch" stroke="#64748B" />
                    <YAxis stroke="#64748B" />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    {hasRnnCurves && (
                      <Area
                        type="monotone"
                        dataKey="rnn_loss"
                        stroke="#A78BFA"
                        fill="#A78BFA"
                        fillOpacity={0.16}
                        strokeWidth={3}
                        name="RNN Loss"
                      />
                    )}
                    {hasQrnnCurves && (
                      <Area
                        type="monotone"
                        dataKey="qrnn_loss"
                        stroke="#06B6D4"
                        fill="#06B6D4"
                        fillOpacity={0.16}
                        strokeWidth={3}
                        name="QNN Loss"
                      />
                    )}
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          ) : (
            <div className="glass rounded-2xl p-8 border border-quantum-purple/10 text-center">
              <p className="font-mono text-sm text-text-primary">
                No history curves were returned by the backend.
              </p>
              <p className="font-mono text-xs text-text-muted mt-2">
                Metrics and exports are still available for this job.
              </p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'export' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass rounded-2xl p-8 border border-quantum-purple/20 text-center">
              <h3 className="font-mono font-bold text-lg text-text-primary mb-2">Export JSON</h3>
              <p className="font-sans text-sm text-text-muted mb-6">
                Download the raw backend results for this job.
              </p>
              <button
                onClick={() =>
                  exportResultsAsJson(
                    addFormattedTrainingTimes(trainingResults),
                    `neurospace_${jobId || 'results'}.json`
                  )
                }
                disabled={!Object.keys(trainingResults).length}
                className="btn-quantum w-full py-3 rounded-xl font-mono text-sm font-semibold disabled:opacity-60"
              >
                Export JSON
              </button>
            </div>

            <div className="glass rounded-2xl p-8 border border-quantum-purple/20 text-center">
              <h3 className="font-mono font-bold text-lg text-text-primary mb-2">Export PDF</h3>
              <p className="font-sans text-sm text-text-muted mb-6">
                Open the PDF report generated by FastAPI.
              </p>
              <button
                onClick={() => {
                  if (jobId) window.open(getReportPdfUrl(jobId), '_blank');
                }}
                disabled={!jobId}
                className="btn-outline w-full py-3 rounded-xl font-mono text-sm font-semibold disabled:opacity-60"
              >
                Open PDF
              </button>
            </div>
          </div>

          <div className="glass rounded-2xl p-8 border border-quantum-purple/20">
            <div className="mb-5">
              <h3 className="font-mono font-bold text-lg text-text-primary mb-2">Comments</h3>
              <p className="font-sans text-sm text-text-muted">
                Share feedback about this visualization with the NeuroSpace community.
              </p>
            </div>

            {authChecked && !isSignedIn && (
              <p className="mb-4 rounded-xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-3 font-mono text-xs text-cyan-200">
                Please sign in to submit a comment.
              </p>
            )}

            <textarea
              value={comment}
              onChange={(event) => {
                setComment(event.target.value);
                if (commentStatus) setCommentStatus(null);
              }}
              rows={5}
              placeholder="Write your comment..."
              className="w-full resize-none rounded-2xl border border-white/10 bg-[#071126] px-4 py-4 font-sans text-sm text-text-primary outline-none transition-colors placeholder:text-text-muted focus:border-quantum-cyan/50"
            />

            <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              {commentStatus ? (
                <p
                  className={`font-mono text-xs ${
                    commentStatus.type === 'success' ? 'text-quantum-teal' : 'text-red-300'
                  }`}
                >
                  {commentStatus.text}
                </p>
              ) : (
                <span className="font-mono text-xs text-text-muted">
                  Comments are public and visible on the homepage.
                </span>
              )}

              <button
                onClick={handleSubmitComment}
                disabled={isCommentDisabled}
                className="btn-quantum rounded-xl px-6 py-3 font-mono text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-50"
              >
                {commentLoading ? 'Submitting...' : 'Submit Comment'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
