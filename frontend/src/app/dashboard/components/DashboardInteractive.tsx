// "use client";

// import { useState } from "react";
// import Sidebar from "./Sidebar";
// import UploadStep from "./UploadStep";
// import ModelStep from "./ModelStep";
// import TrainingStep from "./TrainingStep";
// import EvaluationStep from "./EvaluationStep";
// import VisualizationStep from "./VisualizationStep";
// import Icon from "@/components/ui/AppIcon";

// type StepId = "upload" | "model" | "training" | "evaluation" | "visualization";

// const stepOrder: StepId[] = ["upload", "model", "training", "evaluation", "visualization"];

// export default function DashboardInteractive() {
//   const [activeStep, setActiveStep] = useState<StepId>("upload");
//   const [completedSteps, setCompletedSteps] = useState<StepId[]>([]);
//   const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

//   const handleStepComplete = () => {
//     const currentIndex = stepOrder.indexOf(activeStep);
//     if (!completedSteps.includes(activeStep)) {
//       setCompletedSteps((prev) => [...prev, activeStep]);
//     }
//     if (currentIndex < stepOrder.length - 1) {
//       setActiveStep(stepOrder[currentIndex + 1]);
//     }
//   };

//   const handleStepChange = (step: StepId) => {
//     setActiveStep(step);
//     setMobileSidebarOpen(false);
//   };

//   const stepComponents: Record<StepId, React.ReactNode> = {
//     upload: <UploadStep onComplete={handleStepComplete} />,
//     model: <ModelStep onComplete={handleStepComplete} />,
//     training: <TrainingStep onComplete={handleStepComplete} />,
//     evaluation: <EvaluationStep onComplete={handleStepComplete} />,
//     visualization: <VisualizationStep />,
//   };

//   return (
//     <div className="flex h-screen bg-space overflow-hidden">
//       {/* Desktop Sidebar */}
//       <div className="hidden lg:block">
//         <Sidebar
//           activeStep={activeStep}
//           onStepChange={handleStepChange}
//           completedSteps={completedSteps}
//         />
//       </div>

//       {/* Mobile sidebar overlay */}
//       {mobileSidebarOpen && (
//         <div className="lg:hidden fixed inset-0 z-50 flex">
//           <div className="w-64 flex-shrink-0">
//             <Sidebar
//               activeStep={activeStep}
//               onStepChange={handleStepChange}
//               completedSteps={completedSteps}
//             />
//           </div>
//           <div
//             className="flex-1 bg-black/60 backdrop-blur-sm"
//             onClick={() => setMobileSidebarOpen(false)}
//           />
//         </div>
//       )}

//       {/* Main content area */}
//       <div className="flex-1 flex flex-col overflow-hidden">
//         {/* Top bar */}
//         <div className="flex items-center justify-between px-6 py-4 border-b border-quantum-purple/10 bg-panel/50 backdrop-blur-sm flex-shrink-0">
//           <div className="flex items-center gap-4">
//             {/* Mobile menu toggle */}
//             <button
//               className="lg:hidden p-2 text-text-muted hover:text-text-primary transition-colors"
//               onClick={() => setMobileSidebarOpen(true)}
//               aria-label="Open sidebar"
//             >
//               <Icon name="Bars3Icon" size={20} />
//             </button>

//             {/* Breadcrumb */}
//             <div className="flex items-center gap-2 font-mono text-xs text-text-muted">
//               <span>NeuroSpace</span>
//               <span>/</span>
//               <span className="text-quantum-cyan capitalize">{activeStep}</span>
//             </div>
//           </div>

//           {/* Top-right actions */}
//           <div className="flex items-center gap-3">
//             {/* Status indicator */}
//             <div className="hidden md:flex items-center gap-2 glass px-3 py-1.5 rounded-lg">
//               <span className="w-2 h-2 rounded-full bg-quantum-teal animate-pulse" />
//               <span className="font-mono text-[10px] text-quantum-teal tracking-wider">
//                 {completedSteps.length}/{stepOrder.length} Complete
//               </span>
//             </div>

//             {/* New experiment */}
//             <button
//               onClick={() => {
//                 setActiveStep("upload");
//                 setCompletedSteps([]);
//               }}
//               className="btn-outline px-4 py-2 rounded-lg font-mono text-xs"
//             >
//               + New Experiment
//             </button>
//           </div>
//         </div>

//         {/* Step content */}
//         <div className="flex-1 overflow-y-auto p-6 lg:p-8">
//           {stepComponents[activeStep]}
//         </div>
//       </div>
//     </div>
//   );
// }

'use client';

import { useCallback, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from './Sidebar';
import UploadStep from './UploadStep';
import ModelStep from './ModelStep';
import TrainingStep from './TrainingStep';
import EvaluationStep from './EvaluationStep';
import VisualizationStep from './VisualizationStep';
import Icon from '@/components/ui/AppIcon';
import { createClient } from '@supabase/supabase-js';
import type {
  DatasetMeta,
  ModelConfig,
  PipelineStep,
  TrainingResults,
} from '@/app/dashboard/components/types';

// Supabase client
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type StepId = PipelineStep;
const stepOrder: StepId[] = ['upload', 'model', 'training', 'evaluation', 'visualization'];

type TrainingUsage = {
  plan: 'free' | 'pro' | 'pro_plus';
  used: number;
  limit: number;
};

// ------------------- Profile Menu -------------------
function ProfileMenu() {
  const [user, setUser] = useState<any>(null);
  const [open, setOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      setUser(user);
    };
    fetchUser();
  }, []);

  const logout = async () => {
    await supabase.auth.signOut();
    router.push('/sign-up-login');
  };

  if (!user) return null;

  return (
    <div className="relative">
      {/* Avatar */}
      <button
        onClick={() => setOpen(!open)}
        className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-bold hover:scale-105 transition"
      >
        {user.user_metadata?.name?.[0]?.toUpperCase() || user.email?.[0].toUpperCase()}
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute right-0 mt-2 w-52 bg-panel rounded-xl shadow-lg py-2 flex flex-col z-50 border border-panel/20">
          <div className="px-4 py-3 border-b border-panel/20">
            <p className="text-sm font-semibold">{user.user_metadata?.name || 'User'}</p>
            <p className="text-xs text-text-muted">{user.email}</p>
          </div>

          <button
            onClick={() => router.push('/profile')}
            className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-panel-2 transition-colors"
          >
            <Icon name="UserIcon" size={16} />
            Profile
          </button>

          <button
            onClick={() => router.push('/payment')}
            className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-panel-2 transition-colors"
          >
            <Icon name="CreditCardIcon" size={16} />
            Payment
          </button>

          <button
            onClick={() => router.push('/settings')}
            className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-panel-2 transition-colors"
          >
            <Icon name="Cog6ToothIcon" size={16} />
            Settings
          </button>

          <button
            onClick={() => router.push('/help')}
            className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-panel-2 transition-colors"
          >
            <Icon name="QuestionMarkCircleIcon" size={16} />
            Help
          </button>

          <button
            onClick={logout}
            className="flex items-center gap-3 px-4 py-2 text-sm text-red-500 hover:bg-panel-2 transition-colors"
          >
            <Icon name="ArrowRightOnRectangleIcon" size={16} />
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

// ------------------- Dashboard -------------------
const defaultModelConfig: ModelConfig = {
  selectedRNN: false,
  selectedQRNN: false,
  comparisonMode: 'pca',
  featureSelector: 'pca',
  backend: 'PennyLane',
  encoding: 'Ideal',
  noiseLevel: 0.01,
  mitigationEnabled: false,
  mitigationRuns: 10,
  rnnBatchSize: 32,
  qrnnBatchSize: 16,
  rnnEpochs: 20,
  qrnnEpochs: 20,
};

export default function DashboardInteractive() {
  const [activeStep, setActiveStep] = useState<StepId>('upload');
  const [completedSteps, setCompletedSteps] = useState<StepId[]>([]);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [datasetMeta, setDatasetMeta] = useState<DatasetMeta | null>(null);
  const [modelConfig, setModelConfig] = useState<ModelConfig>(defaultModelConfig);
  const [trainingResults, setTrainingResults] = useState<TrainingResults>({});
  const [trainingUsage, setTrainingUsage] = useState<TrainingUsage>({
    plan: 'free',
    used: 0,
    limit: 1,
  });

  const loadTrainingUsage = useCallback(async () => {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session?.access_token) {
      setTrainingUsage({ plan: 'free', used: 0, limit: 1 });
      return;
    }

    const response = await fetch('/api/user/training-usage', {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    });

    if (!response.ok) return;

    const usage = (await response.json()) as TrainingUsage;
    setTrainingUsage(usage);
  }, []);

  // ✅ Nettoyer l'URL après login pour enlever tous les tokens
  useEffect(() => {
    if (window.location.hash.includes('access_token')) {
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  useEffect(() => {
    loadTrainingUsage();
  }, [loadTrainingUsage]);

  useEffect(() => {
    if (activeStep === 'evaluation' || activeStep === 'visualization') {
      loadTrainingUsage();
    }
  }, [activeStep, loadTrainingUsage]);

  const handleStepComplete = () => {
    const currentIndex = stepOrder.indexOf(activeStep);
    if (!completedSteps.includes(activeStep)) {
      setCompletedSteps((prev) => [...prev, activeStep]);
    }
    if (currentIndex < stepOrder.length - 1) {
      setActiveStep(stepOrder[currentIndex + 1]);
    }
  };

  const handleStepChange = (step: StepId) => {
    setActiveStep(step);
    setMobileSidebarOpen(false);
  };

  const stepComponents: Record<StepId, React.ReactNode> = {
    upload: (
      <UploadStep
        onComplete={(metadata) => {
          setDatasetMeta(metadata);
          setTrainingResults({});
          handleStepComplete();
        }}
      />
    ),
    model: (
      <ModelStep
        modelConfig={modelConfig}
        onConfigChange={setModelConfig}
        onComplete={handleStepComplete}
      />
    ),
    training: (
      <TrainingStep
        datasetMeta={datasetMeta}
        modelConfig={modelConfig}
        onTrainingComplete={setTrainingResults}
        onTrainingUsageChanged={loadTrainingUsage}
        onComplete={handleStepComplete}
      />
    ),
    evaluation: (
      <EvaluationStep trainingResults={trainingResults} onComplete={handleStepComplete} />
    ),
    visualization: <VisualizationStep trainingResults={trainingResults} />,
  };

  return (
    <div className="flex h-screen bg-space overflow-hidden">
      {/* Desktop Sidebar */}
      <div className="hidden lg:block">
        <Sidebar
          activeStep={activeStep}
          onStepChange={handleStepChange}
          completedSteps={completedSteps}
        />
      </div>

      {/* Mobile sidebar overlay */}
      {mobileSidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          <div className="w-64 flex-shrink-0">
            <Sidebar
              activeStep={activeStep}
              onStepChange={handleStepChange}
              completedSteps={completedSteps}
            />
          </div>
          <div
            className="flex-1 bg-black/60 backdrop-blur-sm"
            onClick={() => setMobileSidebarOpen(false)}
          />
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-quantum-purple/10 bg-panel/50 backdrop-blur-sm flex-shrink-0">
          <div className="flex items-center gap-4">
            <button
              className="lg:hidden p-2 text-text-muted hover:text-text-primary transition-colors"
              onClick={() => setMobileSidebarOpen(true)}
              aria-label="Open sidebar"
            >
              <Icon name="Bars3Icon" size={20} />
            </button>

            <div className="flex items-center gap-2 font-mono text-xs text-text-muted">
              <span>NeuroSpace</span>
              <span>/</span>
              <span className="text-quantum-cyan capitalize">{activeStep}</span>
            </div>
          </div>

          {/* Top-right actions */}
          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 glass px-3 py-1.5 rounded-lg">
              <span className="w-2 h-2 rounded-full bg-quantum-teal animate-pulse" />
              <span className="font-mono text-[10px] text-quantum-teal tracking-wider">
                {Math.min(trainingUsage.used, trainingUsage.limit)}/{trainingUsage.limit} Trainings
              </span>
            </div>

            <div className="flex items-center gap-10"></div>

            {/* Profile */}
            <ProfileMenu />
          </div>
        </div>

        {/* Step content */}
        <div className="flex-1 overflow-y-auto p-6 lg:p-8">{stepComponents[activeStep]}</div>
      </div>
    </div>
  );
}
