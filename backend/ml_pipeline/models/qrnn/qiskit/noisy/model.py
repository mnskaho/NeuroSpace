# import numpy as np
# import torch
# import torch.nn as nn
# from qiskit import QuantumCircuit, transpile
# from qiskit_aer import AerSimulator
# from qiskit.circuit import Parameter
# from qiskit.quantum_info import SparsePauliOp
# from qiskit_aer.noise import NoiseModel, depolarizing_error

# class QiskitQRNN(nn.Module):
#     """
#     QRNN Qiskit NOISY - Bruit Depolarizing sur les gates uniquement
#     """
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001,
#                  noise_level=0.0, mitigation_runs=1):
#         super().__init__()
       
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.noise_level = noise_level
#         self.mitigation_runs = max(1, mitigation_runs)

#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
       
#         self.fc = nn.Linear(n_qubits, num_classes)
#         self.criterion = nn.CrossEntropyLoss()

#         if noise_level > 0.0:
#             noise_model = NoiseModel()
#             error = depolarizing_error(noise_level, 1)
#             noise_model.add_all_qubit_quantum_error(error, ['ry', 'rz', 'rx'])
#             self.backend = AerSimulator(noise_model=noise_model, method='density_matrix')
#             self.use_density = True
#             print(f"⚠️ [NOISY] Qiskit - Bruit Depolarizing p={noise_level} | Mitigation runs={self.mitigation_runs}")
#         else:
#             self.backend = AerSimulator(method='statevector')
#             self.use_density = False
#             print(f"✅ Qiskit - Sans bruit (Statevector)")

#         self.circuit = self._build_circuit()
#         self.transpiled_template = transpile(self.circuit, self.backend, optimization_level=1)

#         self.pauli_z_ops = []
#         for q in range(self.n_qubits):
#             pauli_str = 'I' * (self.n_qubits - q - 1) + 'Z' + 'I' * q
#             self.pauli_z_ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))

#     def _build_circuit(self):
#         qc = QuantumCircuit(self.n_qubits)
#         self.param_names = []
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]

#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)

#         param_idx = 0
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             for q in range(self.n_qubits - 1):
#                 qc.cx(q, q + 1)
#             qc.cx(self.n_qubits - 1, 0)

#         if not self.use_density:
#             qc.save_statevector()
#         return qc

#     def _get_parameter_values(self, x, weights):
#         param_values = {self.input_names[i]: float(x[i]) for i in range(self.n_qubits)}
#         for idx, name in enumerate(self.param_names):
#             param_values[name] = float(weights[idx])
#         return param_values

#     def forward(self, x, quantum_weights=None):
#         batch_size = x.shape[0]
#         device = x.device

#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")

#         weights = quantum_weights if quantum_weights is not None else self.quantum_weights.detach().cpu().numpy()

#         if self.noise_level > 0.0 and self.mitigation_runs > 1:
#             all_q_out = []
#             for _ in range(self.mitigation_runs):
#                 q_out_run = self._run_single_forward(x, weights)
#                 all_q_out.append(q_out_run)
#             q_out = torch.mean(torch.stack(all_q_out), dim=0)
#         else:
#             q_out = self._run_single_forward(x, weights)

#         return self.fc(q_out)

#     def _run_single_forward(self, x, weights):
#         batch_size = x.shape[0]
#         device = x.device
#         circuits_to_run = []

#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             param_values = self._get_parameter_values(x_i, weights)
#             bound = self.transpiled_template.assign_parameters(param_values)
#             circuits_to_run.append(bound)

#         result = self.backend.run(circuits_to_run).result()

#         q_out = []
#         for i in range(batch_size):
#             if self.use_density:
#                 dm = result.data(i)['density_matrix']
#                 expvals = [float(dm.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
#             else:
#                 try:
#                     sv = result.get_statevector(i)
#                 except:
#                     sv = result.data(i)['statevector']
#                 expvals = [float(sv.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
#             q_out.append(expvals)

#         return torch.tensor(np.array(q_out, dtype=np.float32), device=device)

#     def get_quantum_weights_numpy(self):
#         return self.quantum_weights.detach().cpu().numpy()

#     def set_quantum_weights_numpy(self, weights):
#         self.quantum_weights.data = torch.tensor(weights, dtype=torch.float32)

#     def predict(self, X):
#         self.eval()
#         X = torch.FloatTensor(X)
#         with torch.no_grad():
#             outputs = self(X)
#             _, predicted = torch.max(outputs, 1)
#         return predicted.numpy()

#     def predict_proba(self, X):
#         self.eval()
#         X = torch.FloatTensor(X)
#         with torch.no_grad():
#             outputs = self(X)
#             probabilities = torch.softmax(outputs, dim=1)
#         return probabilities.numpy()


# def create_qiskit_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1):
#     return QiskitQRNN(n_qubits, n_layers, num_classes, noise_level=noise_level, mitigation_runs=mitigation_runs)

#•________________________________________________________________________________________________________________________

#GROK VERSION MISMATCH CPU AND GPU 
# import numpy as np
# import torch
# import torch.nn as nn
# from qiskit import QuantumCircuit, transpile
# from qiskit_aer import AerSimulator
# from qiskit.circuit import Parameter
# from qiskit.quantum_info import SparsePauliOp
# from qiskit_aer.noise import NoiseModel, depolarizing_error

# class QiskitQRNN(nn.Module):
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001,
#                  noise_level=0.0, mitigation_runs=1):
#         super().__init__()
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.noise_level = noise_level
#         self.mitigation_runs = max(1, mitigation_runs)

#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))

#         self.fc = nn.Linear(n_qubits, num_classes)

#         if noise_level > 0.0:
#             noise_model = NoiseModel()
#             error = depolarizing_error(noise_level, 1)
#             noise_model.add_all_qubit_quantum_error(error, ['ry', 'rz', 'rx'])
#             self.backend = AerSimulator(noise_model=noise_model, method='density_matrix')
#             self.use_density = True
#             print(f"⚠️ [NOISY] Qiskit - Bruit Depolarizing p={noise_level} | Mitigation={self.mitigation_runs}")
#         else:
#             self.backend = AerSimulator(method='statevector')
#             self.use_density = False
#             print(f"✅ Qiskit - Statevector (no noise)")

#         self.circuit = self._build_circuit()
#         self.transpiled_template = transpile(self.circuit, self.backend, optimization_level=1)

#         self.pauli_z_ops = []
#         for q in range(self.n_qubits):
#             pauli_str = 'I' * (self.n_qubits - q - 1) + 'Z' + 'I' * q
#             self.pauli_z_ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))

#     def _build_circuit(self):
#         qc = QuantumCircuit(self.n_qubits)
#         self.param_names = []
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]

#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)

#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             for q in range(self.n_qubits - 1):
#                 qc.cx(q, q + 1)
#             qc.cx(self.n_qubits - 1, 0)

#         if not self.use_density:
#             qc.save_statevector()
#         else:
#             qc.save_density_matrix()   # ← FIX IMPORTANT

#         return qc

#     def _get_parameter_values(self, x, weights):
#         param_values = {self.input_names[i]: float(x[i]) for i in range(self.n_qubits)}
#         for idx, name in enumerate(self.param_names):
#             param_values[name] = float(weights[idx])
#         return param_values

#     def forward(self, x, quantum_weights=None):
#         batch_size = x.shape[0]
#         device = x.device

#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")

#         weights = quantum_weights if quantum_weights is not None else self.quantum_weights.detach().cpu().numpy()

#         if self.noise_level > 0.0 and self.mitigation_runs > 1:
#             all_q_out = []
#             for _ in range(self.mitigation_runs):
#                 q_out_run = self._run_single_forward(x, weights)
#                 all_q_out.append(q_out_run)
#             q_out = torch.mean(torch.stack(all_q_out), dim=0)
#         else:
#             q_out = self._run_single_forward(x, weights)

#         return self.fc(q_out.to(device))

#     def _run_single_forward(self, x, weights):
#         batch_size = x.shape[0]
#         circuits_to_run = []

#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             param_values = self._get_parameter_values(x_i, weights)
#             bound = self.transpiled_template.assign_parameters(param_values)
#             circuits_to_run.append(bound)

#         result = self.backend.run(circuits_to_run).result()

#         q_out = []
#         for i in range(batch_size):
#             if self.use_density:
#                 dm = result.data(i)['density_matrix']
#                 expvals = [float(dm.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
#             else:
#                 sv = result.get_statevector(i)
#                 expvals = [float(sv.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
#             q_out.append(expvals)

#         return torch.tensor(np.array(q_out, dtype=np.float32), device='cpu')  # Qiskit retourne toujours sur CPU

#     # ... (get_quantum_weights_numpy, set_quantum_weights_numpy, predict, predict_proba restent identiques)
#     def get_quantum_weights_numpy(self):
#         return self.quantum_weights.detach().cpu().numpy()

#     def set_quantum_weights_numpy(self, weights):
#         self.quantum_weights.data = torch.tensor(weights, dtype=torch.float32)

#     def predict(self, X):
#         self.eval()
#         X = torch.FloatTensor(X)
#         with torch.no_grad():
#             outputs = self(X)
#             _, predicted = torch.max(outputs, 1)
#         return predicted.numpy()

#     def predict_proba(self, X):
#         self.eval()
#         X = torch.FloatTensor(X)
#         with torch.no_grad():
#             outputs = self(X)
#             probabilities = torch.softmax(outputs, dim=1)
#         return probabilities.numpy()


# def create_qiskit_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1):
#     return QiskitQRNN(n_qubits, n_layers, num_classes, noise_level=noise_level, mitigation_runs=mitigation_runs)

#•________________________________________________________________________________________________________________________
#NEW CODE TO FIX CPU RETURN 

# import numpy as np
# import torch
# import torch.nn as nn
# from qiskit import QuantumCircuit, transpile
# from qiskit_aer import AerSimulator
# from qiskit.circuit import Parameter
# from qiskit.quantum_info import SparsePauliOp
# from qiskit_aer.noise import NoiseModel, depolarizing_error

# class QiskitQRNN(nn.Module):
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001,
#                  noise_level=0.0, mitigation_runs=1):
#         super().__init__()
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.noise_level = noise_level
#         self.mitigation_runs = max(1, mitigation_runs)

#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))

#         self.fc = nn.Linear(n_qubits, num_classes)

#         if noise_level > 0.0:
#             noise_model = NoiseModel()
#             error = depolarizing_error(noise_level, 1)
#             noise_model.add_all_qubit_quantum_error(error, ['ry', 'rz', 'rx'])
#             self.backend = AerSimulator(noise_model=noise_model, method='density_matrix')
#             self.use_density = True
#             print(f"⚠️ [NOISY] Qiskit - Bruit Depolarizing p={noise_level} | Mitigation={self.mitigation_runs}")
#         else:
#             self.backend = AerSimulator(method='statevector')
#             self.use_density = False
#             print(f"✅ Qiskit - Statevector (no noise)")

#         self.circuit = self._build_circuit()
#         self.transpiled_template = transpile(self.circuit, self.backend, optimization_level=1)

#         self.pauli_z_ops = []
#         for q in range(self.n_qubits):
#             pauli_str = 'I' * (self.n_qubits - q - 1) + 'Z' + 'I' * q
#             self.pauli_z_ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))

#     def _build_circuit(self):
#         qc = QuantumCircuit(self.n_qubits)
#         self.param_names = []
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]

#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)

#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             for q in range(self.n_qubits - 1):
#                 qc.cx(q, q + 1)
#             qc.cx(self.n_qubits - 1, 0)

#         if not self.use_density:
#             qc.save_statevector()
#         else:
#             qc.save_density_matrix()

#         return qc

#     def _get_parameter_values(self, x, weights):
#         param_values = {self.input_names[i]: float(x[i]) for i in range(self.n_qubits)}
#         for idx, name in enumerate(self.param_names):
#             param_values[name] = float(weights[idx])
#         return param_values

#     def forward(self, x, quantum_weights=None):
#         batch_size = x.shape[0]
#         device = x.device

#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")

#         weights = quantum_weights if quantum_weights is not None else self.quantum_weights.detach().cpu().numpy()

#         if self.noise_level > 0.0 and self.mitigation_runs > 1:
#             all_q_out = []
#             for _ in range(self.mitigation_runs):
#                 q_out_run = self._run_single_forward(x, weights)
#                 all_q_out.append(q_out_run)
#             q_out = torch.mean(torch.stack(all_q_out), dim=0)
#         else:
#             q_out = self._run_single_forward(x, weights)

#         # 🔥 FIX : Forcer q_out sur le même device que fc
#         q_out = q_out.to(device)
#         return self.fc(q_out)

#     def _run_single_forward(self, x, weights):
#         batch_size = x.shape[0]
#         circuits_to_run = []

#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             param_values = self._get_parameter_values(x_i, weights)
#             bound = self.transpiled_template.assign_parameters(param_values)
#             circuits_to_run.append(bound)

#         result = self.backend.run(circuits_to_run).result()

#         q_out = []
#         for i in range(batch_size):
#             if self.use_density:
#                 dm = result.data(i)['density_matrix']
#                 expvals = [float(dm.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
#             else:
#                 sv = result.get_statevector(i)
#                 expvals = [float(sv.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
#             q_out.append(expvals)

#         # Retourne toujours sur CPU (Qiskit fait ça)
#         return torch.tensor(np.array(q_out, dtype=np.float32), device='cpu')

#     def get_quantum_weights_numpy(self):
#         return self.quantum_weights.detach().cpu().numpy()

#     def set_quantum_weights_numpy(self, weights):
#         self.quantum_weights.data = torch.tensor(weights, dtype=torch.float32)

#     def predict(self, X):
#         self.eval()
#         X = torch.FloatTensor(X).to(self.fc.weight.device)
#         with torch.no_grad():
#             outputs = self(X)
#             _, predicted = torch.max(outputs, 1)
#         return predicted.cpu().numpy()

#     def predict_proba(self, X):
#         self.eval()
#         X = torch.FloatTensor(X).to(self.fc.weight.device)
#         with torch.no_grad():
#             outputs = self(X)
#             probabilities = torch.softmax(outputs, dim=1)
#         return probabilities.cpu().numpy()


# def create_qiskit_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1):
#     return QiskitQRNN(n_qubits, n_layers, num_classes, noise_level=noise_level, mitigation_runs=mitigation_runs)

#NEW CODE WITH FLEXIBILITY___________________________________________________________________________________________________________________________________#

import numpy as np
import torch
import torch.nn as nn
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.noise import NoiseModel, depolarizing_error
from ml_pipeline.adaptive_config import AdaptiveConfig

class QiskitQRNN(nn.Module):
    """
    QRNN Qiskit NOISY - Adaptatif
    Règle : None = auto-calculé par AdaptiveConfig
    """
    def __init__(self, n_qubits, n_layers=None, num_classes=2, learning_rate=None,
                 noise_level=0.0, mitigation_runs=1, dataset_info=None):
        super().__init__()
        
        if dataset_info and (n_layers is None or learning_rate is None):
            n_samples = dataset_info.get('samples', 1000)
            n_features = dataset_info.get('features', n_qubits * 4)
            n_classes = dataset_info.get('classes', num_classes)
            
            adaptive = AdaptiveConfig.compute_qrnn_params(n_qubits, n_samples, n_classes)
            
            if n_layers is None:
                n_layers = adaptive['n_layers']
            if learning_rate is None:
                learning_rate = adaptive['learning_rate']
            
            self.epochs = adaptive['epochs']
            self.fc_epochs = max(20, min(50, self.epochs // 2))
            
            print(f"📊 Qiskit Noisy Adaptatif [{n_samples} samples, {n_features} features, "
                  f"{n_classes} classes]: qubits={n_qubits}, layers={n_layers}, "
                  f"lr={learning_rate:.5f}, SPSA={self.epochs}, FC={self.fc_epochs}")
        else:
            self.epochs = 20
            self.fc_epochs = 20
        
        self.n_qubits = n_qubits
        self.n_layers = n_layers if n_layers is not None else 3
        self.num_classes = num_classes
        self.learning_rate = learning_rate if learning_rate is not None else 0.001
        self.noise_level = noise_level
        self.mitigation_runs = max(1, mitigation_runs)
        self.n_quantum_params = self.n_layers * n_qubits * 3
        self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
        self.fc = nn.Linear(n_qubits, num_classes)

        if noise_level > 0.0:
            noise_model = NoiseModel()
            error = depolarizing_error(noise_level, 1)
            noise_model.add_all_qubit_quantum_error(error, ['ry', 'rz', 'rx'])
            self.backend = AerSimulator(noise_model=noise_model, method='density_matrix')
            self.use_density = True
            print(f"⚠️ [NOISY] Qiskit - Bruit Depolarizing p={noise_level} | Mitigation={self.mitigation_runs}")
        else:
            self.backend = AerSimulator(method='statevector')
            self.use_density = False
            print(f"✅ Qiskit - Statevector (no noise)")

        self.circuit = self._build_circuit()
        self.transpiled_template = transpile(self.circuit, self.backend, optimization_level=1)
        self.pauli_z_ops = []
        for q in range(self.n_qubits):
            pauli_str = 'I' * (self.n_qubits - q - 1) + 'Z' + 'I' * q
            self.pauli_z_ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))

    def _build_circuit(self):
        qc = QuantumCircuit(self.n_qubits)
        self.param_names = []
        self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]
        for i in range(self.n_qubits):
            qc.ry(self.input_names[i], i)
        for layer in range(self.n_layers):
            for qubit in range(self.n_qubits):
                p1 = Parameter(f'θ_{layer}_{qubit}_0')
                p2 = Parameter(f'θ_{layer}_{qubit}_1')
                p3 = Parameter(f'θ_{layer}_{qubit}_2')
                self.param_names.extend([p1, p2, p3])
                qc.ry(p1, qubit)
                qc.rz(p2, qubit)
                qc.ry(p3, qubit)
            for q in range(self.n_qubits - 1):
                qc.cx(q, q + 1)
            qc.cx(self.n_qubits - 1, 0)
        qc.save_statevector() if not self.use_density else qc.save_density_matrix()
        self._param_order = list(self.input_names) + list(self.param_names)
        return qc

    def _get_parameter_values(self, x, weights):
        return dict(zip(self._param_order, np.concatenate([x, weights])))

    def forward(self, x, quantum_weights=None):
        batch_size = x.shape[0]
        device = x.device
        if x.shape[1] != self.n_qubits:
            raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")
        weights = quantum_weights if quantum_weights is not None else self.quantum_weights.detach().cpu().numpy()
        if self.noise_level > 0.0 and self.mitigation_runs > 1:
            all_q_out = []
            for _ in range(self.mitigation_runs):
                all_q_out.append(self._run_single_forward(x, weights))
            q_out = torch.mean(torch.stack(all_q_out), dim=0)
        else:
            q_out = self._run_single_forward(x, weights)
        return self.fc(q_out.to(device))

    def _run_single_forward(self, x, weights):
        circuits_to_run = []
        for i in range(x.shape[0]):
            x_i = x[i].detach().cpu().numpy()
            bound = self.transpiled_template.assign_parameters(
                self._get_parameter_values(x_i, weights)
            )
            circuits_to_run.append(bound)
        result = self.backend.run(circuits_to_run).result()
        q_out = []
        for i in range(x.shape[0]):
            if self.use_density:
                dm = result.data(i)['density_matrix']
                expvals = [float(dm.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
            else:
                sv = result.get_statevector(i)
                expvals = [float(sv.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
            q_out.append(expvals)
        return torch.tensor(np.array(q_out, dtype=np.float32), device='cpu')

    def get_quantum_weights_numpy(self):
        return self.quantum_weights.detach().cpu().numpy()

    def set_quantum_weights_numpy(self, weights):
        self.quantum_weights.data = torch.tensor(weights, dtype=torch.float32)

    def predict(self, X):
        self.eval()
        X = torch.FloatTensor(X).to(self.fc.weight.device)
        with torch.no_grad():
            _, predicted = torch.max(self(X), 1)
        return predicted.cpu().numpy()

    def predict_proba(self, X):
        self.eval()
        X = torch.FloatTensor(X).to(self.fc.weight.device)
        with torch.no_grad():
            return torch.softmax(self(X), dim=1).cpu().numpy()


def create_qiskit_qrnn_model(n_qubits, num_classes=2, n_layers=None, learning_rate=None,
                              noise_level=0.0, mitigation_runs=1, dataset_info=None):
    return QiskitQRNN(
        n_qubits=n_qubits,
        n_layers=n_layers,
        num_classes=num_classes,
        learning_rate=learning_rate,
        noise_level=noise_level,
        mitigation_runs=mitigation_runs,
        dataset_info=dataset_info
    )