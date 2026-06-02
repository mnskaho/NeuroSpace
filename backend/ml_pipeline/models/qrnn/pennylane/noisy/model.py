# import pennylane as qml
# import torch
# import torch.nn as nn
# import numpy as np

# class QRNNClassifier(nn.Module):
#     """
#     QRNN PennyLane NOISY - Bruit Depolarizing sur les gates uniquement
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

#         self.dev = qml.device('default.mixed', wires=n_qubits)

#         self.weight_shape = qml.StronglyEntanglingLayers.shape(n_layers, n_qubits)
#         self.weights = nn.Parameter(0.1 * torch.randn(self.weight_shape))
       
#         self.fc = nn.Linear(n_qubits, num_classes)
#         self.input_scale = nn.Parameter(torch.ones(n_qubits) * np.pi/2)

#         print(f"⚛️ [NOISY] QRNN PennyLane chargé : {n_qubits} qubits | Noise gates={noise_level} | Mitigation={self.mitigation_runs}")

#         @qml.qnode(self.dev, interface='torch', diff_method='backprop')
#         def circuit(inputs, weights):
#             qml.AngleEmbedding(inputs, wires=range(self.n_qubits))
#             qml.StronglyEntanglingLayers(weights, wires=range(self.n_qubits))
           
#             if self.noise_level > 0.0:
#                 for w in range(self.n_qubits):
#                     qml.DepolarizingChannel(self.noise_level, wires=w)
           
#             return [qml.expval(qml.PauliZ(i)) for i in range(self.n_qubits)]
       
#         self.circuit = circuit

#     def forward(self, x):
#         batch_size = x.shape[0]
#         device = x.device
       
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")

#         x_scaled = x * self.input_scale

#         if self.noise_level > 0.0 and self.mitigation_runs > 1:
#             all_q_out = []
#             for _ in range(self.mitigation_runs):
#                 q_out_run = torch.stack([
#                     torch.stack(self.circuit(x_scaled[i], self.weights)) 
#                     for i in range(batch_size)
#                 ])
#                 all_q_out.append(q_out_run)
#             q_out = torch.mean(torch.stack(all_q_out), dim=0)
#         else:
#             q_out = torch.stack([
#                 torch.stack(self.circuit(x_scaled[i], self.weights)) 
#                 for i in range(batch_size)
#             ]).float().to(device)

#         return self.fc(q_out)

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


# def create_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1):
#     return QRNNClassifier(n_qubits, n_layers, num_classes, noise_level=noise_level, mitigation_runs=mitigation_runs)

#ERROR FLOT 64 ABOVE TRYING THIS 
# import pennylane as qml
# import torch
# import torch.nn as nn
# import numpy as np

# def build_noisy_qnode(n_qubits, dev, noise_level):
#     @qml.qnode(dev, interface='torch', diff_method='backprop')
#     def circuit(inputs, weights):
#         qml.AngleEmbedding(inputs, wires=range(n_qubits))
#         qml.StronglyEntanglingLayers(weights, wires=range(n_qubits))
#         if noise_level > 0.0:
#             for w in range(n_qubits):
#                 qml.DepolarizingChannel(noise_level, wires=w)
#         return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]
#     return circuit


# class QRNNClassifier(nn.Module):
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001,
#                  noise_level=0.0, mitigation_runs=1):
#         super().__init__()
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
#         self.noise_level = noise_level
#         self.mitigation_runs = max(1, mitigation_runs)

#         self.dev = qml.device('default.mixed', wires=n_qubits)
#         self.weight_shape = qml.StronglyEntanglingLayers.shape(n_layers, n_qubits)
        
#         # 🔥 FIX: forcer float32 sur les poids
#         self.weights = nn.Parameter(
#             0.1 * torch.randn(self.weight_shape, dtype=torch.float32)
#         )
        
#         self.fc = nn.Linear(n_qubits, num_classes)
        
#         # 🔥 FIX: forcer float32 sur input_scale
#         self.input_scale = nn.Parameter(
#             torch.ones(n_qubits, dtype=torch.float32) * (np.pi / 2)
#         )

#         self.circuit = build_noisy_qnode(n_qubits, self.dev, noise_level)

#         print(f"✅ [NOISY] QRNN PennyLane chargé : {n_qubits} qubits | Noise={noise_level} | Mitigation={self.mitigation_runs}")

#     def forward(self, x):
#         batch_size = x.shape[0]
#         device = x.device

#         x = x.float()

#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")

#         x_scaled = x * self.input_scale

#         if self.noise_level > 0.0 and self.mitigation_runs > 1:
#             all_q_out = []
#             for _ in range(self.mitigation_runs):
#                 q_out_run = torch.stack([
#                     torch.stack(self.circuit(x_scaled[i], self.weights))
#                     for i in range(batch_size)
#                 ])
#                 all_q_out.append(q_out_run)
#             q_out = torch.mean(torch.stack(all_q_out), dim=0)
#         else:
#             q_out = torch.stack([
#                 torch.stack(self.circuit(x_scaled[i], self.weights))
#                 for i in range(batch_size)
#             ])

#         q_out = q_out.float().to(device)
#         return self.fc(q_out)

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


# def create_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1, learning_rate=0.001):
#     return QRNNClassifier(
#         n_qubits=n_qubits,
#         n_layers=n_layers,
#         num_classes=num_classes,
#         learning_rate=learning_rate,
#         noise_level=noise_level,
#         mitigation_runs=mitigation_runs
#     )

# _____________________________________________________________________________________________

# GROK VERSION TO FIX MISMATCH CPU AND GPU 
# import pennylane as qml
# import torch
# import torch.nn as nn
# import numpy as np

# class QRNNClassifier(nn.Module):
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001,
#                  noise_level=0.0, mitigation_runs=1):
#         super().__init__()
        
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.noise_level = noise_level
#         self.mitigation_runs = max(1, mitigation_runs)

#         self.dev = qml.device('default.mixed', wires=n_qubits)
#         self.weight_shape = qml.StronglyEntanglingLayers.shape(n_layers, n_qubits)
#         self.weights = nn.Parameter(0.1 * torch.randn(self.weight_shape, dtype=torch.float32))
        
#         self.fc = nn.Linear(n_qubits, num_classes)
#         self.input_scale = nn.Parameter(torch.ones(n_qubits, dtype=torch.float32) * (np.pi / 2))

#         @qml.qnode(self.dev, interface='torch', diff_method='backprop')
#         def circuit(inputs, weights):
#             qml.AngleEmbedding(inputs, wires=range(self.n_qubits))
#             qml.StronglyEntanglingLayers(weights, wires=range(self.n_qubits))
#             if self.noise_level > 0.0:
#                 for w in range(self.n_qubits):
#                     qml.DepolarizingChannel(self.noise_level, wires=w)
#             return [qml.expval(qml.PauliZ(i)) for i in range(self.n_qubits)]
        
#         self.circuit = circuit

#         print(f"✅ [NOISY] QRNN PennyLane chargé : {n_qubits} qubits | Noise={noise_level} | Mitigation={self.mitigation_runs}")

#     def forward(self, x):
#         device = x.device
#         x = x.to(device).float()

#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")

#         x_scaled = x * self.input_scale.to(device)

#         # Fix forme : (batch, n_qubits)
#         if self.noise_level > 0.0 and self.mitigation_runs > 1:
#             all_q_out = []
#             for _ in range(self.mitigation_runs):
#                 q_out_list = self.circuit(x_scaled, self.weights)
#                 q_out_run = torch.stack(q_out_list, dim=1)   # (batch, n_qubits)
#                 all_q_out.append(q_out_run)
#             q_out = torch.mean(torch.stack(all_q_out), dim=0)
#         else:
#             q_out_list = self.circuit(x_scaled, self.weights)
#             q_out = torch.stack(q_out_list, dim=1)           # (batch, n_qubits)

#         q_out = q_out.float().to(device)
#         return self.fc(q_out)

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


# def create_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1):
#     return QRNNClassifier(n_qubits, n_layers, num_classes, noise_level=noise_level, mitigation_runs=mitigation_runs)


#NEW VERSION FOR FLEXIBILITY __________________________________________________________________________________________________________#

import pennylane as qml
import torch
import torch.nn as nn
import numpy as np
from ml_pipeline.adaptive_config import AdaptiveConfig

class QRNNClassifier(nn.Module):
    """
    QRNN PennyLane NOISY - Adaptatif
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
            
            print(f"📊 QRNN Noisy Adaptatif [{n_samples} samples, {n_features} features, "
                  f"{n_classes} classes]: qubits={n_qubits}, layers={n_layers}, "
                  f"lr={learning_rate:.5f}, epochs={self.epochs}")
        else:
            self.epochs = 20
        
        self.n_qubits = n_qubits
        self.n_layers = n_layers if n_layers is not None else 3
        self.num_classes = num_classes
        self.learning_rate = learning_rate if learning_rate is not None else 0.001
        self.noise_level = noise_level
        self.mitigation_runs = max(1, mitigation_runs)

        self.dev = qml.device('default.mixed', wires=n_qubits)
        self.weight_shape = qml.StronglyEntanglingLayers.shape(self.n_layers, n_qubits)
        self.weights = nn.Parameter(0.1 * torch.randn(self.weight_shape, dtype=torch.float32))
        self.fc = nn.Linear(n_qubits, num_classes)
        self.input_scale = nn.Parameter(torch.ones(n_qubits, dtype=torch.float32) * (np.pi / 2))

        @qml.qnode(self.dev, interface='torch', diff_method='backprop')
        def circuit(inputs, weights):
            qml.AngleEmbedding(inputs, wires=range(self.n_qubits))
            qml.StronglyEntanglingLayers(weights, wires=range(self.n_qubits))
            if self.noise_level > 0.0:
                for w in range(self.n_qubits):
                    qml.DepolarizingChannel(self.noise_level, wires=w)
            return [qml.expval(qml.PauliZ(i)) for i in range(self.n_qubits)]
        
        self.circuit = circuit
        print(f"✅ [NOISY] QRNN PennyLane : {n_qubits} qubits | Noise={noise_level} | "
              f"Mitigation={self.mitigation_runs} | layers={self.n_layers} | epochs={self.epochs}")

    def forward(self, x):
        device = x.device
        x = x.to(device).float()
        batch_size = x.shape[0]
        
        if x.shape[1] != self.n_qubits:
            raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")
        
        x_scaled = x * self.input_scale.to(device)
        
        if self.noise_level > 0.0 and self.mitigation_runs > 1:
            q_out = []
            for i in range(batch_size):
                all_runs = []
                for _ in range(self.mitigation_runs):
                    q_out_i = self.circuit(x_scaled[i], self.weights)
                    all_runs.append(torch.stack(q_out_i))
                q_out.append(torch.mean(torch.stack(all_runs), dim=0))
            q_out = torch.stack(q_out)
        else:
            q_out = []
            for i in range(batch_size):
                q_out_i = self.circuit(x_scaled[i], self.weights)
                q_out.append(torch.stack(q_out_i))
            q_out = torch.stack(q_out)
        
        q_out = q_out.float().to(device)
        return self.fc(q_out)

    def predict(self, X):
        self.eval()
        X = torch.FloatTensor(X).to(self.fc.weight.device)
        with torch.no_grad():
            outputs = self(X)
            _, predicted = torch.max(outputs, 1)
        return predicted.cpu().numpy()

    def predict_proba(self, X):
        self.eval()
        X = torch.FloatTensor(X).to(self.fc.weight.device)
        with torch.no_grad():
            outputs = self(X)
            probabilities = torch.softmax(outputs, dim=1)
        return probabilities.cpu().numpy()


def create_qrnn_model(n_qubits, num_classes=2, n_layers=None, learning_rate=None,
                      noise_level=0.0, mitigation_runs=1, dataset_info=None):
    return QRNNClassifier(
        n_qubits=n_qubits,
        n_layers=n_layers,
        num_classes=num_classes,
        learning_rate=learning_rate,
        noise_level=noise_level,
        mitigation_runs=mitigation_runs,
        dataset_info=dataset_info
    )