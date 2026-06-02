# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Entraîneur spécifique pour PennyLane QRNN
    
#     Args:
#         model: QRNNClassifier model
#         X_train, y_train: training data
#         X_val, y_val: validation data
#         epochs: number of epochs
#         batch_size: batch size
#         lr: learning rate
#         verbose: print progress
    
#     Returns:
#         history: training history
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     # Optimiseur
#     optimizer = optim.Adam(model.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     # DataLoaders
#     train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
#     val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
#     for epoch in range(epochs):
#         # Training
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
            
#             # Clip gradient pour stabilité quantique
#             torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
#             optimizer.step()
            
#             train_loss += loss.item() * X_batch.size(0)
#             _, predicted = torch.max(outputs, 1)
#             train_total += y_batch.size(0)
#             train_correct += (predicted == y_batch).sum().item()
        
#         train_loss /= train_total
#         train_acc = train_correct / train_total
        
#         # Validation
#         model.eval()
#         val_loss = 0.0
#         val_correct = 0
#         val_total = 0
#         with torch.no_grad():
#             for X_batch, y_batch in val_loader:
#                 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#                 outputs = model(X_batch)
#                 loss = criterion(outputs, y_batch)
#                 val_loss += loss.item() * X_batch.size(0)
#                 _, predicted = torch.max(outputs, 1)
#                 val_total += y_batch.size(0)
#                 val_correct += (predicted == y_batch).sum().item()
        
#         val_loss /= val_total
#         val_acc = val_correct / val_total
        
#         history['train_loss'].append(train_loss)
#         history['train_acc'].append(train_acc)
#         history['val_loss'].append(val_loss)
#         history['val_acc'].append(val_acc)
        
#         if verbose and (epoch + 1) % 5 == 0:
#             logger.info(f"Epoch {epoch+1}/{epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
#     return history


#NEW FOR FLEXIBLE VERSION TEST_____________________________________________________________#

# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=None, batch_size=32, 
#                lr=None, verbose=True):
#     """
#     Entraîneur PennyLane QRNN Clean - Adaptatif
    
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
    
#     train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
#     val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
#     for epoch in range(epochs):
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
#             optimizer.step()
            
#             train_loss += loss.item() * X_batch.size(0)
#             _, predicted = torch.max(outputs, 1)
#             train_total += y_batch.size(0)
#             train_correct += (predicted == y_batch).sum().item()
        
#         train_loss /= train_total
#         train_acc = train_correct / train_total
        
#         model.eval()
#         val_loss = 0.0
#         val_correct = 0
#         val_total = 0
#         with torch.no_grad():
#             for X_batch, y_batch in val_loader:
#                 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#                 outputs = model(X_batch)
#                 loss = criterion(outputs, y_batch)
#                 val_loss += loss.item() * X_batch.size(0)
#                 _, predicted = torch.max(outputs, 1)
#                 val_total += y_batch.size(0)
#                 val_correct += (predicted == y_batch).sum().item()
        
#         val_loss /= val_total
#         val_acc = val_correct / val_total
        
#         history['train_loss'].append(train_loss)
#         history['train_acc'].append(train_acc)
#         history['val_loss'].append(val_loss)
#         history['val_acc'].append(val_acc)
        
#         if verbose and (epoch + 1) % 5 == 0:
#             logger.info(f"Epoch {epoch+1}/{epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
#     return history

#NEW CODE WITH GPT5 FOR FLEXIBLE + weight class VERSION TEST_____________________________________________________________#

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, 
               lr=None, class_weights=None, verbose=True):
    """
    Entraîneur PennyLane QRNN Clean - Adaptatif
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
    
    train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
    val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            train_loss += loss.item() * X_batch.size(0)
            _, predicted = torch.max(outputs, 1)
            train_total += y_batch.size(0)
            train_correct += (predicted == y_batch).sum().item()
        
        train_loss /= train_total
        train_acc = train_correct / train_total
        
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                val_loss += loss.item() * X_batch.size(0)
                _, predicted = torch.max(outputs, 1)
                val_total += y_batch.size(0)
                val_correct += (predicted == y_batch).sum().item()
        
        val_loss /= val_total
        val_acc = val_correct / val_total
        
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        if verbose and (epoch + 1) % 5 == 0:
            logger.info(f"Epoch {epoch+1}/{epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
    return history