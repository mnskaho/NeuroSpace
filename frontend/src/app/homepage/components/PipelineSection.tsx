"use client";

import { useEffect, useRef, useState } from "react";

const steps = [
  {
    num: "01",
    title: "Upload Dataset",
    desc: "Upload a CSV dataset, validate its structure, and preview rows, columns, target classes, and recommended settings.",
    icon: "UP",
    tag: "Dataset Intake",
    color: "purple",
  },
  {
    num: "02",
    title: "Configure Model",
    desc: "Select RNN, QNN, or both, then tune each model with its own epochs, batch size, backend, noise, and mitigation options.",
    icon: "CFG",
    tag: "Model Setup",
    color: "cyan",
  },
  {
    num: "03",
    title: "Run Training",
    desc: "Send the selected configuration to the FastAPI backend and Google Colab worker, then follow live progress from the dashboard.",
    icon: "RUN",
    tag: "Execution",
    color: "teal",
  },
  {
    num: "04",
    title: "Evaluate & Compare",
    desc: "Review accuracy, precision, recall, F1 score, loss, confusion matrices, and classification reports for trained models.",
    icon: "EV",
    tag: "Metrics",
    color: "purple",
  },
  {
    num: "05",
    title: "Visualize & Export",
    desc: "Inspect learning curves, export JSON or branded PDF reports, and publish authenticated comments for the community homepage.",
    icon: "OUT",
    tag: "Results",
    color: "cyan",
  },
];

export default function PipelineSection() {
  const [activeStep, setActiveStep] = useState(0);
  const sectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % steps?.length);
    }, 2500);
    return () => clearInterval(timer);
  }, []);

  return (
    <section id="pipeline" className="py-32 relative overflow-hidden" ref={sectionRef}>
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute left-0 top-1/2 -translate-y-1/2 w-64 h-64 rounded-full"
          style={{
            background:
              "radial-gradient(circle, rgba(124,58,237,0.08) 0%, transparent 70%)",
          }}
        />
      </div>
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-20 max-w-2xl">
          <span className="font-mono text-xs text-quantum-purple tracking-widest uppercase mb-4 block">
            02 // Research Pipeline
          </span>
          <h2 className="font-mono font-black text-4xl md:text-6xl text-text-primary leading-tight mb-6">
            From dataset to <span className="gradient-text">complete evaluation</span>
          </h2>
          <p className="font-sans text-text-secondary text-lg leading-relaxed">
            A guided 5-step workflow for training RNN and QNN models, comparing results, and
            exporting reports.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4 relative">
          <div
            className="hidden lg:block absolute top-10 left-0 right-0 h-px"
            style={{
              background:
                "linear-gradient(90deg, transparent, rgba(124,58,237,0.3), rgba(6,182,212,0.3), rgba(16,207,170,0.3), transparent)",
            }}
          />

          {steps?.map((step, i) => (
            <button
              key={step?.num}
              onClick={() => setActiveStep(i)}
              className={`pipeline-step relative p-6 rounded-2xl text-left transition-all duration-500 ${
                activeStep === i
                  ? "glass-cyan border-quantum-cyan/40 shadow-glow-cyan"
                  : "glass border-quantum-purple/10 hover:border-quantum-purple/30"
              }`}
            >
              <div
                className={`step-icon w-12 h-12 rounded-xl flex items-center justify-center mb-5 font-mono font-bold text-xs transition-all duration-300 ${
                  activeStep === i
                    ? "bg-gradient-quantum text-white shadow-glow-cyan"
                    : "bg-panel text-text-muted border border-quantum-purple/20"
                }`}
              >
                {step?.icon}
              </div>

              <div className="mb-2">
                <span
                  className={`font-mono text-[10px] tracking-widest uppercase ${
                    step?.color === "cyan"
                      ? "text-quantum-cyan"
                      : step?.color === "teal"
                        ? "text-quantum-teal"
                        : "text-quantum-violet"
                  }`}
                >
                  {step?.tag}
                </span>
              </div>
              <h3 className="font-mono font-bold text-sm text-text-primary mb-3 leading-tight">
                {step?.title}
              </h3>
              <p className="font-sans text-xs text-text-muted leading-relaxed">{step?.desc}</p>

              {activeStep === i && (
                <div
                  className="absolute bottom-0 left-0 right-0 h-0.5 rounded-b-2xl"
                  style={{ background: "linear-gradient(90deg, #7C3AED, #06B6D4)" }}
                />
              )}
            </button>
          ))}
        </div>

        <div className="mt-8 glass rounded-2xl p-6 flex items-center gap-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-quantum flex items-center justify-center font-mono font-bold text-white text-xs flex-shrink-0">
            {steps?.[activeStep]?.icon}
          </div>
          <div>
            <div className="font-mono font-bold text-text-primary mb-1">
              Step {steps?.[activeStep]?.num}: {steps?.[activeStep]?.title}
            </div>
            <div className="font-sans text-sm text-text-secondary">
              {steps?.[activeStep]?.desc}
            </div>
          </div>
          <div className="ml-auto flex gap-2">
            {steps?.map((_, i) => (
              <button
                key={i}
                onClick={() => setActiveStep(i)}
                className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  i === activeStep ? "bg-quantum-cyan w-6" : "bg-panel-2"
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
