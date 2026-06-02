"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import AppLogo from "@/components/ui/AppLogo";
import Icon from "@/components/ui/AppIcon";
import { createClient } from "@supabase/supabase-js";

// Supabase client
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type StepId = "upload" | "model" | "training" | "evaluation" | "visualization";

interface SidebarProps {
  activeStep: StepId;
  onStepChange: (step: StepId) => void;
  completedSteps: StepId[];
}

const steps: { id: StepId; label: string; icon: string; desc: string }[] = [
  { id: "upload", label: "Dataset Upload", icon: "ArrowUpTrayIcon", desc: "Import & preprocess" },
  { id: "model", label: "Model Config", icon: "CpuChipIcon", desc: "RNN / QNN setup" },
  { id: "training", label: "Training", icon: "BoltIcon", desc: "Parallel execution" },
  { id: "evaluation", label: "Evaluation", icon: "ChartBarIcon", desc: "Metrics & benchmarks" },
  { id: "visualization", label: "Visualization", icon: "PresentationChartLineIcon", desc: "Charts & export" },
];

export default function Sidebar({ activeStep, onStepChange, completedSteps }: SidebarProps) {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const { data: { user }, error } = await supabase.auth.getUser();
      if (!error) setUser(user);
    };
    fetchUser();
  }, []);

  return (
    <aside className="w-64 flex-shrink-0 bg-panel border-r border-quantum-purple/10 flex flex-col h-screen sticky top-0">
      {/* Logo */}
      <div className="p-6 border-b border-quantum-purple/10">
        <Link href="/homepage" className="flex items-center gap-3">
          <AppLogo size={48} />
          <div>
            <div className="font-mono font-bold text-base text-text-primary leading-none">
               <span
      className="text-xl font-bold tracking-tight"
      style={{ fontFamily: "Manrope, sans-serif" }}
    >
      Neuro
      <span className="gradient-text-violet font-display italic font-semibold">
        Space
      </span>
    </span>
            </div>
            <div className="font-mono text-[10px] text-text-muted tracking-widest">v2.1.0</div>
          </div>
        </Link>
      </div>

      {/* Pipeline steps */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="font-mono text-[10px] text-text-muted uppercase tracking-widest px-3 mb-4">
          Research Pipeline
        </div>
        <nav className="flex flex-col gap-1">
          {steps.map((step, i) => {
            const isActive = activeStep === step.id;
            const isCompleted = completedSteps.includes(step.id);
            return (
              <button
                key={step.id}
                onClick={() => onStepChange(step.id)}
                className={`sidebar-item w-full flex items-center gap-3 px-3 py-3 rounded-xl text-left transition-all duration-200 ${isActive ? "active" : ""}`}
              >
                {/* Step indicator */}
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 font-mono text-xs font-bold transition-all ${
                  isCompleted
                    ? "bg-quantum-teal/20 text-quantum-teal border border-quantum-teal/30"
                    : isActive
                    ? "bg-gradient-quantum text-white" :"bg-panel-2 text-text-muted border border-quantum-purple/10"
                }`}>
                  {isCompleted ? "✓" : String(i + 1).padStart(2, "0")}
                </div>
                <div className="flex flex-col min-w-0">
                  <span className={`font-mono text-xs font-semibold truncate ${isActive ? "text-text-primary" : "text-text-secondary"}`}>
                    {step.label}
                  </span>
                  <span className="font-mono text-[10px] text-text-muted truncate">{step.desc}</span>
                </div>
              </button>
            );
          })}
        </nav>

        {/* Progress */}
        <div className="mt-6 px-3">
          <div className="flex justify-between items-center mb-2">
            <span className="font-mono text-[10px] text-text-muted uppercase tracking-widest">Pipeline</span>
            <span className="font-mono text-[10px] text-quantum-cyan">{completedSteps.length}/{steps.length}</span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${(completedSteps.length / steps.length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Bottom - Dynamic User Info (Name only) */}
      {user && (
        <div className="p-4 border-t border-quantum-purple/10">
          <div className="glass rounded-xl p-3 mb-3 flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-quantum flex items-center justify-center font-mono font-bold text-white text-xs flex-shrink-0">
              {user.user_metadata?.name?.[0]?.toUpperCase() || "U"}
            </div>
            <div className="min-w-0">
              <div className="font-mono text-xs text-text-primary truncate font-semibold">
                {user.user_metadata?.name || "User"}
              </div>
            </div>
          </div>
          <Link href="/homepage" className="flex items-center gap-2 px-3 py-2 rounded-xl text-text-muted hover:text-text-secondary font-mono text-xs transition-colors">
            <Icon name="ArrowLeftIcon" size={14} />
            Back to Home
          </Link>
        </div>
      )}
    </aside>
  );
}