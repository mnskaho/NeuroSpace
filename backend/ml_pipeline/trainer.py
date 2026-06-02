# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class Trainer:
#     """
#     Entraîneur de modèles avec gestion automatique du device
#     """
    
#     def __init__(self, model, device='cuda' if torch.cuda.is_available() else 'cpu'):
#         self.model = model.to(device)
#         self.device = device
#         self.criterion = nn.CrossEntropyLoss()

#     def train(self, X_train, y_train, X_val, y_val, epochs=30, batch_size=32, lr=0.001, verbose=True):
#         """Entraîne le modèle avec validation"""
        
#         # Créer les DataLoaders
#         train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
#         val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
#         train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#         val_loader = DataLoader(val_dataset, batch_size=batch_size)

#         # Optimiseur
#         optimizer = optim.Adam(self.model.parameters(), lr=lr)
        
#         history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
        
#         for epoch in range(epochs):
#             # Training
#             self.model.train()
#             train_loss = 0.0
#             train_correct = 0
#             train_total = 0
            
#             for X_batch, y_batch in train_loader:
#                 X_batch, y_batch = X_batch.to(self.device), y_batch.to(self.device)
#                 optimizer.zero_grad()
#                 outputs = self.model(X_batch)
#                 loss = self.criterion(outputs, y_batch)
#                 loss.backward()
#                 optimizer.step()
                
#                 train_loss += loss.item() * X_batch.size(0)
#                 _, predicted = torch.max(outputs, 1)
#                 train_total += y_batch.size(0)
#                 train_correct += (predicted == y_batch).sum().item()
            
#             train_loss /= train_total
#             train_acc = train_correct / train_total
            
#             # Validation
#             self.model.eval()
#             val_loss = 0.0
#             val_correct = 0
#             val_total = 0
#             with torch.no_grad():
#                 for X_batch, y_batch in val_loader:
#                     X_batch, y_batch = X_batch.to(self.device), y_batch.to(self.device)
#                     outputs = self.model(X_batch)
#                     loss = self.criterion(outputs, y_batch)
#                     val_loss += loss.item() * X_batch.size(0)
#                     _, predicted = torch.max(outputs, 1)
#                     val_total += y_batch.size(0)
#                     val_correct += (predicted == y_batch).sum().item()
            
#             val_loss /= val_total
#             val_acc = val_correct / val_total
            
#             history['train_loss'].append(train_loss)
#             history['val_loss'].append(val_loss)
#             history['train_acc'].append(train_acc)
#             history['val_acc'].append(val_acc)
            
#             if verbose and (epoch + 1) % 5 == 0:
#                 logger.info(f"Epoch {epoch+1}/{epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
        
#         return history
    
#     def predict(self, X):
#         """Prédit les classes pour X"""
#         self.model.eval()
#         X_tensor = torch.FloatTensor(X).to(self.device)
#         with torch.no_grad():
#             outputs = self.model(X_tensor)
#             _, predicted = torch.max(outputs, 1)
#         return predicted.cpu().numpy()
    
#     def predict_proba(self, X):
#         """Retourne les probabilités pour X"""
#         self.model.eval()
#         X_tensor = torch.FloatTensor(X).to(self.device)
#         with torch.no_grad():
#             outputs = self.model(X_tensor)
#             probabilities = torch.softmax(outputs, dim=1)
#         return probabilities.cpu().numpy()

#NEW CODE FOR MULTICLASS GPT5

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Trainer:
    """
    Entraîneur flexible pour classification binaire et multi-classe.

    Conditions:
    - Le modèle retourne des logits de shape (batch_size, num_classes)
    - Les labels sont encodés en 0..num_classes-1
    """

    def __init__(
        self,
        model,
        device="cuda" if torch.cuda.is_available() else "cpu",
        class_weights=None,
    ):
        self.model = model.to(device)
        self.device = device

        if class_weights is not None:
            weights_tensor = torch.tensor(class_weights, dtype=torch.float32).to(device)
            self.criterion = nn.CrossEntropyLoss(weight=weights_tensor)
        else:
            self.criterion = nn.CrossEntropyLoss()

    def train(
        self,
        X_train,
        y_train,
        X_val,
        y_val,
        epochs=None,
        batch_size=32,
        lr=None,
        verbose=True,
    ):
        """
        Entraîne le modèle.

        epochs:
        - si fourni par le worker/user, cette valeur est utilisée.
        - sinon fallback à 30.

        lr:
        - si fourni, cette valeur est utilisée.
        - sinon utilise model.learning_rate si disponible.
        - sinon fallback à 0.001.
        """
        if epochs is None:
            epochs = 30

        epochs = int(epochs)
        if epochs <= 0:
            raise ValueError("epochs doit être > 0")

        batch_size = int(batch_size)
        if batch_size <= 0:
            raise ValueError("batch_size doit être > 0")

        if lr is None:
            lr = getattr(self.model, "learning_rate", 0.001)

        lr = float(lr)

        X_train = np.asarray(X_train, dtype=np.float32)
        X_val = np.asarray(X_val, dtype=np.float32)

        y_train = np.asarray(y_train, dtype=np.int64)
        y_val = np.asarray(y_val, dtype=np.int64)

        if y_train.min() < 0 or y_val.min() < 0:
            raise ValueError("Les labels doivent être encodés en 0..num_classes-1.")

        train_dataset = TensorDataset(
            torch.FloatTensor(X_train),
            torch.LongTensor(y_train),
        )

        val_dataset = TensorDataset(
            torch.FloatTensor(X_val),
            torch.LongTensor(y_val),
        )

        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
        )

        optimizer = optim.Adam(self.model.parameters(), lr=lr)

        history = {
            "train_loss": [],
            "val_loss": [],
            "train_acc": [],
            "val_acc": [],
        }

        logger.info(
            f"Training started: epochs={epochs}, batch_size={batch_size}, lr={lr}, device={self.device}"
        )

        for epoch in range(epochs):
            self.model.train()

            train_loss = 0.0
            train_correct = 0
            train_total = 0

            for X_batch, y_batch in train_loader:
                X_batch = X_batch.to(self.device)
                y_batch = y_batch.to(self.device)

                optimizer.zero_grad()

                outputs = self.model(X_batch)

                if outputs.ndim != 2:
                    raise ValueError(
                        f"Sortie modèle invalide: attendu (batch, num_classes), reçu {outputs.shape}"
                    )

                loss = self.criterion(outputs, y_batch)

                loss.backward()
                optimizer.step()

                train_loss += loss.item() * X_batch.size(0)

                predicted = torch.argmax(outputs, dim=1)

                train_total += y_batch.size(0)
                train_correct += (predicted == y_batch).sum().item()

            train_loss = train_loss / max(train_total, 1)
            train_acc = train_correct / max(train_total, 1)

            self.model.eval()

            val_loss = 0.0
            val_correct = 0
            val_total = 0

            with torch.no_grad():
                for X_batch, y_batch in val_loader:
                    X_batch = X_batch.to(self.device)
                    y_batch = y_batch.to(self.device)

                    outputs = self.model(X_batch)

                    if outputs.ndim != 2:
                        raise ValueError(
                            f"Sortie modèle invalide: attendu (batch, num_classes), reçu {outputs.shape}"
                        )

                    loss = self.criterion(outputs, y_batch)

                    val_loss += loss.item() * X_batch.size(0)

                    predicted = torch.argmax(outputs, dim=1)

                    val_total += y_batch.size(0)
                    val_correct += (predicted == y_batch).sum().item()

            val_loss = val_loss / max(val_total, 1)
            val_acc = val_correct / max(val_total, 1)

            history["train_loss"].append(float(train_loss))
            history["val_loss"].append(float(val_loss))
            history["train_acc"].append(float(train_acc))
            history["val_acc"].append(float(val_acc))

            if verbose and ((epoch + 1) % 5 == 0 or epoch == 0 or epoch == epochs - 1):
                logger.info(
                    f"Epoch {epoch + 1}/{epochs} - "
                    f"train_loss: {train_loss:.4f}, "
                    f"val_loss: {val_loss:.4f}, "
                    f"train_acc: {train_acc:.4f}, "
                    f"val_acc: {val_acc:.4f}"
                )

        return history

    def predict(self, X):
        self.model.eval()

        X = np.asarray(X, dtype=np.float32)
        X_tensor = torch.FloatTensor(X).to(self.device)

        with torch.no_grad():
            outputs = self.model(X_tensor)

            if outputs.ndim != 2:
                raise ValueError(
                    f"Sortie modèle invalide: attendu (batch, num_classes), reçu {outputs.shape}"
                )

            predicted = torch.argmax(outputs, dim=1)

        return predicted.cpu().numpy()

    def predict_proba(self, X):
        self.model.eval()

        X = np.asarray(X, dtype=np.float32)
        X_tensor = torch.FloatTensor(X).to(self.device)

        with torch.no_grad():
            outputs = self.model(X_tensor)

            if outputs.ndim != 2:
                raise ValueError(
                    f"Sortie modèle invalide: attendu (batch, num_classes), reçu {outputs.shape}"
                )

            probabilities = torch.softmax(outputs, dim=1)

        return probabilities.cpu().numpy()