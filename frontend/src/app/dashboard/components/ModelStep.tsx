// 'use client';

// import { useMemo } from 'react';

// import type { ModelConfig } from '@/app/dashboard/components/types';

// interface ModelStepProps {
//   modelConfig: ModelConfig;
//   onConfigChange: (config: ModelConfig) => void;
//   onComplete: () => void;
// }

// const noiseLevels = [0.001, 0.002, 0.005, 0.008, 0.01];
// const mitigationRuns = [3, 5, 10, 20, 30, 50];
// const batchSizes = [8, 16, 32, 64, 128];

// export default function ModelStep({ modelConfig, onConfigChange, onComplete }: ModelStepProps) {
//   const canContinue = modelConfig.selectedRNN || modelConfig.selectedQRNN;

//   const selectedModels = useMemo(() => {
//     const list: string[] = [];
//     if (modelConfig.selectedRNN) list.push('Classical RNN / MLP');
//     if (modelConfig.selectedQRNN) list.push('Quantum QNN');
//     return list.join(' + ') || 'No model selected';
//   }, [modelConfig]);

//   const update = (patch: Partial<ModelConfig>) => {
//     onConfigChange({ ...modelConfig, ...patch });
//   };

//   return (
//     <div className="max-w-5xl">
//       <div className="mb-8">
//         <h2 className="font-mono font-black text-2xl text-text-primary mb-2">
//           Model Configuration
//         </h2>
//         <p className="font-sans text-text-secondary text-sm">
//           Configure the backend payload for classical RNN and quantum QNN.
//         </p>
//       </div>

//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
//         <div
//           className={`glass rounded-2xl p-6 border transition-all ${
//             modelConfig.selectedRNN
//               ? 'border-quantum-purple/40'
//               : 'border-quantum-purple/10 opacity-70'
//           }`}
//         >
//           <div className="flex items-center gap-3 mb-6">
//             <div className="w-10 h-10 rounded-xl bg-quantum-purple/10 border border-quantum-purple/20 flex items-center justify-center text-quantum-violet font-mono font-bold">
//               C
//             </div>
//             <div>
//               <div className="font-mono font-bold text-sm text-text-primary">
//                 Classical RNN / MLP
//               </div>
//               <div className="font-mono text-[10px] text-text-muted">
//                 Baseline recurrent neural network
//               </div>
//             </div>
//           </div>

//           <button
//             type="button"
//             onClick={() => update({ selectedRNN: !modelConfig.selectedRNN })}
//             className={`w-full rounded-xl border p-4 text-left transition-all ${
//               modelConfig.selectedRNN
//                 ? 'border-quantum-purple/50 bg-quantum-purple/10'
//                 : 'border-quantum-purple/10 bg-panel/50 hover:border-quantum-purple/30'
//             }`}
//           >
//             <div className="flex items-center gap-3">
//               <div
//                 className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
//                   modelConfig.selectedRNN ? 'border-quantum-violet' : 'border-text-muted'
//                 }`}
//               >
//                 {modelConfig.selectedRNN && (
//                   <div className="w-2 h-2 rounded-full bg-quantum-violet" />
//                 )}
//               </div>
//               <div>
//                 <div className="font-mono text-sm font-semibold text-text-primary">
//                   Enable classical RNN
//                 </div>
//                 <div className="font-mono text-[10px] text-text-muted">
//                   Uses PCA in PCA mode, MI in MI mode
//                 </div>
//               </div>
//             </div>
//           </button>
//         </div>

//         <div
//           className={`glass rounded-2xl p-6 border transition-all ${
//             modelConfig.selectedQRNN
//               ? 'border-quantum-cyan/40'
//               : 'border-quantum-cyan/10 opacity-70'
//           }`}
//         >
//           <div className="flex items-center gap-3 mb-6">
//             <div className="w-10 h-10 rounded-xl bg-quantum-cyan/10 border border-quantum-cyan/20 flex items-center justify-center text-quantum-cyan font-mono font-bold">
//               Q
//             </div>
//             <div>
//               <div className="font-mono font-bold text-sm text-text-primary">
//                 Quantum QNN
//               </div>
//               <div className="font-mono text-[10px] text-text-muted">
//                 MI + Thumb Rule feature sizing
//               </div>
//             </div>
//           </div>

//           <button
//             type="button"
//             onClick={() => update({ selectedQRNN: !modelConfig.selectedQRNN })}
//             className={`w-full rounded-xl border p-4 text-left transition-all ${
//               modelConfig.selectedQRNN
//                 ? 'border-quantum-cyan/50 bg-quantum-cyan/10'
//                 : 'border-quantum-cyan/10 bg-panel/50 hover:border-quantum-cyan/25'
//             }`}
//           >
//             <div className="font-mono text-sm font-semibold text-text-primary">
//               Enable quantum QNN
//             </div>
//           </button>
//         </div>
//       </div>

//       {!canContinue && (
//         <div className="mb-8 rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4">
//           <p className="font-mono text-sm text-amber-200">
//            Please select at least one model to train.
//           </p>
//         </div>
//       )}

//       {canContinue && (
//       <div className="glass rounded-2xl p-6 mb-8 border border-quantum-purple/10 space-y-6">
//         <div>
//           <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//             Comparison Mode
//           </label>
//           <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
//             {[
//               ['pca', 'PCA Mode', 'RNN -> PCA | QNN -> MI + Thumb Rule'],
//               ['mi', 'MI Mode', 'RNN -> MI | QNN -> MI + Thumb Rule'],
//             ].map(([value, title, description]) => (
//               <button
//                 key={value}
//                 type="button"
//                 onClick={() =>
//                   update({
//                     comparisonMode: value as 'pca' | 'mi',
//                     featureSelector: value as 'pca' | 'mi',
//                   })
//                 }
//                 className={`rounded-xl border p-4 text-left transition-all ${
//                   modelConfig.comparisonMode === value
//                     ? 'border-quantum-cyan/50 bg-quantum-cyan/10'
//                     : 'border-quantum-purple/15 text-text-muted hover:border-quantum-purple/30'
//                 }`}
//               >
//                 <div className="font-mono text-sm font-semibold text-text-primary">{title}</div>
//                 <div className="font-mono text-[10px] text-text-muted mt-1">{description}</div>
//               </button>
//             ))}
//           </div>
//         </div>

//         {modelConfig.selectedQRNN && (
//         <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//           <div>
//             <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//               Quantum Framework
//             </label>
//             <div className="grid grid-cols-2 gap-2">
//               {[
//                 ['PennyLane', 'Gradient backpropagation'],
//                 ['Qiskit', 'SPSA optimization'],
//               ].map(([backend, description]) => (
//                 <button
//                   key={backend}
//                   type="button"
//                   onClick={() => update({ backend: backend as 'PennyLane' | 'Qiskit' })}
//                   className={`py-3 px-3 rounded-lg font-mono text-xs border transition-all ${
//                     modelConfig.backend === backend
//                       ? 'border-quantum-cyan/50 bg-quantum-cyan/10 text-quantum-cyan'
//                       : 'border-quantum-purple/15 text-text-muted hover:border-quantum-purple/30'
//                   }`}
//                 >
//                   <span className="block font-semibold">{backend}</span>
//                   <span className="block mt-1 text-[10px]">{description}</span>
//                 </button>
//               ))}
//             </div>
//           </div>

//           <div>
//             <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//               Simulation Noise
//             </label>
//             <div className="grid grid-cols-2 gap-2">
//               {(['Ideal', 'Noisy'] as const).map((encoding) => (
//                 <button
//                   key={encoding}
//                   type="button"
//                   onClick={() => update({ encoding })}
//                   className={`py-3 px-3 rounded-lg font-mono text-xs border transition-all ${
//                     modelConfig.encoding === encoding
//                       ? 'border-quantum-cyan/50 bg-quantum-cyan/10 text-quantum-cyan'
//                       : 'border-quantum-purple/15 text-text-muted hover:border-quantum-purple/30'
//                   }`}
//                 >
//                   {encoding}
//                 </button>
//               ))}
//             </div>
//           </div>
//         </div>
//         )}

//         {modelConfig.selectedQRNN && modelConfig.encoding === 'Noisy' && (
//           <div className="grid grid-cols-1 md:grid-cols-3 gap-4 rounded-xl bg-panel/40 border border-quantum-cyan/20 p-4">
//             <div>
//               <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//                 Noise Level
//               </label>
//               <div className="relative">
//                 <input
//                   type="number"
//                   min={0.001}
//                   max={0.01}
//                   step={0.001}
//                   list="noise-level-options"
//                   value={modelConfig.noiseLevel}
//                   onChange={(event) => update({ noiseLevel: Number(event.target.value) })}
//                   className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 pr-10 text-sm text-text-primary"
//                 />
//                 <span className="pointer-events-none absolute right-3 top-1/2 h-2 w-2 -translate-y-1/2 rotate-45 border-b-2 border-r-2 border-text-primary" />
//               </div>
//               <datalist id="noise-level-options">
//                 {noiseLevels.map((level) => (
//                   <option key={level} value={level}>
//                     {level}
//                   </option>
//                 ))}
//               </datalist>
//             </div>

//             <label className="flex items-center gap-3 rounded-xl border border-quantum-purple/15 px-4 py-3 font-mono text-xs text-text-secondary">
//               <input
//                 type="checkbox"
//                 checked={modelConfig.mitigationEnabled}
//                 onChange={(event) => update({ mitigationEnabled: event.target.checked })}
//                 className="accent-quantum-cyan"
//               />
//               Mitigation enabled
//             </label>

//             <div>
//               <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//                 Mitigation Runs
//               </label>
//               <select
//                 value={modelConfig.mitigationRuns}
//                 onChange={(event) => update({ mitigationRuns: Number(event.target.value) })}
//                 disabled={!modelConfig.mitigationEnabled}
//                 className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary disabled:opacity-50"
//               >
//                 {mitigationRuns.map((runs) => (
//                   <option key={runs} value={runs}>
//                     {runs}
//                   </option>
//                 ))}
//               </select>
//             </div>
//           </div>
//         )}

//         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
//           {modelConfig.selectedRNN && (
//           <div>
//             <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//               RNN Epochs
//             </label>
//             <input
//               type="number"
//               min={1}
//               max={1000}
//               value={modelConfig.rnnEpochs}
//               onChange={(event) => update({ rnnEpochs: Number(event.target.value) })}
//               className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
//             />
//           </div>
//           )}

//           {modelConfig.selectedQRNN && (
//           <div>
//             <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//               QNN Epochs
//             </label>
//             <input
//               type="number"
//               min={1}
//               max={1000}
//               value={modelConfig.qrnnEpochs}
//               onChange={(event) => update({ qrnnEpochs: Number(event.target.value) })}
//               className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
//             />
//           </div>
//           )}

//           {modelConfig.selectedRNN && (
//           <div>
//             <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//               RNN Batch Size
//             </label>
//             <select
//               value={modelConfig.rnnBatchSize}
//               onChange={(event) => update({ rnnBatchSize: Number(event.target.value) })}
//               className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
//             >
//               {batchSizes.map((size) => (
//                 <option key={size} value={size}>
//                   {size}
//                 </option>
//               ))}
//             </select>
//           </div>
//           )}

//           {modelConfig.selectedQRNN && (
//           <div>
//             <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//               QNN Batch Size
//             </label>
//             <select
//               value={modelConfig.qrnnBatchSize}
//               onChange={(event) => update({ qrnnBatchSize: Number(event.target.value) })}
//               className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
//             >
//               {batchSizes.map((size) => (
//                 <option key={size} value={size}>
//                   {size}
//                 </option>
//               ))}
//             </select>
//           </div>
//           )}
//         </div>
//       </div>
//       )}

//       <div className="glass rounded-2xl p-6 mb-8 border border-quantum-purple/10">
//         <div className="font-mono text-[10px] text-text-muted uppercase tracking-wider mb-3">
//           Selected Models
//         </div>
//         <div className="font-mono font-bold text-lg text-text-primary">{selectedModels}</div>
//       </div>

//       <button
//         type="button"
//         disabled={!canContinue}
//         onClick={onComplete}
//         className="btn-quantum px-8 py-4 rounded-xl font-mono text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed"
//       >
//         Continue
//       </button>
//     </div>
//   );
// }

'use client';

import { useMemo } from 'react';

import type { ModelConfig } from '@/app/dashboard/components/types';

interface ModelStepProps {
  modelConfig: ModelConfig;
  onConfigChange: (config: ModelConfig) => void;
  onComplete: () => void;
}

const noiseLevels = [
  { label: '0.001', value: 0.001 },
  { label: '0.0025', value: 0.0025 },
  { label: '0.005', value: 0.005 },
  { label: '0.0075', value: 0.0075 },
  { label: '0.01', value: 0.01 },
];
const mitigationRuns = [3, 5, 10, 20, 30, 50];
const batchSizes = [8, 16, 32, 64, 128];

export default function ModelStep({ modelConfig, onConfigChange, onComplete }: ModelStepProps) {
  const canContinue = modelConfig.selectedRNN || modelConfig.selectedQRNN;

  const selectedModels = useMemo(() => {
    const list: string[] = [];
    if (modelConfig.selectedRNN) list.push('Classical RNN / MLP');
    if (modelConfig.selectedQRNN) list.push('Quantum QNN');
    return list.join(' + ') || 'No model selected';
  }, [modelConfig]);

  const update = (patch: Partial<ModelConfig>) => {
    onConfigChange({ ...modelConfig, ...patch });
  };

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h2 className="font-mono font-black text-2xl text-text-primary mb-2">
          Model Configuration
        </h2>
        <p className="font-sans text-text-secondary text-sm">
          Configure the backend payload for classical RNN and quantum QNN.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div
          className={`glass rounded-2xl p-6 border transition-all ${
            modelConfig.selectedRNN
              ? 'border-quantum-purple/40'
              : 'border-quantum-purple/10 opacity-70'
          }`}
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-quantum-purple/10 border border-quantum-purple/20 flex items-center justify-center text-quantum-violet font-mono font-bold">
              C
            </div>
            <div>
              <div className="font-mono font-bold text-sm text-text-primary">
                Classical RNN / MLP
              </div>
              <div className="font-mono text-[10px] text-text-muted">
                Baseline recurrent neural network
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={() => update({ selectedRNN: !modelConfig.selectedRNN })}
            className={`w-full rounded-xl border p-4 text-left transition-all ${
              modelConfig.selectedRNN
                ? 'border-quantum-purple/50 bg-quantum-purple/10'
                : 'border-quantum-purple/10 bg-panel/50 hover:border-quantum-purple/30'
            }`}
          >
            <div className="flex items-center gap-3">
              <div
                className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                  modelConfig.selectedRNN ? 'border-quantum-violet' : 'border-text-muted'
                }`}
              >
                {modelConfig.selectedRNN && (
                  <div className="w-2 h-2 rounded-full bg-quantum-violet" />
                )}
              </div>
              <div>
                <div className="font-mono text-sm font-semibold text-text-primary">
                  Enable classical RNN
                </div>
                <div className="font-mono text-[10px] text-text-muted">
                  Uses PCA in PCA mode, MI in MI mode
                </div>
              </div>
            </div>
          </button>
        </div>

        <div
          className={`glass rounded-2xl p-6 border transition-all ${
            modelConfig.selectedQRNN
              ? 'border-quantum-cyan/40'
              : 'border-quantum-cyan/10 opacity-70'
          }`}
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-quantum-cyan/10 border border-quantum-cyan/20 flex items-center justify-center text-quantum-cyan font-mono font-bold">
              Q
            </div>
            <div>
              <div className="font-mono font-bold text-sm text-text-primary">
                Quantum QNN
              </div>
              <div className="font-mono text-[10px] text-text-muted">
                MI + Thumb Rule feature sizing
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={() => update({ selectedQRNN: !modelConfig.selectedQRNN })}
            className={`w-full rounded-xl border p-4 text-left transition-all ${
              modelConfig.selectedQRNN
                ? 'border-quantum-cyan/50 bg-quantum-cyan/10'
                : 'border-quantum-cyan/10 bg-panel/50 hover:border-quantum-cyan/25'
            }`}
          >
            <div className="font-mono text-sm font-semibold text-text-primary">
              Enable quantum QNN
            </div>
          </button>
        </div>
      </div>

      {!canContinue && (
        <div className="mb-8 rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4">
          <p className="font-mono text-sm text-amber-200">
           Please select at least one model to train.
          </p>
        </div>
      )}

      {canContinue && (
      <div className="glass rounded-2xl p-6 mb-8 border border-quantum-purple/10 space-y-6">
        <div>
          <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
            Comparison Mode
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {[
              ['pca', 'PCA Mode', 'RNN -> PCA | QNN -> MI + Thumb Rule'],
              ['mi', 'MI Mode', 'RNN -> MI | QNN -> MI + Thumb Rule'],
            ].map(([value, title, description]) => (
              <button
                key={value}
                type="button"
                onClick={() =>
                  update({
                    comparisonMode: value as 'pca' | 'mi',
                    featureSelector: value as 'pca' | 'mi',
                  })
                }
                className={`rounded-xl border p-4 text-left transition-all ${
                  modelConfig.comparisonMode === value
                    ? 'border-quantum-cyan/50 bg-quantum-cyan/10'
                    : 'border-quantum-purple/15 text-text-muted hover:border-quantum-purple/30'
                }`}
              >
                <div className="font-mono text-sm font-semibold text-text-primary">{title}</div>
                <div className="font-mono text-[10px] text-text-muted mt-1">{description}</div>
              </button>
            ))}
          </div>
        </div>

        {modelConfig.selectedQRNN && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
              Quantum Framework
            </label>
            <div className="grid grid-cols-2 gap-2">
              {[
                ['PennyLane', 'Gradient backpropagation'],
                ['Qiskit', 'SPSA optimization'],
              ].map(([backend, description]) => (
                <button
                  key={backend}
                  type="button"
                  onClick={() => update({ backend: backend as 'PennyLane' | 'Qiskit' })}
                  className={`py-3 px-3 rounded-lg font-mono text-xs border transition-all ${
                    modelConfig.backend === backend
                      ? 'border-quantum-cyan/50 bg-quantum-cyan/10 text-quantum-cyan'
                      : 'border-quantum-purple/15 text-text-muted hover:border-quantum-purple/30'
                  }`}
                >
                  <span className="block font-semibold">{backend}</span>
                  <span className="block mt-1 text-[10px]">{description}</span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
              Simulation Noise
            </label>
            <div className="grid grid-cols-2 gap-2">
              {(['Ideal', 'Noisy'] as const).map((encoding) => (
                <button
                  key={encoding}
                  type="button"
                  onClick={() => update({ encoding })}
                  className={`py-3 px-3 rounded-lg font-mono text-xs border transition-all ${
                    modelConfig.encoding === encoding
                      ? 'border-quantum-cyan/50 bg-quantum-cyan/10 text-quantum-cyan'
                      : 'border-quantum-purple/15 text-text-muted hover:border-quantum-purple/30'
                  }`}
                >
                  {encoding}
                </button>
              ))}
            </div>
          </div>
        </div>
        )}

        {modelConfig.selectedQRNN && modelConfig.encoding === 'Noisy' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 rounded-xl bg-panel/40 border border-quantum-cyan/20 p-4">
            <div>
              <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
                Noise Level
              </label>
              <select
                value={modelConfig.noiseLevel}
                onChange={(event) => update({ noiseLevel: Number(event.target.value) })}
                className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
              >
                {noiseLevels.map((level) => (
                  <option key={level.value} value={level.value}>
                    {level.label}
                  </option>
                ))}
              </select>
            </div>

            <label className="flex items-center gap-3 rounded-xl border border-quantum-purple/15 px-4 py-3 font-mono text-xs text-text-secondary">
              <input
                type="checkbox"
                checked={modelConfig.mitigationEnabled}
                onChange={(event) => update({ mitigationEnabled: event.target.checked })}
                className="accent-quantum-cyan"
              />
              Mitigation enabled
            </label>

            <div>
              <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
                Mitigation Runs
              </label>
              <select
                value={modelConfig.mitigationRuns}
                onChange={(event) => update({ mitigationRuns: Number(event.target.value) })}
                disabled={!modelConfig.mitigationEnabled}
                className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary disabled:opacity-50"
              >
                {mitigationRuns.map((runs) => (
                  <option key={runs} value={runs}>
                    {runs}
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {modelConfig.selectedRNN && (
          <div>
            <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
              RNN Epochs
            </label>
            <input
              type="number"
              min={1}
              max={1000}
              value={modelConfig.rnnEpochs}
              onChange={(event) => update({ rnnEpochs: Number(event.target.value) })}
              className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
            />
          </div>
          )}

          {modelConfig.selectedQRNN && (
          <div>
            <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
              QNN Epochs
            </label>
            <input
              type="number"
              min={1}
              max={1000}
              value={modelConfig.qrnnEpochs}
              onChange={(event) => update({ qrnnEpochs: Number(event.target.value) })}
              className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
            />
          </div>
          )}

          {modelConfig.selectedRNN && (
          <div>
            <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
              RNN Batch Size
            </label>
            <select
              value={modelConfig.rnnBatchSize}
              onChange={(event) => update({ rnnBatchSize: Number(event.target.value) })}
              className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
            >
              {batchSizes.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </div>
          )}

          {modelConfig.selectedQRNN && (
          <div>
            <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
              QNN Batch Size
            </label>
            <select
              value={modelConfig.qrnnBatchSize}
              onChange={(event) => update({ qrnnBatchSize: Number(event.target.value) })}
              className="w-full rounded-xl border border-panel-2 bg-panel/70 px-3 py-2 text-sm text-text-primary"
            >
              {batchSizes.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </div>
          )}
        </div>
      </div>
      )}

      <div className="glass rounded-2xl p-6 mb-8 border border-quantum-purple/10">
        <div className="font-mono text-[10px] text-text-muted uppercase tracking-wider mb-3">
          Selected Models
        </div>
        <div className="font-mono font-bold text-lg text-text-primary">{selectedModels}</div>
      </div>

      <button
        type="button"
        disabled={!canContinue}
        onClick={onComplete}
        className="btn-quantum px-8 py-4 rounded-xl font-mono text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed"
      >
        Continue
      </button>
    </div>
  );
}
