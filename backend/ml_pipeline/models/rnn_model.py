# import torch
# import torch.nn as nn
# import torch.optim as optim
# import numpy as np

# class RNNClassifier(nn.Module):
#     """
#     RNN Classique avec LSTM pour classification
#     """
    
#     def __init__(self, input_size, hidden_size=64, num_layers=2, num_classes=2, dropout=0.2, learning_rate=0.001):
#         super().__init__()
#         self.input_size = input_size
#         self.hidden_size = hidden_size
#         self.num_layers = num_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
        
#         self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
#         self.fc = nn.Linear(hidden_size, num_classes)
#         self.dropout = nn.Dropout(dropout)
        
#         self.optimizer = None
#         self.criterion = nn.CrossEntropyLoss()

#     def forward(self, x):
#         # Si x est 2D (batch, features), ajouter dimension temporelle
#         if len(x.shape) == 2:
#             x = x.unsqueeze(1)  # (batch, 1, input_size)
        
#         h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
#         c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
#         out, _ = self.lstm(x, (h0, c0))
#         out = self.dropout(out[:, -1, :])
#         out = self.fc(out)
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

# def create_rnn_model(input_size, num_classes, hidden_size=64, num_layers=2):
#     """Fonction de création du modèle RNN"""
#     return RNNClassifier(input_size, hidden_size, num_layers, num_classes)

#VERSION GROK POUR GPU
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset

# class RNNClassifier(nn.Module):
#     """
#     RNN Classique avec LSTM - Version finale GPU/CPU safe
#     """
#     def __init__(self, input_size, hidden_size=64, num_layers=2, num_classes=2, dropout=0.2, learning_rate=0.001):
#         super().__init__()
#         self.input_size = input_size
#         self.hidden_size = hidden_size
#         self.num_layers = num_layers
#         self.num_classes = num_classes
#         self.learning_rate = learning_rate
        
#         # LSTM + Dropout + FC
#         self.lstm = nn.LSTM(
#             input_size, 
#             hidden_size, 
#             num_layers, 
#             batch_first=True, 
#             dropout=dropout if num_layers > 1 else 0
#         )
#         self.fc = nn.Linear(hidden_size, num_classes)
#         self.dropout = nn.Dropout(dropout)

#     def forward(self, x):
#         # Si x est 2D (batch, features) → le transformer en (batch, seq=1, features)
#         if len(x.shape) == 2:
#             x = x.unsqueeze(1)
        
#         # Initialisation de l'état caché sur le même device que l'entrée
#         h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size, device=x.device)
#         c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size, device=x.device)
        
#         out, _ = self.lstm(x, (h0, c0))
#         out = self.dropout(out[:, -1, :])   # Prendre la dernière sortie
#         out = self.fc(out)
#         return out

#     def predict(self, X):
#         """Méthode predict utilisée par l'Evaluator"""
#         self.eval()
#         # Convertir en tensor et mettre sur le même device que les poids du modèle
#         X = torch.FloatTensor(X).to(self.fc.weight.device)
        
#         with torch.no_grad():
#             outputs = self(X)
#             _, predicted = torch.max(outputs, 1)
        
#         return predicted.cpu().numpy()

#     def predict_proba(self, X):
#         """Probabilités (optionnel)"""
#         self.eval()
#         X = torch.FloatTensor(X).to(self.fc.weight.device)
        
#         with torch.no_grad():
#             outputs = self(X)
#             probabilities = torch.softmax(outputs, dim=1)
        
#         return probabilities.cpu().numpy()


# def create_rnn_model(input_size, num_classes, hidden_size=64, num_layers=2):
#     """Fonction factory utilisée dans le worker"""
#     return RNNClassifier(input_size, hidden_size, num_layers, num_classes)

#NEWVERSION MLP FLEXIBLE ______________________________________________________________________________________#
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from ml_pipeline.adaptive_config import AdaptiveConfig


class RNNClassifier(nn.Module):
    """
    MLP Classifier avec ReLU - Version finale GPU/CPU safe
    Architecture: Input → Hidden Layers (ReLU + Dropout) → Output
    """
    def __init__(self, input_size, hidden_size=64, num_layers=2, num_classes=2, 
                 dropout=0.2, learning_rate=0.001):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.dropout = dropout  # ✅ Correction : self.dropout (pas dropout_rate)
        
        # Construction dynamique des couches MLP
        layers = []
        
        # Première couche : Input → Hidden
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(nn.ReLU())
        layers.append(nn.BatchNorm1d(hidden_size))
        layers.append(nn.Dropout(dropout))
        
        # Couches cachées : Hidden → Hidden (num_layers - 1 fois)
        for _ in range(num_layers - 1):
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.BatchNorm1d(hidden_size))
            layers.append(nn.Dropout(dropout))
        
        # Dernière couche : Hidden → Output
        layers.append(nn.Linear(hidden_size, num_classes))
        
        self.mlp = nn.Sequential(*layers)

    def forward(self, x):
        """
        Forward pass - Accepte 2D (batch, features) ou 3D (batch, seq, features)
        """
        # Si x est 3D (batch, seq, features) → aplatir en 2D
        if len(x.shape) == 3:
            x = x.reshape(x.size(0), -1)
        
        return self.mlp(x)

    def predict(self, X):
        """Méthode predict utilisée par l'Evaluator"""
        self.eval()
        # Convertir en tensor et mettre sur le même device que les poids du modèle
        X = torch.FloatTensor(X).to(next(self.parameters()).device)
        
        with torch.no_grad():
            outputs = self(X)
            _, predicted = torch.max(outputs, 1)
        
        return predicted.cpu().numpy()

    def predict_proba(self, X):
        """Probabilités (optionnel)"""
        self.eval()
        X = torch.FloatTensor(X).to(next(self.parameters()).device)
        
        with torch.no_grad():
            outputs = self(X)
            probabilities = torch.softmax(outputs, dim=1)
        
        return probabilities.cpu().numpy()


def create_rnn_model(input_size, num_classes, hidden_size=None, num_layers=None,
                     dropout=None, learning_rate=None, dataset_info=None):
    """
    Factory function pour créer un MLP avec paramètres adaptatifs
    
    Args:
        input_size: nombre de features en entrée
        num_classes: nombre de classes
        hidden_size: None = auto-calculé via AdaptiveConfig
        num_layers: None = auto-calculé via AdaptiveConfig
        dropout: None = auto-calculé via AdaptiveConfig
        learning_rate: None = auto-calculé via AdaptiveConfig
        dataset_info: dict optionnel pour l'adaptation automatique
    
    Returns:
        RNNClassifier (MLP) configuré
    """
    # Si dataset_info est fourni et que des paramètres sont None, utiliser AdaptiveConfig
    if dataset_info is not None:
        adaptive_params = AdaptiveConfig.compute_all_params(dataset_info)
        
        # ✅ Utiliser la structure PLATE de compute_all_params
        # Les clés sont : hidden_size, num_layers, dropout, learning_rate, etc.
        if hidden_size is None:
            hidden_size = adaptive_params.get('hidden_size', 64)
        if num_layers is None:
            num_layers = adaptive_params.get('num_layers', 2)
        if dropout is None:
            dropout = adaptive_params.get('dropout', 0.2)
        if learning_rate is None:
            learning_rate = adaptive_params.get('learning_rate', 0.001)
    
    # Valeurs par défaut si toujours None
    if hidden_size is None:
        # Taille adaptative selon input_size
        hidden_size = min(256, max(32, input_size * 4))
    if num_layers is None:
        num_layers = 2
    if dropout is None:
        dropout = 0.2
    if learning_rate is None:
        learning_rate = 0.001
    
    print(f"   ✅ MLP créé: input={input_size}, hidden={hidden_size}, "
          f"layers={num_layers}, dropout={dropout}, lr={learning_rate}")
    
    return RNNClassifier(
        input_size=input_size,
        hidden_size=hidden_size,
        num_layers=num_layers,
        num_classes=num_classes,
        dropout=dropout,
        learning_rate=learning_rate
    )