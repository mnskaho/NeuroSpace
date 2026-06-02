"use client";

import {
  BarChart3,
  CloudCog,
  Download,
  MessageSquareText,
  SlidersHorizontal,
  UploadCloud,
} from "lucide-react";

const features = [
  {
    title: "Dataset Upload",
    desc: "Upload a CSV dataset, validate its structure, preview metadata, and prepare it for the training pipeline.",
    icon: UploadCloud,
    size: "large",
    color: "purple",
    tag: "Data Preparation",
  },
  {
    title: "Model Selection",
    desc: "Choose exactly what to train: Classical RNN / MLP, Quantum QNN, or both for a direct comparison.",
    icon: SlidersHorizontal,
    size: "small",
    color: "cyan",
    tag: "RNN + QNN",
  },
  {
    title: "Complete Evaluation",
    desc: "Review accuracy, precision, recall, F1 score, loss, confusion matrices, and classification reports.",
    icon: BarChart3,
    size: "small",
    color: "teal",
    tag: "Evaluation",
  },
  {
    title: "Colab Training Worker",
    desc: "Run selected models through the FastAPI pipeline and Google Colab worker with live polling from the dashboard.",
    icon: CloudCog,
    size: "large",
    color: "pink",
    tag: "Training Pipeline",
  },
  {
    title: "JSON & PDF Export",
    desc: "Export raw JSON results and a branded PDF report with the platform logo and available evaluation outputs.",
    icon: Download,
    size: "small",
    color: "cyan",
    tag: "Reporting",
  },
  {
    title: "Community Comments",
    desc: "Authenticated users can publish feedback from Visualization, then everyone can read the latest comments on the homepage.",
    icon: MessageSquareText,
    size: "small",
    color: "purple",
    tag: "Collaboration",
  },
];

const colorMap: Record<string, { border: string; bg: string; text: string; glow: string }> = {
  purple: {
    border: "border-quantum-purple/30",
    bg: "bg-quantum-purple/10",
    text: "text-quantum-violet",
    glow: "hover:shadow-glow-purple",
  },
  cyan: {
    border: "border-quantum-cyan/30",
    bg: "bg-quantum-cyan/10",
    text: "text-quantum-cyan",
    glow: "hover:shadow-glow-cyan",
  },
  teal: {
    border: "border-quantum-teal/30",
    bg: "bg-quantum-teal/10",
    text: "text-quantum-teal",
    glow: "",
  },
  pink: {
    border: "border-quantum-pink/30",
    bg: "bg-quantum-pink/10",
    text: "text-quantum-pink",
    glow: "",
  },
};

export default function FeaturesSection() {
  return (
    <section id="platform" className="py-32 relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-20">
          <span className="font-mono text-xs text-quantum-cyan tracking-widest uppercase mb-4 block">
            03 // Platform Capabilities
          </span>
          <h2 className="font-mono font-black text-4xl md:text-6xl text-text-primary mb-6">
            Everything you <span className="gradient-text">need.</span>
          </h2>
          <p className="font-sans text-text-secondary text-lg max-w-2xl mx-auto">
            From dataset upload to model selection, live training, evaluation, export, and
            community feedback.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {features.map((feature) => {
            const colors = colorMap[feature.color];
            const isLarge = feature.size === "large";
            const Icon = feature.icon;

            return (
              <div
                key={feature.title}
                className={`glass metric-card rounded-2xl p-8 border ${colors.border} ${
                  colors.glow
                } transition-all duration-300 ${isLarge ? "md:col-span-2" : ""}`}
              >
                <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${colors.bg} mb-6`}>
                  <span className={`font-mono text-[10px] ${colors.text} tracking-widest uppercase`}>
                    {feature.tag}
                  </span>
                </div>
                <div
                  className={`mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border ${colors.border} ${colors.bg} ${colors.text}`}
                >
                  <Icon className="h-7 w-7" strokeWidth={1.8} />
                </div>
                <h3 className="font-mono font-bold text-xl text-text-primary mb-3">
                  {feature.title}
                </h3>
                <p className="font-sans text-text-secondary leading-relaxed">{feature.desc}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
