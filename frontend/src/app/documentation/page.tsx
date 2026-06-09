"use client";

import {
  BarChart2,
  BookOpen,
  CheckCircle2,
  Cpu,
  CreditCard,
  Database,
  Download,
  FileText,
  GitCompareArrows,
  Home,
  Layers,
  Settings2,
  ShieldCheck,
  Upload,
  Zap,
} from "lucide-react";
import Link from "next/link";

const quickStart = [
  "Sign in and open the Dashboard.",
  "Upload a numeric CSV dataset with a target column.",
  "Choose RNN, QNN, or both models for training.",
  "Configure epochs, batch sizes, and QNN options when needed.",
  "Start training, then review Evaluation and Visualization.",
  "Export the results as JSON or as a PDF report.",
];

const sections = [
  {
    id: "overview",
    icon: BookOpen,
    title: "Overview",
    content: [
      "NeuroSpace is a research platform for training and comparing classical RNN models and quantum QNN models on the same dataset.",
      "The workflow is guided from dataset upload to model selection, FastAPI and Colab-powered training, evaluation, visualization, and report export.",
      "You can train RNN only, QNN only, or RNN + QNN. Full comparison views are shown only when both model results are available.",
    ],
  },
  {
    id: "dataset",
    icon: Upload,
    title: "Dataset Upload",
    content: [
      "The dashboard accepts a numeric CSV file. The backend validates the file and detects dataset dimensions, target column, class count, and recommended qubit count.",
      "Your dataset should contain usable feature columns and one target column for classification. Non-numeric or irrelevant columns should be prepared before upload when necessary.",
      "After upload, NeuroSpace displays a summary with filename, rows, columns, target, classes, and recommended qubits.",
    ],
  },
  {
    id: "model-selection",
    icon: Cpu,
    title: "Model Selection",
    content: [
      "In Model Config, no model is enabled by default. You must select at least one model before continuing.",
      "Classical RNN / MLP trains the classical baseline with its own epochs and batch size.",
      "Quantum QNN trains the quantum model with its own epochs, batch size, quantum backend, and noise options.",
      "If only one model is selected, only that model's settings are displayed and sent to the backend. If both are selected, both configuration sections are shown.",
    ],
  },
  {
    id: "rnn-config",
    icon: Layers,
    title: "RNN Configuration",
    content: [
      "The classical RNN is the baseline model. It can be trained alone or alongside QNN for direct comparison.",
      "Visible settings when RNN is selected: rnn_epochs and rnn_batch_size.",
      "Depending on the comparison mode, features can be prepared with PCA or MI to keep the experiment protocol consistent.",
    ],
  },
  {
    id: "qrnn-config",
    icon: Zap,
    title: "QNN Configuration",
    content: [
      "QNN uses a configurable quantum backend. The current payload supports PennyLane and Qiskit modes.",
      "Visible settings when QNN is selected: qrnn_epochs, qrnn_batch_size, qrnn_backend, noise_enabled, noise_level, mitigation_enabled, and mitigation_runs.",
      "In Ideal mode, training runs without simulated noise. In Noisy mode, you can set a noise level and optionally enable mitigation to test QNN robustness.",
    ],
  },
  {
    id: "training",
    icon: Settings2,
    title: "Training Pipeline",
    content: [
      "TrainingStep builds a conditional payload. RNN only sends model_types: ['rnn']; QNN only sends model_types: ['qrnn']; both sends ['rnn', 'qrnn'].",
      "The FastAPI backend creates a job, prepares the package, and the Colab worker trains only the requested models.",
      "The frontend polls job status until completion or failure. Polling behavior remains the same whether one or two models are trained.",
    ],
  },
  {
    id: "evaluation",
    icon: BarChart2,
    title: "Evaluation",
    content: [
      "Evaluation displays metrics returned by the backend: accuracy, precision, recall, F1 score, loss, confusion matrix, and classification report.",
      "If only RNN is available, only the RNN section is shown. If only QNN is available, NeuroSpace displays QNN clean, noisy, or mitigated blocks depending on the returned results.",
      "The Best Model card and RNN vs QNN comparison table appear only when both models exist in the result JSON.",
    ],
  },
  {
    id: "visualization",
    icon: GitCompareArrows,
    title: "Visualization & Curves",
    content: [
      "Visualization renders accuracy and loss curves from the training history returned by the backend.",
      "Curves are conditional: RNN appears only when results.rnn.history exists; QNN appears only when a QNN block contains history.",
      "This step helps inspect convergence, train-validation gaps, and model stability.",
    ],
  },
  {
    id: "exports",
    icon: Download,
    title: "JSON and PDF Exports",
    content: [
      "Export JSON downloads the raw backend result. The file contains only what the job produced: rnn, qrnn, comparison, config_used, history, and related metrics.",
      "Export PDF opens a FastAPI-generated report with the NeuroSpace logo, configuration, metrics, matrices, classification reports, and learning curves.",
      "The PDF supports RNN-only, QNN-only, and RNN + QNN runs. It does not assume both models exist.",
    ],
  },
  {
    id: "billing",
    icon: CreditCard,
    title: "Payment, Invoices, and Profile",
    content: [
      "The Payment page lets users choose a Free, Pro, or Pro+ plan, then select Credit Card, Dahabia, or PayPal as the payment method.",
      "After payment, Payment Success shows the confirmation, invoice, plan, amount, method, date, and transaction ID.",
      "Billing lists payment history and opens invoices. Profile and settings remain available from the dashboard.",
    ],
  },
  {
    id: "security",
    icon: ShieldCheck,
    title: "Accounts and Security",
    content: [
      "Authentication is handled with Supabase. Profile, payment, dashboard, and billing pages load data for the signed-in user.",
      "Exports and training runs are tied to backend jobs and result files. Job, polling, and upload errors are surfaced in the interface.",
      "For reproducible experiments, prepare your datasets carefully, verify the target column before upload, and keep exported JSON files for later review.",
    ],
  },
];

const payloadExamples = [
  {
    title: "RNN only",
    code: `{
  "model_types": ["rnn"],
  "comparison_mode": "pca",
  "feature_selector": "pca",
  "rnn_epochs": 20,
  "rnn_batch_size": 32
}`,
  },
  {
    title: "QNN only",
    code: `{
  "model_types": ["qrnn"],
  "comparison_mode": "mi",
  "feature_selector": "mi",
  "qrnn_epochs": 10,
  "qrnn_batch_size": 16,
  "qrnn_backend": "pennylane",
  "noise_enabled": false
}`,
  },
  {
    title: "RNN + QNN",
    code: `{
  "model_types": ["rnn", "qrnn"],
  "comparison_mode": "pca",
  "feature_selector": "pca",
  "rnn_epochs": 20,
  "rnn_batch_size": 32,
  "qrnn_epochs": 10,
  "qrnn_batch_size": 16,
  "qrnn_backend": "qiskit"
}`,
  },
];

export default function DocsPage() {
  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-16 relative">
      <Link
        href="/homepage"
        className="absolute left-6 top-6 flex items-center gap-2 text-quantum-purple transition-colors hover:text-quantum-violet"
      >
        <Home className="h-6 w-6" />
      </Link>

      <div className="text-center">
        <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-xl border border-quantum-cyan/30 bg-quantum-cyan/10">
          <FileText className="h-7 w-7 text-quantum-cyan" />
        </div>
        <h1 className="mb-4 font-mono text-4xl font-black text-text-primary md:text-5xl">
          NeuroSpace Documentation
        </h1>
        <p className="mx-auto max-w-3xl text-sm text-text-secondary md:text-base">
          A complete guide to the NeuroSpace workflow: datasets, RNN/QNN model selection,
          training, evaluation, visualization, exports, payments, and invoices.
        </p>
      </div>

      <div className="glass rounded-2xl border border-quantum-purple/10 p-6">
        <div className="mb-5 flex items-center gap-3">
          <div className="rounded-lg bg-quantum-purple/10 p-2">
            <CheckCircle2 className="h-5 w-5 text-quantum-violet" />
          </div>
          <h2 className="font-mono text-lg font-bold text-text-primary">Quick Start</h2>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {quickStart.map((step, index) => (
            <div
              key={step}
              className="flex items-start gap-3 rounded-xl border border-quantum-purple/10 bg-panel/50 p-4"
            >
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-quantum-cyan/10 font-mono text-xs font-bold text-quantum-cyan">
                {index + 1}
              </span>
              <p className="text-sm text-text-secondary">{step}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-wrap justify-center gap-3">
        {sections.map((section) => (
          <a
            key={section.id}
            href={`#${section.id}`}
            className="rounded-lg border border-quantum-purple/30 px-4 py-2 font-mono text-xs text-text-muted transition-colors hover:bg-quantum-purple/10 hover:text-text-primary"
          >
            <section.icon className="mr-1 inline-block h-4 w-4" />
            {section.title}
          </a>
        ))}
      </div>

      <div className="grid gap-6">
        {sections.map((section) => (
          <section
            key={section.id}
            id={section.id}
            className="glass-cyan rounded-2xl border border-quantum-cyan/20 p-7 shadow-card"
          >
            <div className="mb-5 flex items-center gap-4">
              <div className="rounded-lg bg-quantum-purple/10 p-3">
                <section.icon className="h-6 w-6 text-quantum-purple" />
              </div>
              <h2 className="font-mono text-lg font-bold text-text-primary md:text-xl">
                {section.title}
              </h2>
            </div>
            <div className="space-y-3">
              {section.content.map((paragraph) => (
                <p key={paragraph} className="text-sm leading-6 text-text-secondary md:text-base">
                  {paragraph}
                </p>
              ))}
            </div>
          </section>
        ))}
      </div>

      <section className="glass rounded-2xl border border-quantum-purple/10 p-7">
        <div className="mb-5 flex items-center gap-4">
          <div className="rounded-lg bg-quantum-cyan/10 p-3">
            <Database className="h-6 w-6 text-quantum-cyan" />
          </div>
          <h2 className="font-mono text-lg font-bold text-text-primary md:text-xl">
            Payloads Sent to the Backend
          </h2>
        </div>
        <p className="mb-6 text-sm text-text-secondary">
          The frontend sends only the fields required by the selected model setup. These examples
          reflect the current Dashboard logic.
        </p>
        <div className="grid gap-4 lg:grid-cols-3">
          {payloadExamples.map((example) => (
            <div key={example.title} className="rounded-xl border border-quantum-purple/10 bg-panel p-4">
              <h3 className="mb-3 font-mono text-sm font-bold text-text-primary">
                {example.title}
              </h3>
              <pre className="overflow-x-auto rounded-lg bg-space/80 p-4 text-xs leading-5 text-text-secondary">
                <code>{example.code}</code>
              </pre>
            </div>
          ))}
        </div>
      </section>

      <section className="glass rounded-2xl border border-quantum-cyan/20 p-7">
        <h2 className="mb-4 font-mono text-lg font-bold text-text-primary">Best Practices</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {[
            "Start with RNN only to validate the dataset and establish a fast baseline.",
            "Use QNN only to test quantum parameters without running the classical baseline.",
            "Run RNN + QNN when you need a complete comparison and exportable report.",
          ].map((tip) => (
            <div key={tip} className="rounded-xl border border-quantum-cyan/10 bg-panel/60 p-4">
              <p className="text-sm leading-6 text-text-secondary">{tip}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
