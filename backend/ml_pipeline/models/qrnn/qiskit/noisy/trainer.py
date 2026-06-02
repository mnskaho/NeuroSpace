# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# try:
#     from qiskit_algorithms.optimizers import SPSA
#     HAS_SPSA = True
# except ImportError:
#     HAS_SPSA = False

# def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)

#     X_train_tensor = torch.FloatTensor(X_train).to(device)
#     y_train_tensor = torch.LongTensor(y_train).to(device)
#     X_val_tensor = torch.FloatTensor(X_val).to(device)
#     y_val_tensor = torch.LongTensor(y_val).to(device)

#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()

#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

#     logger.info(f"🚀 Entraînement Qiskit | Bruit gates={model.noise_level} | Mitigation={model.mitigation_runs}")

#     # SPSA même avec bruit
#     if HAS_SPSA:
#         logger.info("🔮 Optimisation SPSA des poids quantiques...")
#         initial_weights = model.get_quantum_weights_numpy()

#         def quantum_loss_fn(weights):
#             model.eval()
#             model.set_quantum_weights_numpy(weights)
#             with torch.no_grad():
#                 outputs = model(X_train_tensor)
#                 return criterion(outputs, y_train_tensor).item()

#         spsa = SPSA(maxiter=epochs, learning_rate=lr*8, perturbation=0.01, last_avg=1)
#         result = spsa.minimize(fun=quantum_loss_fn, x0=initial_weights)
#         model.set_quantum_weights_numpy(result.x)
#         logger.info(f"✅ SPSA terminé - Loss: {result.fun:.4f}")

#     # Entraînement couche classique
#     model.quantum_weights.requires_grad = False
#     train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(TensorDataset(X_val_tensor, y_val_tensor), batch_size=batch_size)

#     for epoch in range(30):
#         model.train()
#         train_loss, train_correct, train_total = 0.0, 0, 0
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             fc_optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             fc_optimizer.step()
           
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

#         if verbose and (epoch + 1) % 10 == 0:
#             logger.info(f"Epoch {epoch+1}/30 - Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

#     logger.info(f"✅ Qiskit QRNN terminé - Val Accuracy finale: {history['val_acc'][-1]:.4f}")
#     return history


#NEW CODE WITH FLEXIBILITY FOR OPTIMIZER AND LOSS TEST ________________________________________________________________________#
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# try:
#     from qiskit_algorithms.optimizers import SPSA
#     HAS_SPSA = True
# except ImportError:
#     HAS_SPSA = False

# def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=None, batch_size=32, 
#                       lr=None, verbose=True):
#     """
#     Entraîneur Qiskit QRNN Noisy - Adaptatif
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)

#     if lr is None:
#         lr = getattr(model, 'learning_rate', 0.001)
#     if epochs is None:
#         epochs = getattr(model, 'epochs', 20)
    
#     fc_epochs = getattr(model, 'fc_epochs', max(20, min(50, epochs // 2)))

#     X_train_tensor = torch.FloatTensor(X_train).to(device)
#     y_train_tensor = torch.LongTensor(y_train).to(device)
#     X_val_tensor = torch.FloatTensor(X_val).to(device)
#     y_val_tensor = torch.LongTensor(y_val).to(device)

#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()

#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

#     logger.info(f"🚀 Entraînement Qiskit Noisy | Bruit={model.noise_level} | "
#                 f"Mitigation={model.mitigation_runs} | SPSA={epochs} | FC={fc_epochs} | lr={lr}")

#     # SPSA
#     if HAS_SPSA:
#         logger.info("🔮 Optimisation SPSA des poids quantiques...")
#         initial_weights = model.get_quantum_weights_numpy()
        
#         spsa_batch_size = min(64, len(X_train))

#         def quantum_loss_fn(weights):
#             model.eval()
#             model.set_quantum_weights_numpy(weights)
#             idx = np.random.choice(len(X_train_tensor), size=spsa_batch_size, replace=False)
#             X_batch = X_train_tensor[idx]
#             y_batch = y_train_tensor[idx]
#             with torch.no_grad():
#                 outputs = model(X_batch)
#                 return criterion(outputs, y_batch).item()

#         spsa_lr = min(0.05, lr * 3)
#         spsa = SPSA(maxiter=epochs, learning_rate=spsa_lr, perturbation=0.01, last_avg=1)
#         logger.info(f"   Lancement SPSA pour {epochs} itérations (lr={spsa_lr:.5f}, batch={spsa_batch_size})...")
        
#         try:
#             result = spsa.minimize(fun=quantum_loss_fn, x0=initial_weights)
#             model.set_quantum_weights_numpy(result.x)
#             logger.info(f"   ✅ SPSA terminé - Loss finale: {result.fun:.4f}")
#         except Exception as e:
#             logger.error(f"   ❌ SPSA error: {e}")
#             logger.warning("⚠️ Entraînement FC avec poids quantiques initiaux (non optimisés)")
#     else:
#         logger.warning("⚠️ SPSA non disponible - poids quantiques initiaux utilisés")

#     # FC Layer + Early Stopping
#     model.quantum_weights.requires_grad = False
#     train_loader = DataLoader(
#         TensorDataset(X_train_tensor, y_train_tensor), 
#         batch_size=batch_size, shuffle=True
#     )
#     val_loader = DataLoader(
#         TensorDataset(X_val_tensor, y_val_tensor), 
#         batch_size=batch_size
#     )

#     best_val_acc = 0.0
#     patience = 10
#     patience_counter = 0
#     best_state = None

#     for epoch in range(fc_epochs):
#         model.train()
#         train_loss, train_correct, train_total = 0.0, 0, 0
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             fc_optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
#             fc_optimizer.step()
           
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

#         if val_acc > best_val_acc:
#             best_val_acc = val_acc
#             patience_counter = 0
#             best_state = {
#                 'fc_state': model.fc.state_dict().copy(),
#                 'epoch': epoch + 1
#             }
#         else:
#             patience_counter += 1

#         if verbose and (epoch + 1) % 10 == 0:
#             logger.info(f"Epoch FC {epoch+1}/{fc_epochs} - Train Acc: {train_acc:.4f} | "
#                        f"Val Acc: {val_acc:.4f} | patience: {patience_counter}/{patience}")
        
#         if patience_counter >= patience:
#             logger.info(f"⏹️ Early stopping à l'epoch {epoch+1} (best val_acc: {best_val_acc:.4f})")
#             break

#     if best_state is not None:
#         model.fc.load_state_dict(best_state['fc_state'])
#         logger.info(f"🔄 Meilleur état restauré (epoch {best_state['epoch']})")

#     logger.info(f"✅ Qiskit QRNN Noisy terminé - Val Accuracy finale: {best_val_acc:.4f}")
#     return history

# NEW CODE WITH GPT5 FOR FLEXIBLE with weight class VERSION TEST_____________________________________________________________#

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from qiskit_algorithms.optimizers import SPSA
    HAS_SPSA = True
except ImportError:
    HAS_SPSA = False

def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, 
                      lr=None, class_weights=None, verbose=True):
    """
    Entraîneur Qiskit QRNN Noisy - Adaptatif
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    if lr is None:
        lr = getattr(model, 'learning_rate', 0.001)
    if epochs is None:
        epochs = getattr(model, 'epochs', 20)
    
    fc_epochs = getattr(model, 'fc_epochs', max(20, min(50, epochs // 2)))

    X_train_tensor = torch.FloatTensor(X_train).to(device)
    y_train_tensor = torch.LongTensor(y_train).to(device)
    X_val_tensor = torch.FloatTensor(X_val).to(device)
    y_val_tensor = torch.LongTensor(y_val).to(device)

    # 🔥 FIX 4 : Class weights
    if class_weights is not None:
        weight_tensor = torch.tensor(class_weights, dtype=torch.float32).to(device)
        criterion = nn.CrossEntropyLoss(weight=weight_tensor)
        logger.info(f"⚖️ Weighted loss activée: {class_weights}")
    else:
        criterion = nn.CrossEntropyLoss()

    fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

    logger.info(f"🚀 Qiskit Noisy | Bruit={model.noise_level} | Mit={model.mitigation_runs} | SPSA={epochs} | FC={fc_epochs}")

    if HAS_SPSA:
        logger.info("🔮 SPSA...")
        initial_weights = model.get_quantum_weights_numpy()
        spsa_batch_size = min(64, len(X_train))

        def quantum_loss_fn(weights):
            model.eval()
            model.set_quantum_weights_numpy(weights)
            idx = np.random.choice(len(X_train_tensor), size=spsa_batch_size, replace=False)
            with torch.no_grad():
                outputs = model(X_train_tensor[idx])
                return criterion(outputs, y_train_tensor[idx]).item()

        spsa_lr = min(0.05, lr * 3)
        spsa = SPSA(maxiter=epochs, learning_rate=spsa_lr, perturbation=0.01, last_avg=1)
        
        try:
            result = spsa.minimize(fun=quantum_loss_fn, x0=initial_weights)
            model.set_quantum_weights_numpy(result.x)
            logger.info(f"✅ SPSA terminé - Loss: {result.fun:.4f}")
        except Exception as e:
            logger.error(f"❌ SPSA error: {e}")

    model.quantum_weights.requires_grad = False
    train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val_tensor, y_val_tensor), batch_size=batch_size)

    best_val_acc = 0.0
    patience = 10
    patience_counter = 0
    best_state = None

    for epoch in range(fc_epochs):
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            fc_optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            fc_optimizer.step()
           
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

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            best_state = {'fc_state': model.fc.state_dict().copy(), 'epoch': epoch + 1}
        else:
            patience_counter += 1

        if verbose and (epoch + 1) % 10 == 0:
            logger.info(f"FC {epoch+1}/{fc_epochs} - train: {train_acc:.4f}, val: {val_acc:.4f} | patience: {patience_counter}/{patience}")
        
        if patience_counter >= patience:
            logger.info(f"⏹️ Early stopping à epoch {epoch+1} (best: {best_val_acc:.4f})")
            break

    if best_state is not None:
        model.fc.load_state_dict(best_state['fc_state'])

    logger.info(f"✅ Qiskit QRNN Noisy - Val Accuracy: {best_val_acc:.4f}")
    return history