# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# try:
#     from qiskit.algorithms.optimizers import SPSA
#     HAS_SPSA = True
# except ImportError:
#     HAS_SPSA = False
#     print("⚠️ SPSA not available. Install qiskit-algorithms: pip install qiskit-algorithms")

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Entraîneur spécifique pour Qiskit QRNN avec SPSA pour les paramètres quantiques
#     et Adam pour la couche classique finale.
    
#     Args:
#         model: QiskitQRNN model
#         X_train, y_train: training data
#         X_val, y_val: validation data
#         epochs: number of epochs (pour SPSA)
#         batch_size: batch size (pour la couche FC)
#         lr: learning rate (pour la couche FC)
#         verbose: print progress
    
#     Returns:
#         history: training history
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     if not HAS_SPSA:
#         logger.warning("SPSA not available. Quantum weights will not be optimized!")
#         spsa_available = False
#     else:
#         spsa_available = True
    
#     # Convertir les données en tenseurs PyTorch
#     X_train_tensor = torch.FloatTensor(X_train).to(device)
#     y_train_tensor = torch.LongTensor(y_train).to(device)
#     X_val_tensor = torch.FloatTensor(X_val).to(device)
#     y_val_tensor = torch.LongTensor(y_val).to(device)
    
#     # Optimiseur classique pour la couche FC (Adam)
#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     history = {
#         'train_loss': [], 'train_acc': [],
#         'val_loss': [], 'val_acc': [],
#         'quantum_loss': []
#     }
    
#     # ============================================
#     # 1. Entraînement des paramètres quantiques avec SPSA
#     # ============================================
#     if spsa_available:
#         logger.info("🔮 Optimisation des paramètres quantiques avec SPSA...")
        
#         # Récupérer les poids quantiques initiaux
#         initial_weights = model.get_quantum_weights_numpy()
        
#         # Définir la fonction de loss pour SPSA (sur l'ensemble d'entraînement complet)
#         def quantum_loss_fn(weights):
#             """Fonction de loss pour SPSA (sans gradient)"""
#             model.eval()
            
#             # Mettre à jour les poids quantiques
#             model.set_quantum_weights_numpy(weights)
            
#             # Forward pass complet
#             with torch.no_grad():
#                 outputs = model(X_train_tensor, quantum_weights=weights)
#                 loss = criterion(outputs, y_train_tensor)
            
#             return loss.item()
        
#         # Configurer SPSA
#         spsa = SPSA(
#             maxiter=epochs,
#             learning_rate=lr * 10,  # SPSA a besoin d'un learning rate plus élevé
#             perturbation=0.01,      # Amplitude de la perturbation
#             last_avg=1              # Moyenne des dernières itérations
#         )
        
#         # Optimiser avec SPSA
#         logger.info(f"   Lancement SPSA pour {epochs} itérations...")
        
#         opt_weights, opt_value, _ = spsa.optimize(
#             num_vars=len(initial_weights),
#             objective_function=quantum_loss_fn,
#             initial_point=initial_weights
#         )
        
#         # Appliquer les poids optimisés
#         model.set_quantum_weights_numpy(opt_weights)
        
#         logger.info(f"   ✅ SPSA terminé - Loss finale: {opt_value:.4f}")
#         history['quantum_loss'].append(opt_value)
    
#     # ============================================
#     # 2. Entraînement de la couche classique FC
#     # ============================================
#     logger.info("📈 Optimisation de la couche classique avec Adam...")
    
#     # Freezer les poids quantiques (plus de modifications)
#     model.quantum_weights.requires_grad = False
    
#     # DataLoaders pour l'entraînement de la FC
#     train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
#     val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     fc_epochs = 30  # Époques supplémentaires pour la couche FC
    
#     for epoch in range(fc_epochs):
#         # Training
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             fc_optimizer.zero_grad()
            
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             fc_optimizer.step()
            
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
#             logger.info(f"   Epoch FC {epoch+1}/{fc_epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
#     # Évaluation finale
#     model.eval()
#     with torch.no_grad():
#         final_outputs = model(X_val_tensor)
#         _, final_pred = torch.max(final_outputs, 1)
#         final_acc = (final_pred == y_val_tensor).sum().item() / len(y_val_tensor)
    
#     logger.info(f"✅ Qiskit QRNN entraîné - Accuracy finale: {final_acc:.4f}")
    
#     return history


# def train_qiskit_qrnn_alternative(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Version alternative: entraîne SPSA et FC en parallèle (batch par batch)
#     Plus lent mais potentiellement meilleur.
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     if not HAS_SPSA:
#         logger.warning("SPSA not available. Quantum weights will not be optimized!")
#         spsa_available = False
#     else:
#         spsa_available = True
    
#     # Optimiseur classique
#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     # DataLoaders
#     train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
#     val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
#     if spsa_available:
#         # Configurer SPSA
#         spsa = SPSA(maxiter=epochs * len(train_loader), learning_rate=lr * 5, perturbation=0.01)
#         current_weights = model.get_quantum_weights_numpy()
        
#         # Fonction de loss pour un batch
#         def batch_loss_fn(weights, X_batch, y_batch):
#             model.set_quantum_weights_numpy(weights)
#             model.eval()
#             with torch.no_grad():
#                 outputs = model(X_batch, quantum_weights=weights)
#                 loss = criterion(outputs, y_batch)
#             return loss.item()
    
#     for epoch in range(epochs):
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
#             # Mettre à jour les poids quantiques avec SPSA (sur le batch)
#             if spsa_available:
#                 def partial_loss_fn(weights):
#                     return batch_loss_fn(weights, X_batch, y_batch)
                
#                 opt_weights, _, _ = spsa.optimize(
#                     num_vars=len(current_weights),
#                     objective_function=partial_loss_fn,
#                     initial_point=current_weights
#                 )
#                 model.set_quantum_weights_numpy(opt_weights)
#                 current_weights = opt_weights
            
#             # Mettre à jour la couche FC
#             fc_optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             fc_optimizer.step()
            
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

# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# try:
#     from qiskit.algorithms.optimizers import SPSA
#     HAS_SPSA = True
# except ImportError:
#     HAS_SPSA = False
#     print("⚠️ SPSA not available. Install qiskit-algorithms: pip install qiskit-algorithms")

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Entraîneur spécifique pour Qiskit QRNN avec SPSA pour les paramètres quantiques
#     et Adam pour la couche classique finale.
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     if not HAS_SPSA:
#         logger.warning("SPSA not available. Install qiskit-algorithms")
#         logger.warning("Quantum weights will NOT be optimized!")
#         spsa_available = False
#     else:
#         spsa_available = True
    
#     # Convertir les données en tenseurs PyTorch
#     X_train_tensor = torch.FloatTensor(X_train).to(device)
#     y_train_tensor = torch.LongTensor(y_train).to(device)
#     X_val_tensor = torch.FloatTensor(X_val).to(device)
#     y_val_tensor = torch.LongTensor(y_val).to(device)
    
#     # Optimiseur classique pour la couche FC (Adam)
#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     history = {
#         'train_loss': [], 'train_acc': [],
#         'val_loss': [], 'val_acc': [],
#         'quantum_loss': []
#     }
    
#     # ============================================
#     # 1. Entraînement des paramètres quantiques avec SPSA
#     # ============================================
#     if spsa_available:
#         logger.info("🔮 Optimisation des paramètres quantiques avec SPSA...")
        
#         # Récupérer les poids quantiques initiaux
#         initial_weights = model.get_quantum_weights_numpy()
        
#         # Définir la fonction de loss pour SPSA
#         def quantum_loss_fn(weights):
#             model.eval()
#             model.set_quantum_weights_numpy(weights)
#             with torch.no_grad():
#                 outputs = model(X_train_tensor, quantum_weights=weights)
#                 loss = criterion(outputs, y_train_tensor)
#             return loss.item()
        
#         # Configurer SPSA
#         spsa = SPSA(
#             maxiter=epochs,
#             learning_rate=lr * 10,
#             perturbation=0.01,
#             last_avg=1
#         )
        
#         logger.info(f"   Lancement SPSA pour {epochs} itérations...")
        
#         try:
#             opt_weights, opt_value, _ = spsa.optimize(
#                 num_vars=len(initial_weights),
#                 objective_function=quantum_loss_fn,
#                 initial_point=initial_weights
#             )
            
#             # Appliquer les poids optimisés
#             model.set_quantum_weights_numpy(opt_weights)
#             logger.info(f"   ✅ SPSA terminé - Loss finale: {opt_value:.4f}")
#             history['quantum_loss'].append(opt_value)
#         except Exception as e:
#             logger.error(f"   ❌ SPSA error: {e}")
#             logger.warning("   Using initial quantum weights")
    
#     # ============================================
#     # 2. Entraînement de la couche classique FC
#     # ============================================
#     logger.info("📈 Optimisation de la couche classique avec Adam...")
    
#     # Freezer les poids quantiques
#     model.quantum_weights.requires_grad = False
    
#     # DataLoaders
#     train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
#     val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     fc_epochs = 30
    
#     for epoch in range(fc_epochs):
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             fc_optimizer.zero_grad()
            
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             fc_optimizer.step()
            
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
        
#         if verbose and (epoch + 1) % 10 == 0:
#             logger.info(f"   Epoch FC {epoch+1}/{fc_epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
#     # Évaluation finale
#     model.eval()
#     with torch.no_grad():
#         final_outputs = model(X_val_tensor)
#         _, final_pred = torch.max(final_outputs, 1)
#         final_acc = (final_pred == y_val_tensor).sum().item() / len(y_val_tensor)
    
#     logger.info(f"✅ Qiskit QRNN entraîné - Accuracy finale: {final_acc:.4f}")
    
#     return history


# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# # 🔥 IMPORT CORRECT POUR SPSA (qiskit_algorithms, pas qiskit.algorithms)
# try:
#     from qiskit_algorithms.optimizers import SPSA
#     HAS_SPSA = True
#     print("✅ SPSA imported successfully")
# except ImportError:
#     try:
#         from qiskit.algorithms.optimizers import SPSA
#         HAS_SPSA = True
#         print("✅ SPSA imported from qiskit.algorithms")
#     except ImportError:
#         HAS_SPSA = False
#         print("⚠️ SPSA not available. Install: pip install qiskit-algorithms")

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Entraîneur spécifique pour Qiskit QRNN avec SPSA pour les paramètres quantiques
#     et Adam pour la couche classique finale.
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     if not HAS_SPSA:
#         logger.warning("SPSA not available. Quantum weights will NOT be optimized!")
#         logger.warning("Install: pip install qiskit-algorithms")
#         spsa_available = False
#     else:
#         spsa_available = True
    
#     # Convertir les données en tenseurs PyTorch
#     X_train_tensor = torch.FloatTensor(X_train).to(device)
#     y_train_tensor = torch.LongTensor(y_train).to(device)
#     X_val_tensor = torch.FloatTensor(X_val).to(device)
#     y_val_tensor = torch.LongTensor(y_val).to(device)
    
#     # Optimiseur classique pour la couche FC (Adam)
#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     history = {
#         'train_loss': [], 'train_acc': [],
#         'val_loss': [], 'val_acc': [],
#         'quantum_loss': []
#     }
    
#     # ============================================
#     # 1. Entraînement des paramètres quantiques avec SPSA
#     # ============================================
#     if spsa_available:
#         logger.info("🔮 Optimisation des paramètres quantiques avec SPSA...")
        
#         # Récupérer les poids quantiques initiaux
#         initial_weights = model.get_quantum_weights_numpy()
#         logger.info(f"   Nombre de paramètres quantiques: {len(initial_weights)}")
        
#         # Définir la fonction de loss pour SPSA
#         def quantum_loss_fn(weights):
#             model.eval()
#             model.set_quantum_weights_numpy(weights)
#             with torch.no_grad():
#                 outputs = model(X_train_tensor, quantum_weights=weights)
#                 loss = criterion(outputs, y_train_tensor)
#             return loss.item()
        
#         # Configurer SPSA
#         spsa = SPSA(
#             maxiter=epochs,
#             learning_rate=lr * 10,
#             perturbation=0.01,
#             last_avg=1
#         )
        
#         logger.info(f"   Lancement SPSA pour {epochs} itérations...")
        
#         try:
#             opt_weights, opt_value, _ = spsa.optimize(
#                 num_vars=len(initial_weights),
#                 objective_function=quantum_loss_fn,
#                 initial_point=initial_weights
#             )
            
#             # Appliquer les poids optimisés
#             model.set_quantum_weights_numpy(opt_weights)
#             logger.info(f"   ✅ SPSA terminé - Loss finale: {opt_value:.4f}")
#             history['quantum_loss'].append(opt_value)
#         except Exception as e:
#             logger.error(f"   ❌ SPSA error: {e}")
#             logger.warning("   Using initial quantum weights")
    
#     # ============================================
#     # 2. Entraînement de la couche classique FC
#     # ============================================
#     logger.info("📈 Optimisation de la couche classique avec Adam...")
    
#     # Freezer les poids quantiques
#     model.quantum_weights.requires_grad = False
    
#     # DataLoaders
#     train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
#     val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     fc_epochs = 30
    
#     for epoch in range(fc_epochs):
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             fc_optimizer.zero_grad()
            
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             fc_optimizer.step()
            
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
        
#         if verbose and (epoch + 1) % 10 == 0:
#             logger.info(f"   Epoch FC {epoch+1}/{fc_epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
#     # Évaluation finale
#     model.eval()
#     with torch.no_grad():
#         final_outputs = model(X_val_tensor)
#         _, final_pred = torch.max(final_outputs, 1)
#         final_acc = (final_pred == y_val_tensor).sum().item() / len(y_val_tensor)
    
#     logger.info(f"✅ Qiskit QRNN entraîné - Accuracy finale: {final_acc:.4f}")
    
#     return history


# def train_qiskit_qrnn_alternative(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Version alternative: entraîne SPSA et FC en parallèle (batch par batch)
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     if not HAS_SPSA:
#         logger.warning("SPSA not available. Quantum weights will not be optimized!")
#         spsa_available = False
#     else:
#         spsa_available = True
    
#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
#     val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
#     if spsa_available:
#         spsa = SPSA(maxiter=epochs * len(train_loader), learning_rate=lr * 5, perturbation=0.01)
#         current_weights = model.get_quantum_weights_numpy()
        
#         def batch_loss_fn(weights, X_batch, y_batch):
#             model.set_quantum_weights_numpy(weights)
#             model.eval()
#             with torch.no_grad():
#                 outputs = model(X_batch, quantum_weights=weights)
#                 loss = criterion(outputs, y_batch)
#             return loss.item()
    
#     for epoch in range(epochs):
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
#             if spsa_available:
#                 def partial_loss_fn(weights):
#                     return batch_loss_fn(weights, X_batch, y_batch)
                
#                 opt_weights, _, _ = spsa.optimize(
#                     num_vars=len(current_weights),
#                     objective_function=partial_loss_fn,
#                     initial_point=current_weights
#                 )
#                 model.set_quantum_weights_numpy(opt_weights)
#                 current_weights = opt_weights
            
#             fc_optimizer.zero_grad()
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             fc_optimizer.step()
            
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

#VERSION THAT WORKS  very well this one above or under i forgot anyway next __________________________________________#


# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# # 🔥 IMPORT CORRECT POUR SPSA (qiskit_algorithms)
# try:
#     from qiskit_algorithms.optimizers import SPSA
#     HAS_SPSA = True
#     print("✅ SPSA imported successfully")
# except ImportError:
#     try:
#         from qiskit.algorithms.optimizers import SPSA
#         HAS_SPSA = True
#         print("✅ SPSA imported from qiskit.algorithms")
#     except ImportError:
#         HAS_SPSA = False
#         print("⚠️ SPSA not available. Install: pip install qiskit-algorithms")

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     """
#     Entraîneur spécifique pour Qiskit QRNN avec SPSA pour les paramètres quantiques
#     et Adam pour la couche classique finale.
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     if not HAS_SPSA:
#         logger.warning("SPSA not available. Quantum weights will NOT be optimized!")
#         logger.warning("Install: pip install qiskit-algorithms")
#         spsa_available = False
#     else:
#         spsa_available = True
    
#     # Convertir les données en tenseurs PyTorch
#     X_train_tensor = torch.FloatTensor(X_train).to(device)
#     y_train_tensor = torch.LongTensor(y_train).to(device)
#     X_val_tensor = torch.FloatTensor(X_val).to(device)
#     y_val_tensor = torch.LongTensor(y_val).to(device)
    
#     # Optimiseur classique pour la couche FC (Adam)
#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     history = {
#         'train_loss': [], 'train_acc': [],
#         'val_loss': [], 'val_acc': [],
#         'quantum_loss': []
#     }
    
#     # ============================================
#     # 1. Entraînement des paramètres quantiques avec SPSA
#     # ============================================
#     if spsa_available:
#         logger.info("🔮 Optimisation des paramètres quantiques avec SPSA...")
        
#         # Récupérer les poids quantiques initiaux
#         initial_weights = model.get_quantum_weights_numpy()
#         logger.info(f"   Nombre de paramètres quantiques: {len(initial_weights)}")
        
#         # Définir la fonction de loss pour SPSA
#         def quantum_loss_fn(weights):
#             model.eval()
#             model.set_quantum_weights_numpy(weights)
#             with torch.no_grad():
#                 outputs = model(X_train_tensor, quantum_weights=weights)
#                 loss = criterion(outputs, y_train_tensor)
#             return loss.item()
        
#         # 🔥 CORRECTION: Utiliser .minimize() au lieu de .optimize()
#         spsa = SPSA(
#             maxiter=epochs,
#             learning_rate=lr * 10,
#             perturbation=0.01,
#             last_avg=1
#         )
        
#         logger.info(f"   Lancement SPSA pour {epochs} itérations...")
        
#         try:
#             # Nouvelle API qiskit_algorithms
#             result = spsa.minimize(
#                 fun=quantum_loss_fn,
#                 x0=initial_weights
#             )
            
#             opt_weights = result.x
#             opt_value = result.fun
            
#             # Appliquer les poids optimisés
#             model.set_quantum_weights_numpy(opt_weights)
#             logger.info(f"   ✅ SPSA terminé - Loss finale: {opt_value:.4f}")
#             history['quantum_loss'].append(opt_value)
#         except Exception as e:
#             logger.error(f"   ❌ SPSA error: {e}")
#             logger.warning("   Using initial quantum weights")
    
#     # ============================================
#     # 2. Entraînement de la couche classique FC
#     # ============================================
#     logger.info("📈 Optimisation de la couche classique avec Adam...")
    
#     # Freezer les poids quantiques
#     model.quantum_weights.requires_grad = False
    
#     # DataLoaders
#     train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
#     val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
#     fc_epochs = 30
    
#     for epoch in range(fc_epochs):
#         model.train()
#         train_loss = 0.0
#         train_correct = 0
#         train_total = 0
        
#         for X_batch, y_batch in train_loader:
#             X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#             fc_optimizer.zero_grad()
            
#             outputs = model(X_batch)
#             loss = criterion(outputs, y_batch)
#             loss.backward()
#             fc_optimizer.step()
            
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
        
#         if verbose and (epoch + 1) % 10 == 0:
#             logger.info(f"   Epoch FC {epoch+1}/{fc_epochs} - train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
#     # Évaluation finale
#     model.eval()
#     with torch.no_grad():
#         final_outputs = model(X_val_tensor)
#         _, final_pred = torch.max(final_outputs, 1)
#         final_acc = (final_pred == y_val_tensor).sum().item() / len(y_val_tensor)
    
#     logger.info(f"✅ Qiskit QRNN entraîné - Accuracy finale: {final_acc:.4f}")
    
#     return history


#NEW VERSION TRAINER FLEXIBLE ________________________________________________________________________________________#

# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import numpy as np
# import logging

# try:
#     from qiskit_algorithms.optimizers import SPSA
#     HAS_SPSA = True
#     print("✅ SPSA imported successfully")
# except ImportError:
#     try:
#         from qiskit.algorithms.optimizers import SPSA
#         HAS_SPSA = True
#         print("✅ SPSA imported from qiskit.algorithms")
#     except ImportError:
#         HAS_SPSA = False
#         print("⚠️ SPSA not available. Install: pip install qiskit-algorithms")

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=None, batch_size=32, 
#                       lr=None, verbose=True):
#     """
#     Entraîneur Qiskit QRNN Clean - Adaptatif
#     """
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
    
#     if lr is None:
#         lr = getattr(model, 'learning_rate', 0.001)
#     if epochs is None:
#         epochs = getattr(model, 'epochs', 20)
    
#     fc_epochs = getattr(model, 'fc_epochs', max(20, min(50, epochs // 2)))
    
#     spsa_available = HAS_SPSA
    
#     X_train_tensor = torch.FloatTensor(X_train).to(device)
#     y_train_tensor = torch.LongTensor(y_train).to(device)
#     X_val_tensor = torch.FloatTensor(X_val).to(device)
#     y_val_tensor = torch.LongTensor(y_val).to(device)
    
#     fc_optimizer = optim.Adam(model.fc.parameters(), lr=lr)
#     criterion = nn.CrossEntropyLoss()
    
#     history = {
#         'train_loss': [], 'train_acc': [],
#         'val_loss': [], 'val_acc': [],
#         'quantum_loss': []
#     }
    
#     logger.info(f"📊 Qiskit Clean: SPSA={epochs} itérations, FC={fc_epochs} époques (early stopping)")
    
#     # SPSA
#     if spsa_available:
#         logger.info("🔮 Optimisation des paramètres quantiques avec SPSA...")
#         initial_weights = model.get_quantum_weights_numpy()
        
#         spsa_batch_size = min(64, len(X_train))
        
#         def quantum_loss_fn(weights):
#             model.eval()
#             model.set_quantum_weights_numpy(weights)
#             idx = np.random.choice(len(X_train_tensor), size=spsa_batch_size, replace=False)
#             X_batch = X_train_tensor[idx]
#             y_batch = y_train_tensor[idx]
#             with torch.no_grad():
#                 outputs = model(X_batch, quantum_weights=weights)
#                 loss = criterion(outputs, y_batch)
#             return loss.item()
        
#         spsa_lr = min(0.05, lr * 3)
#         spsa = SPSA(maxiter=epochs, learning_rate=spsa_lr, perturbation=0.01, last_avg=1)
#         logger.info(f"   Lancement SPSA pour {epochs} itérations (lr={spsa_lr:.5f}, batch={spsa_batch_size})...")
        
#         try:
#             result = spsa.minimize(fun=quantum_loss_fn, x0=initial_weights)
#             model.set_quantum_weights_numpy(result.x)
#             logger.info(f"   ✅ SPSA terminé - Loss finale: {result.fun:.4f}")
#             history['quantum_loss'].append(result.fun)
#         except Exception as e:
#             logger.error(f"   ❌ SPSA error: {e}")
#             logger.warning("⚠️ Entraînement FC avec poids quantiques initiaux (non optimisés)")
    
#     # FC Layer + Early Stopping
#     logger.info(f"📈 Optimisation de la couche classique avec Adam ({fc_epochs} max)...")
#     model.quantum_weights.requires_grad = False
    
#     train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
#     val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
#     train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
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
#             _, predicted = torch.max(outputs, 1)
#             train_total += y_batch.size(0)
#             train_correct += (predicted == y_batch).sum().item()
        
#         train_acc = train_correct / train_total
        
#         model.eval()
#         val_loss, val_correct, val_total = 0.0, 0, 0
#         with torch.no_grad():
#             for X_batch, y_batch in val_loader:
#                 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
#                 outputs = model(X_batch)
#                 loss = criterion(outputs, y_batch)
#                 val_loss += loss.item() * X_batch.size(0)
#                 _, predicted = torch.max(outputs, 1)
#                 val_total += y_batch.size(0)
#                 val_correct += (predicted == y_batch).sum().item()
        
#         val_acc = val_correct / val_total
        
#         history['train_loss'].append(train_loss / train_total)
#         history['train_acc'].append(train_acc)
#         history['val_loss'].append(val_loss / val_total)
#         history['val_acc'].append(val_acc)
        
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
#             logger.info(f"   Epoch FC {epoch+1}/{fc_epochs} - train_acc: {train_acc:.4f}, "
#                        f"val_acc: {val_acc:.4f} | patience: {patience_counter}/{patience}")
        
#         if patience_counter >= patience:
#             logger.info(f"⏹️ Early stopping à l'epoch {epoch+1} (best val_acc: {best_val_acc:.4f})")
#             break
    
#     if best_state is not None:
#         model.fc.load_state_dict(best_state['fc_state'])
#         logger.info(f"🔄 Meilleur état restauré (epoch {best_state['epoch']})")
    
#     model.eval()
#     with torch.no_grad():
#         final_outputs = model(X_val_tensor)
#         _, final_pred = torch.max(final_outputs, 1)
#         final_acc = (final_pred == y_val_tensor).sum().item() / len(y_val_tensor)
    
#     logger.info(f"✅ Qiskit QRNN entraîné - Accuracy finale: {final_acc:.4f}")
#     return history

#NEW VERSION WITH CLASS WEIGHT FOR FLEXIBILITY GPT 5 ________________________________________________________________________________________#

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import logging

try:
    from qiskit_algorithms.optimizers import SPSA
    HAS_SPSA = True
except ImportError:
    try:
        from qiskit.algorithms.optimizers import SPSA
        HAS_SPSA = True
    except ImportError:
        HAS_SPSA = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_qiskit_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, 
                      lr=None, class_weights=None, verbose=True):
    """
    Entraîneur Qiskit QRNN Clean - Adaptatif
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    if lr is None:
        lr = getattr(model, 'learning_rate', 0.001)
    if epochs is None:
        epochs = getattr(model, 'epochs', 20)
    
    fc_epochs = getattr(model, 'fc_epochs', max(20, min(50, epochs // 2)))
    spsa_available = HAS_SPSA
    
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
    
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': [], 'quantum_loss': []}
    
    logger.info(f"📊 Qiskit Clean: SPSA={epochs}, FC={fc_epochs}")
    
    if spsa_available:
        logger.info("🔮 SPSA...")
        initial_weights = model.get_quantum_weights_numpy()
        spsa_batch_size = min(64, len(X_train))
        
        def quantum_loss_fn(weights):
            model.eval()
            model.set_quantum_weights_numpy(weights)
            idx = np.random.choice(len(X_train_tensor), size=spsa_batch_size, replace=False)
            with torch.no_grad():
                outputs = model(X_train_tensor[idx], quantum_weights=weights)
                loss = criterion(outputs, y_train_tensor[idx])
            return loss.item()
        
        spsa_lr = min(0.05, lr * 3)
        spsa = SPSA(maxiter=epochs, learning_rate=spsa_lr, perturbation=0.01, last_avg=1)
        
        try:
            result = spsa.minimize(fun=quantum_loss_fn, x0=initial_weights)
            model.set_quantum_weights_numpy(result.x)
            logger.info(f"✅ SPSA terminé - Loss: {result.fun:.4f}")
            history['quantum_loss'].append(result.fun)
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
            _, predicted = torch.max(outputs, 1)
            train_total += y_batch.size(0)
            train_correct += (predicted == y_batch).sum().item()
        
        train_acc = train_correct / train_total
        
        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                val_loss += loss.item() * X_batch.size(0)
                _, predicted = torch.max(outputs, 1)
                val_total += y_batch.size(0)
                val_correct += (predicted == y_batch).sum().item()
        
        val_acc = val_correct / val_total
        
        history['train_loss'].append(train_loss / train_total)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss / val_total)
        history['val_acc'].append(val_acc)
        
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
    
    model.eval()
    with torch.no_grad():
        final_outputs = model(X_val_tensor)
        _, final_pred = torch.max(final_outputs, 1)
        final_acc = (final_pred == y_val_tensor).sum().item() / len(y_val_tensor)
    
    logger.info(f"✅ Qiskit QRNN - Accuracy finale: {final_acc:.4f}")
    return history