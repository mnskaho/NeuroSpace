# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)

#     optimizer = optim.Adam(model.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()

#     train_loader = DataLoader(TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train)), 
#                               batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val)), 
#                             batch_size=batch_size)

#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

#     logger.info(f"🚀 Entraînement PennyLane | Bruit gates={model.noise_level} | Mitigation runs={model.mitigation_runs}")

#     for epoch in range(epochs):
#         model.train()
#         train_loss, train_correct, train_total = 0.0, 0, 0
       
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             optimizer.step()
           
#             train_loss += loss.item() * X_batch.size(0)
#             _, pred = torch.max(outputs, 1)
#             train_total += y_batch.size(0)
#             train_correct += (pred == y_batch).sum().item()
       
#         train_acc = train_correct / train_total
#         history['train_acc'].append(train_acc)
#         history['train_loss'].append(train_loss / train_total)

#         model.eval()
#         val_loss, val_correct, val_total = 0.0, 0, 0
#         with torch.no_grad():
#             for X_batch, y_batch in val_loader:
#                 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#                 outputs = model(X_batch)
#                 loss = criterion(outputs, y_batch)
#                 val_loss += loss.item() * X_batch.size(0)
#                 _, pred = torch.max(outputs, 1)
#                 val_total += y_batch.size(0)
#                 val_correct += (pred == y_batch).sum().item()
       
#         val_acc = val_correct / val_total
#         history['val_acc'].append(val_acc)
#         history['val_loss'].append(val_loss / val_total)

#         if verbose and (epoch + 1) % 5 == 0:
#             logger.info(f"Epoch {epoch+1}/{epochs} - Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

#     logger.info(f"✅ PennyLane QRNN terminé - Val Accuracy finale: {history['val_acc'][-1]:.4f}")
#     return history

#ANOTHER CODE JUST TO DO COMPARAISON NOISY VS WITH MITIGATION 
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def predict_with_averaging(model, X, runs=10):
#     """
#     Prédiction avec averaging pour mitigation du bruit
#     """
#     all_probs = []
#     for _ in range(runs):
#         probs = model.predict_proba(X)
#         all_probs.append(probs)
#     return np.mean(all_probs, axis=0)


# def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Entraîneur spécifique pour PennyLane QRNN Noisy
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)

#     optimizer = optim.Adam(model.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()

#     train_loader = DataLoader(TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train)), 
#                               batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val)), 
#                             batch_size=batch_size)

#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

#     logger.info(f"🚀 Entraînement PennyLane NOISY | Bruit gates={model.noise_level} | Mitigation runs={model.mitigation_runs}")

#     for epoch in range(epochs):
#         model.train()
#         train_loss, train_correct, train_total = 0.0, 0, 0
       
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             optimizer.step()
           
#             train_loss += loss.item() * X_batch.size(0)
#             _, pred = torch.max(outputs, 1)
#             train_total += y_batch.size(0)
#             train_correct += (pred == y_batch).sum().item()
       
#         train_acc = train_correct / train_total
#         history['train_acc'].append(train_acc)
#         history['train_loss'].append(train_loss / train_total)

#         model.eval()
#         val_loss, val_correct, val_total = 0.0, 0, 0
#         with torch.no_grad():
#             for X_batch, y_batch in val_loader:
#                 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#                 outputs = model(X_batch)
#                 loss = criterion(outputs, y_batch)
#                 val_loss += loss.item() * X_batch.size(0)
#                 _, pred = torch.max(outputs, 1)
#                 val_total += y_batch.size(0)
#                 val_correct += (pred == y_batch).sum().item()
       
#         val_acc = val_correct / val_total
#         history['val_acc'].append(val_acc)
#         history['val_loss'].append(val_loss / val_total)

#         if verbose and (epoch + 1) % 5 == 0:
#             logger.info(f"Epoch {epoch+1}/{epochs} - Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

#     logger.info(f"✅ PennyLane QRNN NOISY terminé - Val Accuracy finale: {history['val_acc'][-1]:.4f}")
    
#     return history

#NEW CODE FOR FLEXIBILITY IN TRAINING WITH OR WITHOUT MITIGATION_______________________________________________________________________________________#

# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def predict_with_averaging(model, X, runs=10):
#     all_probs = []
#     for _ in range(runs):
#         probs = model.predict_proba(X)
#         all_probs.append(probs)
#     return np.mean(all_probs, axis=0)


# def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=None, batch_size=32, 
#                lr=None, verbose=True):
#     """
#     Entraîneur PennyLane QRNN Noisy - Adaptatif
    
#     Args:
#         model: QRNNClassifier
#         epochs: si None → utilise model.epochs (d'AdaptiveConfig)
#         lr: si None → utilise model.learning_rate
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)

#     if lr is None:
#         lr = getattr(model, 'learning_rate', 0.001)
#     if epochs is None:
#         epochs = getattr(model, 'epochs', 20)

#     optimizer = optim.Adam(model.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()

#     train_loader = DataLoader(
#         TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train)), 
#         batch_size=batch_size, shuffle=True
#     )
#     val_loader = DataLoader(
#         TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val)), 
#         batch_size=batch_size
#     )

#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

#     logger.info(f"🚀 Entraînement PennyLane NOISY | Bruit={model.noise_level} | "
#                 f"Mitigation={model.mitigation_runs} | epochs={epochs} | lr={lr}")

#     for epoch in range(epochs):
#         model.train()
#         train_loss, train_correct, train_total = 0.0, 0, 0
       
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
#             optimizer.step()
           
#             train_loss += loss.item() * X_batch.size(0)
#             _, pred = torch.max(outputs, 1)
#             train_total += y_batch.size(0)
#             train_correct += (pred == y_batch).sum().item()
       
#         train_acc = train_correct / train_total
#         history['train_acc'].append(train_acc)
#         history['train_loss'].append(train_loss / train_total)

#         model.eval()
#         val_loss, val_correct, val_total = 0.0, 0, 0
#         with torch.no_grad():
#             for X_batch, y_batch in val_loader:
#                 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#                 outputs = model(X_batch)
#                 loss = criterion(outputs, y_batch)
#                 val_loss += loss.item() * X_batch.size(0)
#                 _, pred = torch.max(outputs, 1)
#                 val_total += y_batch.size(0)
#                 val_correct += (pred == y_batch).sum().item()
       
#         val_acc = val_correct / val_total
#         history['val_acc'].append(val_acc)
#         history['val_loss'].append(val_loss / val_total)

#         if verbose and (epoch + 1) % 5 == 0:
#             logger.info(f"Epoch {epoch+1}/{epochs} - Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

#     logger.info(f"✅ PennyLane QRNN NOISY terminé - Val Accuracy: {history['val_acc'][-1]:.4f}")
#     return history


#NEW CODE WITH FLEXIBLE WITH WEIGHT CLASS VERSION TEST_______________________________________________________________________________________#

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def predict_with_averaging(model, X, runs=10):
    all_probs = []
    for _ in range(runs):
        probs = model.predict_proba(X)
        all_probs.append(probs)
    return np.mean(all_probs, axis=0)


def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, 
               lr=None, class_weights=None, verbose=True):
    """
    Entraîneur PennyLane QRNN Noisy - Adaptatif
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    if lr is None:
        lr = getattr(model, 'learning_rate', 0.001)
    if epochs is None:
        epochs = getattr(model, 'epochs', 20)

    # 🔥 FIX 4 : Class weights
    if class_weights is not None:
        weight_tensor = torch.tensor(class_weights, dtype=torch.float32).to(device)
        criterion = nn.CrossEntropyLoss(weight=weight_tensor)
        logger.info(f"⚖️ Weighted loss activée: {class_weights}")
    else:
        criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(model.parameters(), lr=lr)

    train_loader = DataLoader(
        TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train)), 
        batch_size=batch_size, shuffle=True
    )
    val_loader = DataLoader(
        TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val)), 
        batch_size=batch_size
    )

    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

    logger.info(f"🚀 Entraînement PennyLane NOISY | Bruit={model.noise_level} | "
                f"Mitigation={model.mitigation_runs} | epochs={epochs} | lr={lr}")

    for epoch in range(epochs):
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
       
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
           
            train_loss += loss.item() * X_batch.size(0)
            _, pred = torch.max(outputs, 1)
            train_total += y_batch.size(0)
            train_correct += (pred == y_batch).sum().item()
       
        train_acc = train_correct / train_total
        history['train_acc'].append(train_acc)
        history['train_loss'].append(train_loss / train_total)

        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                val_loss += loss.item() * X_batch.size(0)
                _, pred = torch.max(outputs, 1)
                val_total += y_batch.size(0)
                val_correct += (pred == y_batch).sum().item()
       
        val_acc = val_correct / val_total
        history['val_acc'].append(val_acc)
        history['val_loss'].append(val_loss / val_total)

        if verbose and (epoch + 1) % 5 == 0:
            logger.info(f"Epoch {epoch+1}/{epochs} - Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

    logger.info(f"✅ PennyLane QRNN NOISY terminé - Val Accuracy: {history['val_acc'][-1]:.4f}")
    return history