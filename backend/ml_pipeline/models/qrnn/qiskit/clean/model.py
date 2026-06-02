# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim

# try:
#     from qiskit import QuantumCircuit, transpile
#     from qiskit_aer import AerSimulator
#     from qiskit.circuit import Parameter
#     HAS_QISKIT = True
# except ImportError:
#     HAS_QISKIT = False
#     print("⚠️ Qiskit not installed. Install with: pip install qiskit qiskit-aer")


# class QiskitQRNN(nn.Module):
#     """
#     QRNN avec Qiskit (simulateur Aer)
#     Utilise un circuit paramétré avec des rotations RY et portes CNOT
    
#     IMPORTANT: Les paramètres quantiques sont entraînés avec SPSA (sans gradient)
#     La couche finale classique est entraînée avec PyTorch (avec gradient)
#     """
    
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001, shots=1024):
#         super().__init__()
#         if not HAS_QISKIT:
#             raise ImportError("Qiskit is required. Install with: pip install qiskit qiskit-aer")
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.shots = shots
        
#         # Paramètres quantiques (angles de rotation)
#         # Structure: (n_layers, n_qubits, 3) pour les rotations RY, RZ, RY
#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
        
#         # Couche de sortie classique (entraînée avec PyTorch)
#         self.fc = nn.Linear(n_qubits, num_classes)
        
#         # Optimiseur classique pour la couche FC
#         self.fc_optimizer = None
#         self.criterion = nn.CrossEntropyLoss()
        
#         # Simulateur
#         self.backend = AerSimulator()
        
#         # Construire le circuit quantique
#         self.circuit = self._build_circuit()
        
#         print(f"⚛️ QRNN Qiskit: {n_qubits} qubits, {n_layers} layers")
#         print(f"   Paramètres quantiques: {self.n_quantum_params} (optimisés avec SPSA)")
#         print(f"   Paramètres classiques: {n_qubits * num_classes + num_classes} (optimisés avec Adam)")
    
#     def _build_circuit(self):
#         """Construit le circuit quantique paramétré"""
#         qc = QuantumCircuit(self.n_qubits)
        
#         # Paramètres pour chaque couche
#         self.param_names = []
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 # 3 paramètres par qubit par couche (RY, RZ, RY)
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
        
#         # Entrées (features)
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]
        
#         # Encodage des données (AngleEmbedding-like avec RY)
#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)
        
#         # Couches variationnelles
#         param_idx = 0
#         for layer in range(self.n_layers):
#             # Rotations individuelles
#             for qubit in range(self.n_qubits):
#                 p1 = self.param_names[param_idx]; param_idx += 1
#                 p2 = self.param_names[param_idx]; param_idx += 1
#                 p3 = self.param_names[param_idx]; param_idx += 1
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             # Portes d'intrication (CNOT)
#             for qubit in range(self.n_qubits - 1):
#                 qc.cx(qubit, qubit + 1)
#             qc.cx(self.n_qubits - 1, 0)
        
#         return qc
    
#     def _get_parameter_values(self, x, weights):
#         """
#         Récupère les valeurs des paramètres pour l'exécution du circuit
#         """
#         param_values = {}
        
#         # Valeurs des features (inputs)
#         for i in range(self.n_qubits):
#             param_values[self.input_names[i]] = float(x[i])
        
#         # Valeurs des poids quantiques
#         for idx, param_name in enumerate(self.param_names):
#             param_values[param_name] = float(weights[idx])
        
#         return param_values
    
#     def _run_circuit(self, x, weights):
#         """
#         Exécute le circuit quantique pour un échantillon
#         """
#         param_values = self._get_parameter_values(x, weights)
        
#         # Assigner les paramètres
#         bound_circuit = self.circuit.bind_parameters(param_values)
        
#         # Transpiler et exécuter
#         transpiled = transpile(bound_circuit, self.backend)
#         job = self.backend.run(transpiled, shots=self.shots)
#         result = job.result()
#         counts = result.get_counts()
        
#         # Calculer les valeurs d'espérance
#         expvals = []
#         for qubit in range(self.n_qubits):
#             # Calculer <Z> = (P(0) - P(1)) pour le qubit
#             prob0 = 0
#             prob1 = 0
#             for bitstring, count in counts.items():
#                 # Qiskit donne les bits dans l'ordre inverse
#                 if bitstring[-1 - qubit] == '0':
#                     prob0 += count
#                 else:
#                     prob1 += count
#             total = prob0 + prob1
#             if total > 0:
#                 expval = (prob0 - prob1) / total
#             else:
#                 expval = 0
#             expvals.append(expval)
        
#         return np.array(expvals, dtype=np.float32)
    
#     def forward(self, x, quantum_weights=None):
#         """
#         Forward pass
#         x: tenseur de forme (batch_size, n_qubits)
#         quantum_weights: poids quantiques (optionnel, pour SPSA)
#         """
#         batch_size = x.shape[0]
#         device = x.device
        
#         # Vérification des dimensions
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")
        
#         # Utiliser les poids passés en paramètre ou les poids du modèle
#         if quantum_weights is not None:
#             weights = quantum_weights
#         else:
#             weights = self.quantum_weights.detach().cpu().numpy()
        
#         # Exécution du circuit pour chaque échantillon
#         q_out = []
#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             expvals = self._run_circuit(x_i, weights)
#             q_out.append(expvals)
        
#         q_out = torch.tensor(np.array(q_out), dtype=torch.float32, device=device)
        
#         # Classification
#         out = self.fc(q_out)
#         return out
    
#     def get_quantum_weights_numpy(self):
#         """Retourne les poids quantiques en numpy (pour SPSA)"""
#         return self.quantum_weights.detach().cpu().numpy()
    
#     def set_quantum_weights_numpy(self, weights):
#         """Définit les poids quantiques depuis numpy (pour SPSA)"""
#         self.quantum_weights.data = torch.tensor(weights, dtype=torch.float32)
    
#     def predict(self, X):
#         """Prédit les classes pour X"""
#         self.eval()
#         X = torch.FloatTensor(X)
        
#         with torch.no_grad():
#             outputs = self(X)
#             _, predicted = torch.max(outputs, 1)
        
#         return predicted.numpy()
    
#     def predict_proba(self, X):
#         """Retourne les probabilités pour X"""
#         self.eval()
#         X = torch.FloatTensor(X)
        
#         with torch.no_grad():
#             outputs = self(X)
#             probabilities = torch.softmax(outputs, dim=1)
        
#         return probabilities.numpy()


# def create_qiskit_qrnn_model(n_qubits, num_classes, n_layers=3):
#     """Fonction de création du modèle QRNN Qiskit"""
#     return QiskitQRNN(n_qubits, n_layers, num_classes)

# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim

# try:
#     from qiskit import QuantumCircuit, transpile
#     from qiskit_aer import AerSimulator
#     from qiskit.circuit import Parameter
#     HAS_QISKIT = True
# except ImportError:
#     HAS_QISKIT = False
#     print("⚠️ Qiskit not installed. Install with: pip install qiskit qiskit-aer")


# class QiskitQRNN(nn.Module):
#     """
#     QRNN avec Qiskit (simulateur Aer)
#     Utilise un circuit paramétré avec des rotations RY et portes CNOT
    
#     IMPORTANT: Les paramètres quantiques sont entraînés avec SPSA (sans gradient)
#     La couche finale classique est entraînée avec PyTorch (avec gradient)
#     """
    
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001, shots=1024):
#         super().__init__()
#         if not HAS_QISKIT:
#             raise ImportError("Qiskit is required. Install with: pip install qiskit qiskit-aer")
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.shots = shots
        
#         # Paramètres quantiques (angles de rotation)
#         # Structure: (n_layers, n_qubits, 3) pour les rotations RY, RZ, RY
#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
        
#         # Couche de sortie classique (entraînée avec PyTorch)
#         self.fc = nn.Linear(n_qubits, num_classes)
        
#         # Optimiseur classique pour la couche FC
#         self.fc_optimizer = None
#         self.criterion = nn.CrossEntropyLoss()
        
#         # Simulateur
#         self.backend = AerSimulator()
        
#         # Construire le circuit quantique
#         self.circuit = self._build_circuit()
#         self.param_names = []
#         self.input_names = []
        
#         print(f"⚛️ QRNN Qiskit: {n_qubits} qubits, {n_layers} layers")
#         print(f"   Paramètres quantiques: {self.n_quantum_params} (optimisés avec SPSA)")
#         print(f"   Paramètres classiques: {n_qubits * num_classes + num_classes} (optimisés avec Adam)")
    
#     def _build_circuit(self):
#         """Construit le circuit quantique paramétré"""
#         qc = QuantumCircuit(self.n_qubits)
        
#         # Paramètres pour chaque couche
#         self.param_names = []
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 # 3 paramètres par qubit par couche (RY, RZ, RY)
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
        
#         # Entrées (features)
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]
        
#         # Encodage des données (AngleEmbedding-like avec RY)
#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)
        
#         # Couches variationnelles
#         param_idx = 0
#         for layer in range(self.n_layers):
#             # Rotations individuelles
#             for qubit in range(self.n_qubits):
#                 p1 = self.param_names[param_idx]; param_idx += 1
#                 p2 = self.param_names[param_idx]; param_idx += 1
#                 p3 = self.param_names[param_idx]; param_idx += 1
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             # Portes d'intrication (CNOT)
#             for qubit in range(self.n_qubits - 1):
#                 qc.cx(qubit, qubit + 1)
#             qc.cx(self.n_qubits - 1, 0)
        
#         return qc
    
#     def _get_parameter_values(self, x, weights):
#         """
#         Récupère les valeurs des paramètres pour l'exécution du circuit
#         """
#         param_values = {}
        
#         # Valeurs des features (inputs)
#         for i in range(self.n_qubits):
#             param_values[self.input_names[i]] = float(x[i])
        
#         # Valeurs des poids quantiques
#         for idx, param_name in enumerate(self.param_names):
#             param_values[param_name] = float(weights[idx])
        
#         return param_values
    
#     def _run_circuit(self, x, weights):
#         """
#         Exécute le circuit quantique pour un échantillon
#         """
#         param_values = self._get_parameter_values(x, weights)
        
#         # 🔥 CORRECTION: Utiliser assign_parameters (nouvelle API Qiskit)
#         # La méthode bind_parameters est dépréciée dans les versions récentes
#         try:
#             # Méthode 1: assign_parameters (Qiskit >= 0.45)
#             bound_circuit = self.circuit.assign_parameters(param_values)
#         except AttributeError:
#             try:
#                 # Méthode 2: bind_parameters (ancienne API)
#                 bound_circuit = self.circuit.bind_parameters(param_values)
#             except AttributeError:
#                 # Méthode 3: méthode manuelle avec copy
#                 bound_circuit = self.circuit.copy()
#                 for param, value in param_values.items():
#                     bound_circuit = bound_circuit.assign_parameters({param: value})
        
#         # Transpiler et exécuter
#         transpiled = transpile(bound_circuit, self.backend)
#         job = self.backend.run(transpiled, shots=self.shots)
#         result = job.result()
#         counts = result.get_counts()
        
#         # Calculer les valeurs d'espérance
#         expvals = []
#         for qubit in range(self.n_qubits):
#             # Calculer <Z> = (P(0) - P(1)) pour le qubit
#             prob0 = 0
#             prob1 = 0
#             for bitstring, count in counts.items():
#                 # Qiskit donne les bits dans l'ordre inverse
#                 if len(bitstring) > qubit:
#                     if bitstring[-1 - qubit] == '0':
#                         prob0 += count
#                     else:
#                         prob1 += count
#             total = prob0 + prob1
#             if total > 0:
#                 expval = (prob0 - prob1) / total
#             else:
#                 expval = 0
#             expvals.append(expval)
        
#         return np.array(expvals, dtype=np.float32)
    
#     def forward(self, x, quantum_weights=None):
#         """
#         Forward pass
#         x: tenseur de forme (batch_size, n_qubits)
#         quantum_weights: poids quantiques (optionnel, pour SPSA)
#         """
#         batch_size = x.shape[0]
#         device = x.device
        
#         # Vérification des dimensions
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")
        
#         # Utiliser les poids passés en paramètre ou les poids du modèle
#         if quantum_weights is not None:
#             weights = quantum_weights
#         else:
#             weights = self.quantum_weights.detach().cpu().numpy()
        
#         # Exécution du circuit pour chaque échantillon
#         q_out = []
#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             expvals = self._run_circuit(x_i, weights)
#             q_out.append(expvals)
        
#         q_out = torch.tensor(np.array(q_out), dtype=torch.float32, device=device)
        
#         # Classification
#         out = self.fc(q_out)
#         return out
    
#     def get_quantum_weights_numpy(self):
#         """Retourne les poids quantiques en numpy (pour SPSA)"""
#         return self.quantum_weights.detach().cpu().numpy()
    
#     def set_quantum_weights_numpy(self, weights):
#         """Définit les poids quantiques depuis numpy (pour SPSA)"""
#         self.quantum_weights.data = torch.tensor(weights, dtype=torch.float32)
    
#     def predict(self, X):
#         """Prédit les classes pour X"""
#         self.eval()
#         X = torch.FloatTensor(X)
        
#         with torch.no_grad():
#             outputs = self(X)
#             _, predicted = torch.max(outputs, 1)
        
#         return predicted.numpy()
    
#     def predict_proba(self, X):
#         """Retourne les probabilités pour X"""
#         self.eval()
#         X = torch.FloatTensor(X)
        
#         with torch.no_grad():
#             outputs = self(X)
#             probabilities = torch.softmax(outputs, dim=1)
        
#         return probabilities.numpy()


# def create_qiskit_qrnn_model(n_qubits, num_classes, n_layers=3):
#     """Fonction de création du modèle QRNN Qiskit"""
#     return QiskitQRNN(n_qubits, n_layers, num_classes)

#new test that might work 
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim

# try:
#     from qiskit import QuantumCircuit, transpile
#     from qiskit_aer import AerSimulator
#     from qiskit.circuit import Parameter
#     HAS_QISKIT = True
# except ImportError:
#     HAS_QISKIT = False
#     print("⚠️ Qiskit not installed. Install with: pip install qiskit qiskit-aer")


# class QiskitQRNN(nn.Module):
#     """
#     QRNN avec Qiskit (simulateur Aer)
#     Utilise un circuit paramétré avec des rotations RY et portes CNOT
    
#     IMPORTANT: Les paramètres quantiques sont entraînés avec SPSA (sans gradient)
#     La couche finale classique est entraînée avec PyTorch (avec gradient)
#     """
    
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001, shots=1024):
#         super().__init__()
#         if not HAS_QISKIT:
#             raise ImportError("Qiskit is required. Install with: pip install qiskit qiskit-aer")
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.shots = shots
        
#         # Paramètres quantiques (angles de rotation)
#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
        
#         # Couche de sortie classique
#         self.fc = nn.Linear(n_qubits, num_classes)
        
#         # Optimiseur classique pour la couche FC
#         self.fc_optimizer = None
#         self.criterion = nn.CrossEntropyLoss()
        
#         # Simulateur
#         self.backend = AerSimulator()
        
#         # Construire le circuit quantique
#         self.circuit = self._build_circuit()
#         self.param_names = []
#         self.input_names = []
        
#         print(f"⚛️ QRNN Qiskit: {n_qubits} qubits, {n_layers} layers")
#         print(f"   Paramètres quantiques: {self.n_quantum_params} (optimisés avec SPSA)")
#         print(f"   Paramètres classiques: {n_qubits * num_classes + num_classes} (optimisés avec Adam)")
    
#     def _build_circuit(self):
#         """Construit le circuit quantique paramétré avec mesures"""
#         qc = QuantumCircuit(self.n_qubits, self.n_qubits)  # Ajout des bits classiques
        
#         # Paramètres pour chaque couche
#         self.param_names = []
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
        
#         # Entrées (features)
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]
        
#         # Encodage des données (AngleEmbedding-like avec RY)
#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)
        
#         # Couches variationnelles
#         param_idx = 0
#         for layer in range(self.n_layers):
#             # Rotations individuelles
#             for qubit in range(self.n_qubits):
#                 p1 = self.param_names[param_idx]; param_idx += 1
#                 p2 = self.param_names[param_idx]; param_idx += 1
#                 p3 = self.param_names[param_idx]; param_idx += 1
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             # Portes d'intrication (CNOT)
#             for qubit in range(self.n_qubits - 1):
#                 qc.cx(qubit, qubit + 1)
#             qc.cx(self.n_qubits - 1, 0)
        
#         # 🔥 AJOUT DES MESURES (CRITIQUE)
#         qc.measure_all()
        
#         return qc
    
#     def _get_parameter_values(self, x, weights):
#         """
#         Récupère les valeurs des paramètres pour l'exécution du circuit
#         """
#         param_values = {}
        
#         # 🔥 VÉRIFICATION DE DIMENSION (CRITIQUE)
#         if len(x) != self.n_qubits:
#             raise ValueError(f"Input size mismatch: expected {self.n_qubits} features, got {len(x)}")
        
#         # Valeurs des features (inputs)
#         for i in range(self.n_qubits):
#             param_values[self.input_names[i]] = float(x[i])
        
#         # Valeurs des poids quantiques
#         for idx, param_name in enumerate(self.param_names):
#             param_values[param_name] = float(weights[idx])
        
#         return param_values
    
#     def _run_circuit(self, x, weights):
#         """
#         Exécute le circuit quantique pour un échantillon
#         """
#         param_values = self._get_parameter_values(x, weights)
        
#         # Assigner les paramètres (compatible avec les versions récentes de Qiskit)
#         try:
#             bound_circuit = self.circuit.assign_parameters(param_values)
#         except AttributeError:
#             try:
#                 bound_circuit = self.circuit.bind_parameters(param_values)
#             except AttributeError:
#                 bound_circuit = self.circuit.copy()
#                 for param, value in param_values.items():
#                     bound_circuit = bound_circuit.assign_parameters({param: value})
        
#         # Transpiler et exécuter
#         transpiled = transpile(bound_circuit, self.backend)
#         job = self.backend.run(transpiled, shots=self.shots)
#         result = job.result()
#         counts = result.get_counts()
        
#         # Calculer les valeurs d'espérance à partir des mesures
#         expvals = []
#         for qubit in range(self.n_qubits):
#             prob0 = 0
#             prob1 = 0
#             for bitstring, count in counts.items():
#                 # La mesure donne les bits dans l'ordre q0 q1 q2...
#                 if len(bitstring) > qubit:
#                     if bitstring[qubit] == '0':
#                         prob0 += count
#                     else:
#                         prob1 += count
#             total = prob0 + prob1
#             if total > 0:
#                 # <Z> = P(0) - P(1)
#                 expval = (prob0 - prob1) / total
#             else:
#                 expval = 0
#             expvals.append(expval)
        
#         return np.array(expvals, dtype=np.float32)
    
#     def forward(self, x, quantum_weights=None):
#         """
#         Forward pass
#         x: tenseur de forme (batch_size, n_qubits)
#         quantum_weights: poids quantiques (optionnel, pour SPSA)
#         """
#         batch_size = x.shape[0]
#         device = x.device
        
#         # 🔥 VÉRIFICATION DES DIMENSIONS (CRITIQUE)
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Dimension mismatch: Expected {self.n_qubits} features, got {x.shape[1]}")
        
#         # Utiliser les poids passés en paramètre ou les poids du modèle
#         if quantum_weights is not None:
#             weights = quantum_weights
#         else:
#             weights = self.quantum_weights.detach().cpu().numpy()
        
#         # Exécution du circuit pour chaque échantillon
#         q_out = []
#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             expvals = self._run_circuit(x_i, weights)
#             q_out.append(expvals)
        
#         q_out = torch.tensor(np.array(q_out), dtype=torch.float32, device=device)
        
#         # Classification
#         out = self.fc(q_out)
#         return out
    
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


# def create_qiskit_qrnn_model(n_qubits, num_classes, n_layers=3):
#     return QiskitQRNN(n_qubits, n_layers, num_classes)

# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim

# try:
#     from qiskit import QuantumCircuit, transpile
#     from qiskit_aer import AerSimulator
#     from qiskit.circuit import Parameter
#     HAS_QISKIT = True
# except ImportError:
#     HAS_QISKIT = False
#     print("⚠️ Qiskit not installed. Install with: pip install qiskit qiskit-aer")


# class QiskitQRNN(nn.Module):
#     """
#     QRNN avec Qiskit (simulateur Aer)
#     Utilise un circuit paramétré avec des rotations RY et portes CNOT
#     """
    
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001, shots=1024):
#         super().__init__()
#         if not HAS_QISKIT:
#             raise ImportError("Qiskit is required. Install with: pip install qiskit qiskit-aer")
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.shots = shots
        
#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
        
#         self.fc = nn.Linear(n_qubits, num_classes)
#         self.fc_optimizer = None
#         self.criterion = nn.CrossEntropyLoss()
        
#         self.backend = AerSimulator()
        
#         self.circuit = self._build_circuit()
#         self.param_names = []
#         self.input_names = []
        
#         print(f"⚛️ QRNN Qiskit: {n_qubits} qubits, {n_layers} layers")
#         print(f"   Paramètres quantiques: {self.n_quantum_params}")
    
#     def _build_circuit(self):
#         """Construit le circuit quantique paramétré avec mesures"""
#         qc = QuantumCircuit(self.n_qubits, self.n_qubits)
        
#         self.param_names = []
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
        
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]
        
#         # Encodage
#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)
        
#         # Couches variationnelles
#         param_idx = 0
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = self.param_names[param_idx]; param_idx += 1
#                 p2 = self.param_names[param_idx]; param_idx += 1
#                 p3 = self.param_names[param_idx]; param_idx += 1
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             for qubit in range(self.n_qubits - 1):
#                 qc.cx(qubit, qubit + 1)
#             qc.cx(self.n_qubits - 1, 0)
        
#         qc.measure_all()
#         return qc
    
#     def _get_parameter_values(self, x, weights):
#         """
#         Récupère les valeurs des paramètres pour l'exécution du circuit
#         """
#         param_values = {}
        
#         # 🔥 SÉCURITÉ ABSOLUE
#         if len(x) < self.n_qubits:
#             raise ValueError(f"Input too small: got {len(x)}, expected {self.n_qubits}")
        
#         # 🔥 Tronquer si trop grand (solution pratique)
#         x = x[:self.n_qubits]
        
#         for i in range(self.n_qubits):
#             param_values[self.input_names[i]] = float(x[i])
        
#         for idx, param_name in enumerate(self.param_names):
#             param_values[param_name] = float(weights[idx])
        
#         return param_values
    
#     def _run_circuit(self, x, weights):
#         """
#         Exécute le circuit quantique pour un échantillon
#         """
#         param_values = self._get_parameter_values(x, weights)
        
#         try:
#             bound_circuit = self.circuit.assign_parameters(param_values)
#         except AttributeError:
#             try:
#                 bound_circuit = self.circuit.bind_parameters(param_values)
#             except AttributeError:
#                 bound_circuit = self.circuit.copy()
#                 for param, value in param_values.items():
#                     bound_circuit = bound_circuit.assign_parameters({param: value})
        
#         transpiled = transpile(bound_circuit, self.backend)
#         job = self.backend.run(transpiled, shots=self.shots)
#         result = job.result()
#         counts = result.get_counts()
        
#         expvals = []
#         for qubit in range(self.n_qubits):
#             prob0 = 0
#             prob1 = 0
#             for bitstring, count in counts.items():
#                 # 🔥 Correction: Qiskit retourne souvent l'ordre inversé
#                 bit = bitstring[::-1][qubit] if len(bitstring) > qubit else '0'
#                 if bit == '0':
#                     prob0 += count
#                 else:
#                     prob1 += count
#             total = prob0 + prob1
#             expval = (prob0 - prob1) / total if total > 0 else 0
#             expvals.append(expval)
        
#         return np.array(expvals, dtype=np.float32)
    
#     def forward(self, x, quantum_weights=None):
#         """
#         Forward pass
#         """
#         batch_size = x.shape[0]
#         device = x.device
        
#         # 🔥 DEBUG: Afficher la forme des données reçues
#         print(f"🔍 DEBUG forward - x.shape: {x.shape}, n_qubits: {self.n_qubits}")
        
#         # 🔥 VÉRIFICATION CRITIQUE
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Dimension mismatch: Expected {self.n_qubits} features, got {x.shape[1]}")
        
#         if quantum_weights is not None:
#             weights = quantum_weights
#         else:
#             weights = self.quantum_weights.detach().cpu().numpy()
        
#         q_out = []
#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             print(f"🔍 DEBUG x_i: {x_i}, len: {len(x_i)}")  # Debug
#             expvals = self._run_circuit(x_i, weights)
#             q_out.append(expvals)
        
#         q_out = torch.tensor(np.array(q_out), dtype=torch.float32, device=device)
#         out = self.fc(q_out)
#         return out
    
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


# def create_qiskit_qrnn_model(n_qubits, num_classes, n_layers=3):
#     return QiskitQRNN(n_qubits, n_layers, num_classes)

#ANOTHER ONE HOPE THIS ONE WORKS FINE 
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim

# try:
#     from qiskit import QuantumCircuit, transpile
#     from qiskit_aer import AerSimulator
#     from qiskit.circuit import Parameter
#     HAS_QISKIT = True
# except ImportError:
#     HAS_QISKIT = False
#     print("⚠️ Qiskit not installed. Install with: pip install qiskit qiskit-aer")


# class QiskitQRNN(nn.Module):
#     """
#     QRNN avec Qiskit (simulateur Aer)
#     Utilise un circuit paramétré avec des rotations RY et portes CNOT
#     """
    
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001, shots=1024):
#         super().__init__()
#         if not HAS_QISKIT:
#             raise ImportError("Qiskit is required. Install with: pip install qiskit qiskit-aer")
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.shots = shots
        
#         # Paramètres quantiques (angles de rotation)
#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
        
#         # Couche de sortie classique
#         self.fc = nn.Linear(n_qubits, num_classes)
        
#         # Optimiseur classique pour la couche FC
#         self.fc_optimizer = None
#         self.criterion = nn.CrossEntropyLoss()
        
#         # Simulateur
#         self.backend = AerSimulator()
        
#         # 🔥 IMPORTANT: Construire le circuit (cela remplit param_names et input_names)
#         self.circuit = self._build_circuit()
        
#         # ✅ NE PAS réinitialiser param_names et input_names ici !
#         # Les attributs sont déjà définis dans _build_circuit()
        
#         print(f"⚛️ QRNN Qiskit: {n_qubits} qubits, {n_layers} layers")
#         print(f"   Paramètres quantiques: {self.n_quantum_params}")
#         print(f"   Input names length: {len(self.input_names)}")  # Debug
#         print(f"   Param names length: {len(self.param_names)}")  # Debug
    
#     def _build_circuit(self):
#         """Construit le circuit quantique paramétré avec mesures"""
#         qc = QuantumCircuit(self.n_qubits, self.n_qubits)
        
#         # 🔥 Initialiser les listes ici (pas dans __init__)
#         self.param_names = []
#         self.input_names = []
        
#         # Paramètres pour chaque couche
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
        
#         # Entrées (features)
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]
        
#         # Encodage des données (AngleEmbedding-like avec RY)
#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)
        
#         # Couches variationnelles
#         param_idx = 0
#         for layer in range(self.n_layers):
#             # Rotations individuelles
#             for qubit in range(self.n_qubits):
#                 p1 = self.param_names[param_idx]; param_idx += 1
#                 p2 = self.param_names[param_idx]; param_idx += 1
#                 p3 = self.param_names[param_idx]; param_idx += 1
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
            
#             # Portes d'intrication (CNOT)
#             for qubit in range(self.n_qubits - 1):
#                 qc.cx(qubit, qubit + 1)
#             qc.cx(self.n_qubits - 1, 0)
        
#         # Mesures
#         qc.measure_all()
        
#         return qc
    
#     def _get_parameter_values(self, x, weights):
#         """
#         Récupère les valeurs des paramètres pour l'exécution du circuit
#         """
#         param_values = {}
        
#         # 🔥 SÉCURITÉ ABSOLUE
#         if len(x) < self.n_qubits:
#             raise ValueError(f"Input too small: got {len(x)}, expected {self.n_qubits}")
        
#         # 🔥 Vérifier que input_names est correctement initialisé
#         if len(self.input_names) != self.n_qubits:
#             raise ValueError(f"input_names length mismatch: {len(self.input_names)} != {self.n_qubits}")
        
#         # Tronquer si trop grand
#         x = x[:self.n_qubits]
        
#         # Valeurs des features (inputs)
#         for i in range(self.n_qubits):
#             param_values[self.input_names[i]] = float(x[i])
        
#         # Valeurs des poids quantiques
#         for idx, param_name in enumerate(self.param_names):
#             param_values[param_name] = float(weights[idx])
        
#         return param_values
    
#     def _run_circuit(self, x, weights):
#         """
#         Exécute le circuit quantique pour un échantillon
#         """
#         param_values = self._get_parameter_values(x, weights)
        
#         # Assigner les paramètres
#         try:
#             bound_circuit = self.circuit.assign_parameters(param_values)
#         except AttributeError:
#             try:
#                 bound_circuit = self.circuit.bind_parameters(param_values)
#             except AttributeError:
#                 bound_circuit = self.circuit.copy()
#                 for param, value in param_values.items():
#                     bound_circuit = bound_circuit.assign_parameters({param: value})
        
#         # Transpiler et exécuter
#         transpiled = transpile(bound_circuit, self.backend)
#         job = self.backend.run(transpiled, shots=self.shots)
#         result = job.result()
#         counts = result.get_counts()
        
#         # Calculer les valeurs d'espérance
#         expvals = []
#         for qubit in range(self.n_qubits):
#             prob0 = 0
#             prob1 = 0
#             for bitstring, count in counts.items():
#                 # Correction ordre des bits
#                 bit = bitstring[::-1][qubit] if len(bitstring) > qubit else '0'
#                 if bit == '0':
#                     prob0 += count
#                 else:
#                     prob1 += count
#             total = prob0 + prob1
#             expval = (prob0 - prob1) / total if total > 0 else 0
#             expvals.append(expval)
        
#         return np.array(expvals, dtype=np.float32)
    
#     def forward(self, x, quantum_weights=None):
#         """
#         Forward pass
#         """
#         batch_size = x.shape[0]
#         device = x.device
        
#         # Debug
#         print(f"🔍 DEBUG forward - x.shape: {x.shape}, n_qubits: {self.n_qubits}")
#         print(f"🔍 DEBUG input_names length: {len(self.input_names)}")
        
#         # Vérification des dimensions
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Dimension mismatch: Expected {self.n_qubits} features, got {x.shape[1]}")
        
#         if quantum_weights is not None:
#             weights = quantum_weights
#         else:
#             weights = self.quantum_weights.detach().cpu().numpy()
        
#         q_out = []
#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             print(f"🔍 DEBUG x_i: {x_i}, len: {len(x_i)}")
#             expvals = self._run_circuit(x_i, weights)
#             q_out.append(expvals)
        
#         q_out = torch.tensor(np.array(q_out), dtype=torch.float32, device=device)
#         out = self.fc(q_out)
#         return out
    
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


# def create_qiskit_qrnn_model(n_qubits, num_classes, n_layers=3):
#     return QiskitQRNN(n_qubits, n_layers, num_classes)

#version 6 GROK VERSION hope this one works 

# import numpy as np
# import torch
# import torch.nn as nn
# from qiskit import QuantumCircuit, transpile
# from qiskit_aer import AerSimulator
# from qiskit.circuit import Parameter
# from qiskit.quantum_info import SparsePauliOp

# class QiskitQRNN(nn.Module):
#     """
#     QRNN avec Qiskit - Version hautement optimisée
#     - Statevector simulator (exact, très rapide)
#     - Batching des circuits
#     - Transpile optimisé
#     - Calcul rapide des <Z> avec SparsePauliOp
#     """
   
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001):
#         super().__init__()
       
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
       
#         # Paramètres quantiques (angles)
#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
       
#         # Couche classique de sortie
#         self.fc = nn.Linear(n_qubits, num_classes)
#         self.criterion = nn.CrossEntropyLoss()
       
#         # Backend ultra-rapide : statevector
#         self.backend = AerSimulator(method='statevector')
       
#         # Construction du circuit
#         self.circuit = self._build_circuit()
       
#         # Transpile du template une seule fois
#         self.transpiled_template = transpile(self.circuit, self.backend, optimization_level=1)
       
#         # Pré-calcul des observables Z pour chaque qubit (très important pour la vitesse)
#         self.pauli_z_list = []
#         for q in range(n_qubits):
#             pauli_str = 'I' * q + 'Z' + 'I' * (n_qubits - q - 1)
#             self.pauli_z_list.append(SparsePauliOp(pauli_str))
       
#         print(f"✅ QRNN Qiskit optimisé chargé : {n_qubits} qubits, {n_layers} layers")
#         print(f"   Paramètres quantiques : {self.n_quantum_params}")
#         print(f"   Backend : Statevector (exact & rapide)")
   
#     def _build_circuit(self):
#         """Construit le circuit paramétré"""
#         qc = QuantumCircuit(self.n_qubits)
       
#         self.param_names = []
#         self.input_names = []
       
#         # Paramètres θ
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = Parameter(f'θ_{layer}_{qubit}_0')
#                 p2 = Parameter(f'θ_{layer}_{qubit}_1')
#                 p3 = Parameter(f'θ_{layer}_{qubit}_2')
#                 self.param_names.extend([p1, p2, p3])
       
#         # Features d'entrée (x)
#         self.input_names = [Parameter(f'x_{i}') for i in range(self.n_qubits)]
       
#         # Encoding
#         for i in range(self.n_qubits):
#             qc.ry(self.input_names[i], i)
       
#         # Couches variationnelles + entanglement
#         param_idx = 0
#         for layer in range(self.n_layers):
#             for qubit in range(self.n_qubits):
#                 p1 = self.param_names[param_idx]; param_idx += 1
#                 p2 = self.param_names[param_idx]; param_idx += 1
#                 p3 = self.param_names[param_idx]; param_idx += 1
#                 qc.ry(p1, qubit)
#                 qc.rz(p2, qubit)
#                 qc.ry(p3, qubit)
           
#             # Entanglement en anneau
#             for qubit in range(self.n_qubits - 1):
#                 qc.cx(qubit, qubit + 1)
#             qc.cx(self.n_qubits - 1, 0)
       
#         return qc
   
#     def _get_parameter_values(self, x, weights):
#         param_values = {}
#         for i in range(self.n_qubits):
#             param_values[self.input_names[i]] = float(x[i])
#         for idx, param_name in enumerate(self.param_names):
#             param_values[param_name] = float(weights[idx])
#         return param_values
   
#     def forward(self, x, quantum_weights=None):
#         batch_size = x.shape[0]
#         device = x.device
       
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")
       
#         weights = quantum_weights if quantum_weights is not None else self.quantum_weights.detach().cpu().numpy()
       
#         # 1. Créer tous les circuits du batch
#         circuits_to_run = []
#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             param_values = self._get_parameter_values(x_i, weights)
#             bound = self.circuit.assign_parameters(param_values)
#             circuits_to_run.append(bound)
       
#         # 2. Transpiler le batch une seule fois
#         transpiled_batch = transpile(circuits_to_run, self.backend, optimization_level=1)
       
#         # 3. Exécution batch (statevector)
#         job = self.backend.run(transpiled_batch)
#         result = job.result()
       
#         # 4. Extraction rapide des <Z>
#         q_out = []
#         for i in range(batch_size):
#             sv = result.get_statevector(i)
#             expvals = []
#             for pauli_z in self.pauli_z_list:
#                 expval = sv.expectation_value(pauli_z)
#                 expvals.append(float(expval.real))
#             q_out.append(expvals)
       
#         q_out = torch.tensor(np.array(q_out, dtype=np.float32), device=device)
#         return self.fc(q_out)
   
#     # Méthodes utilitaires
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


# def create_qiskit_qrnn_model(n_qubits, num_classes=2, n_layers=3):
#     return QiskitQRNN(n_qubits, n_layers, num_classes)

#version 7 GROK VERSION - Correction de bugs et optimisations supplémentaires

# import numpy as np
# import torch
# import torch.nn as nn
# from qiskit import QuantumCircuit, transpile
# from qiskit_aer import AerSimulator
# from qiskit.circuit import Parameter
# from qiskit.quantum_info import SparsePauliOp

# class QiskitQRNN(nn.Module):
#     """
#     QRNN Qiskit CLEAN - Version Finale GPU-safe
#     """
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001):
#         super().__init__()
       
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
       
#         self.n_quantum_params = n_layers * n_qubits * 3
#         self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
       
#         self.fc = nn.Linear(n_qubits, num_classes)
#         self.criterion = nn.CrossEntropyLoss()
       
#         self.backend = AerSimulator(method='statevector')
       
#         self.circuit = self._build_circuit()
#         self.transpiled_template = transpile(self.circuit, self.backend, optimization_level=1)
       
#         self.pauli_z_ops = []
#         for q in range(self.n_qubits):
#             pauli_str = 'I' * (self.n_qubits - q - 1) + 'Z' + 'I' * q
#             self.pauli_z_ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))
       
#         print(f"✅ QRNN Qiskit CLEAN chargé : {n_qubits} qubits, {n_layers} layers | Statevector")

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

#         qc.save_statevector()
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

#         weights = (quantum_weights if quantum_weights is not None 
#                    else self.quantum_weights.detach().cpu().numpy())

#         circuits_to_run = []
#         for i in range(batch_size):
#             x_i = x[i].detach().cpu().numpy()
#             param_values = self._get_parameter_values(x_i, weights)
#             bound = self.transpiled_template.assign_parameters(param_values)
#             circuits_to_run.append(bound)

#         result = self.backend.run(circuits_to_run).result()

#         q_out = []
#         for i in range(batch_size):
#             try:
#                 sv = result.get_statevector(i)
#             except Exception:
#                 sv = result.data(i)['statevector']
            
#             expvals = [float(sv.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
#             q_out.append(expvals)

#         # 🔥 FIX IMPORTANT : Qiskit retourne sur CPU → on le met sur le bon device
#         q_out = torch.tensor(np.array(q_out, dtype=np.float32), device=device)
#         return self.fc(q_out)

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


# def create_qiskit_qrnn_model(n_qubits, num_classes=2, n_layers=3):
#     return QiskitQRNN(n_qubits, n_layers, num_classes)

#NEW VERSION FOR FLEXIBILITY TEST 1 __________________________________________________________________________#

import numpy as np
import torch
import torch.nn as nn
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from ml_pipeline.adaptive_config import AdaptiveConfig

class QiskitQRNN(nn.Module):
    """
    QRNN Qiskit CLEAN - Adaptatif
    Règle : None = auto-calculé par AdaptiveConfig
    """
    def __init__(self, n_qubits, n_layers=None, num_classes=2, learning_rate=None,
                 dataset_info=None):
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
            
            print(f"📊 Qiskit Clean Adaptatif [{n_samples} samples, {n_features} features, "
                  f"{n_classes} classes]: qubits={n_qubits}, layers={n_layers}, "
                  f"lr={learning_rate:.5f}, SPSA={self.epochs}, FC={self.fc_epochs}")
        else:
            self.epochs = 20
            self.fc_epochs = 20
       
        self.n_qubits = n_qubits
        self.n_layers = n_layers if n_layers is not None else 3
        self.num_classes = num_classes
        self.learning_rate = learning_rate if learning_rate is not None else 0.001
       
        self.n_quantum_params = self.n_layers * n_qubits * 3
        self.quantum_weights = nn.Parameter(0.1 * torch.randn(self.n_quantum_params))
        self.fc = nn.Linear(n_qubits, num_classes)
        self.criterion = nn.CrossEntropyLoss()
        self.backend = AerSimulator(method='statevector')
        self.circuit = self._build_circuit()
        self.transpiled_template = transpile(self.circuit, self.backend, optimization_level=1)
       
        self.pauli_z_ops = []
        for q in range(self.n_qubits):
            pauli_str = 'I' * (self.n_qubits - q - 1) + 'Z' + 'I' * q
            self.pauli_z_ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))
       
        print(f"✅ QRNN Qiskit CLEAN : {n_qubits} qubits, {self.n_layers} layers | "
              f"lr={self.learning_rate} | SPSA={self.epochs} | FC={self.fc_epochs}")

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
        qc.save_statevector()
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
        circuits_to_run = []
        for i in range(batch_size):
            x_i = x[i].detach().cpu().numpy()
            bound = self.transpiled_template.assign_parameters(
                self._get_parameter_values(x_i, weights)
            )
            circuits_to_run.append(bound)
        result = self.backend.run(circuits_to_run).result()
        q_out = []
        for i in range(batch_size):
            try:
                sv = result.get_statevector(i)
            except Exception:
                sv = result.data(i)['statevector']
            expvals = [float(sv.expectation_value(pauli).real) for pauli in self.pauli_z_ops]
            q_out.append(expvals)
        q_out = torch.tensor(np.array(q_out, dtype=np.float32), device=device)
        return self.fc(q_out)

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
                              dataset_info=None):
    return QiskitQRNN(
        n_qubits=n_qubits,
        n_layers=n_layers,
        num_classes=num_classes,
        learning_rate=learning_rate,
        dataset_info=dataset_info
    )