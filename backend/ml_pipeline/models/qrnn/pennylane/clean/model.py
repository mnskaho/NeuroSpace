# import ml_pipeline.models.qrnn.pennylane.clean as qml
# import torch
# import torch.nn as nn
# import torch.optim as optim
# import numpy as np

# class QRNNClassifier(nn.Module):
#     """
#     QRNN avec PennyLane et AngleEmbedding
#     Features = n_qubits (Thumb Rule)
#     """
    
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001):
#         super().__init__()
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
        
#         # Device quantique
#         self.dev = qml.device('default.qubit', wires=n_qubits)
        
#         # Poids du circuit (StronglyEntanglingLayers)
#         self.weight_shape = qml.StronglyEntanglingLayers.shape(n_layers, n_qubits)
#         self.weights = nn.Parameter(0.1 * torch.randn(self.weight_shape))
        
#         # Couche de sortie classique
#         self.fc = nn.Linear(n_qubits, num_classes)
        
#         # Optimiseur et loss
#         self.optimizer = None
#         self.criterion = nn.CrossEntropyLoss()
        
#         # Échelle d'entrée apprise (normalisation adaptative)
#         self.input_scale = nn.Parameter(torch.ones(n_qubits) * np.pi/2)
        
#         print(f"⚛️ QRNN PennyLane: {n_qubits} qubits, {n_layers} layers")
        
#         @qml.qnode(self.dev, interface='torch', diff_method='backprop')
#         def circuit(inputs, weights):
#             """
#             Circuit quantique:
#             1. AngleEmbedding: encode les features dans les angles RX
#             2. StronglyEntanglingLayers: couches variationnelles
#             3. Mesure: expval PauliZ sur chaque qubit
#             """
#             qml.AngleEmbedding(inputs, wires=range(self.n_qubits))
#             qml.StronglyEntanglingLayers(weights, wires=range(self.n_qubits))
#             return [qml.expval(qml.PauliZ(i)) for i in range(self.n_qubits)]
        
#         self.circuit = circuit

#     def forward(self, x):
#         """
#         Forward pass
#         x: tenseur de forme (batch_size, n_qubits)
#         """
#         batch_size = x.shape[0]
#         device = x.device
        
#         # Vérification des dimensions
#         if x.shape[1] != self.n_qubits:
#             raise ValueError(
#                 f"Dimension mismatch: reçu {x.shape[1]} features, "
#                 f"attendu {self.n_qubits} (n_qubits)"
#             )
        
#         # Mise à l'échelle adaptative
#         x_scaled = x * self.input_scale
        
#         # Passage dans le circuit quantique pour chaque échantillon
#         q_out = torch.stack([
#             torch.stack(self.circuit(x_scaled[i], self.weights))
#             for i in range(batch_size)
#         ]).float().to(device)
        
#         # Classification finale
#         out = self.fc(q_out)
#         return out
    
#     def fit(self, X, y, epochs=10, batch_size=32, verbose=True):
#         """Entraîne le modèle"""
#         self.train()
        
#         if self.optimizer is None:
#             self.optimizer = optim.Adam(self.parameters(), lr=self.learning_rate)
        
#         X = torch.FloatTensor(X)
#         y = torch.LongTensor(y)
        
#         dataset = torch.utils.data.TensorDataset(X, y)
#         dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
#         history = {'train_loss': [], 'train_acc': []}
        
#         for epoch in range(epochs):
#             epoch_loss = 0
#             correct = 0
#             total = 0
            
#             for batch_X, batch_y in dataloader:
#                 self.optimizer.zero_grad()
#                 outputs = self(batch_X)
#                 loss = self.criterion(outputs, batch_y)
#                 loss.backward()
                
#                 # Clip gradient pour stabilité
#                 torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
#                 self.optimizer.step()
                
#                 epoch_loss += loss.item()
#                 _, predicted = torch.max(outputs, 1)
#                 total += batch_y.size(0)
#                 correct += (predicted == batch_y).sum().item()
            
#             avg_loss = epoch_loss / len(dataloader)
#             accuracy = correct / total
            
#             history['train_loss'].append(avg_loss)
#             history['train_acc'].append(accuracy)
            
#             if verbose and (epoch + 1) % 5 == 0:
#                 print(f"   Époque {epoch+1}/{epochs} - Loss: {avg_loss:.4f}, Acc: {accuracy:.4f}")
        
#         return history
    
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


# def create_qrnn_model(n_qubits, num_classes, n_layers=3):
#     """Fonction de création du modèle QRNN PennyLane"""
#     return QRNNClassifier(n_qubits, n_layers, num_classes)


# NEW CUZ ERROR FLOT 64 IN ABOVE 
# import pennylane as qml
# import torch
# import torch.nn as nn
# import numpy as np

# def build_clean_qnode(n_qubits, dev):
#     @qml.qnode(dev, interface='torch', diff_method='backprop')
#     def circuit(inputs, weights):
#         qml.AngleEmbedding(inputs, wires=range(n_qubits))
#         qml.StronglyEntanglingLayers(weights, wires=range(n_qubits))
#         return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]
#     return circuit


# class QRNNClassifier(nn.Module):
#     def __init__(self, n_qubits, n_layers=3, num_classes=2, learning_rate=0.001):
#         super().__init__()
#         self.n_qubits = n_qubits
#         self.n_layers = n_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate

#         self.dev = qml.device('default.qubit', wires=n_qubits)
#         self.weight_shape = qml.StronglyEntanglingLayers.shape(n_layers, n_qubits)
        
#         self.weights = nn.Parameter(0.1 * torch.randn(self.weight_shape, dtype=torch.float32))
        
#         self.fc = nn.Linear(n_qubits, num_classes)
#         self.input_scale = nn.Parameter(torch.ones(n_qubits, dtype=torch.float32) * (np.pi / 2))

#         self.circuit = build_clean_qnode(n_qubits, self.dev)

#         print(f"✅ [CLEAN] QRNN PennyLane chargé : {n_qubits} qubits, {n_layers} layers")

#     def forward(self, x):
#         device = x.device
#         x = x.to(device).float()                     # ← Fix important

#         if x.shape[1] != self.n_qubits:
#             raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")

#         x_scaled = x * self.input_scale.to(device)   # ← Fix important

#         q_out_list = self.circuit(x_scaled, self.weights)
#         q_out = torch.stack(q_out_list, dim=1)       # (batch, n_qubits)

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


# def create_qrnn_model(n_qubits, num_classes=2, n_layers=3):
#     return QRNNClassifier(n_qubits, n_layers, num_classes)

#NEW VERSION FLEXIBLE TEST______________________________________________________________________________________________________#

import pennylane as qml
import torch
import torch.nn as nn
import numpy as np
from ml_pipeline.adaptive_config import AdaptiveConfig

def build_clean_qnode(n_qubits, dev):
    @qml.qnode(dev, interface='torch', diff_method='backprop')
    def circuit(inputs, weights):
        qml.AngleEmbedding(inputs, wires=range(n_qubits))
        qml.StronglyEntanglingLayers(weights, wires=range(n_qubits))
        return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]
    return circuit


class QRNNClassifier(nn.Module):
    """
    QRNN PennyLane CLEAN - Adaptatif
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
            
            print(f"📊 QRNN Clean Adaptatif [{n_samples} samples, {n_features} features, "
                  f"{n_classes} classes]: qubits={n_qubits}, layers={n_layers}, "
                  f"lr={learning_rate:.5f}, epochs={self.epochs}")
        else:
            self.epochs = 20
        
        self.n_qubits = n_qubits
        self.n_layers = n_layers if n_layers is not None else 3
        self.num_classes = num_classes
        self.learning_rate = learning_rate if learning_rate is not None else 0.001

        self.dev = qml.device('default.qubit', wires=n_qubits)
        self.weight_shape = qml.StronglyEntanglingLayers.shape(self.n_layers, n_qubits)
        
        self.weights = nn.Parameter(0.1 * torch.randn(self.weight_shape, dtype=torch.float32))
        self.fc = nn.Linear(n_qubits, num_classes)
        self.input_scale = nn.Parameter(torch.ones(n_qubits, dtype=torch.float32) * (np.pi / 2))
        self.circuit = build_clean_qnode(n_qubits, self.dev)

        print(f"✅ [CLEAN] QRNN PennyLane : {n_qubits} qubits, {self.n_layers} layers | "
              f"lr={self.learning_rate} | epochs={self.epochs}")

    def forward(self, x):
        device = x.device
        x = x.to(device).float()
        batch_size = x.shape[0]
        
        if x.shape[1] != self.n_qubits:
            raise ValueError(f"Expected {self.n_qubits} features, got {x.shape[1]}")
        
        x_scaled = x * self.input_scale.to(device)
        
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
                      dataset_info=None):
    return QRNNClassifier(
        n_qubits=n_qubits,
        n_layers=n_layers,
        num_classes=num_classes,
        learning_rate=learning_rate,
        dataset_info=dataset_info
    )

