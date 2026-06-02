# """
# QRNN PennyLane - Point d'entrée principal
# Permet d'importer facilement la version clean ou noisy
# """

# # Version sans bruit (recommandée par défaut)
# from .clean.model import create_qrnn_model as create_qrnn_model_clean
# from .clean.trainer import train_qrnn as train_qrnn_clean

# # Version avec bruit + mitigation
# from .noisy.model import create_qrnn_model as create_qrnn_model_noisy
# from .noisy.trainer import train_qrnn as train_qrnn_noisy

# __all__ = [
#     # Clean (sans bruit)
#     'create_qrnn_model_clean',
#     'train_qrnn_clean',
    
#     # Noisy (avec bruit)
#     'create_qrnn_model_noisy',
#     'train_qrnn_noisy',
    
#     # Alias pratiques
#     'create_qrnn_model',      # par défaut = clean
#     'train_qrnn',
# ]

# # Alias par défaut (clean)
# create_qrnn_model = create_qrnn_model_clean
# train_qrnn = train_qrnn_clean

#___________________________________________________________________________________________________________________________
# """
# QRNN PennyLane - Point d'entrée principal
# Permet d'importer automatiquement clean ou noisy selon le bruit
# """

# # Version sans bruit
# from .clean.model import create_qrnn_model as create_qrnn_model_clean
# from .clean.trainer import train_qrnn as train_qrnn_clean

# # Version avec bruit
# from .noisy.model import create_qrnn_model as create_qrnn_model_noisy
# from .noisy.trainer import train_qrnn as train_qrnn_noisy


# # 🔥 ROUTER INTELLIGENT (IMPORTANT)
# def create_qrnn_model(n_qubits, num_classes=2, n_layers=3,
#                      noise_level=0.0, mitigation_runs=1):
#     """
#     Choisit automatiquement clean ou noisy
#     """
#     if noise_level > 0:
#         return create_qrnn_model_noisy(
#             n_qubits,
#             num_classes,
#             n_layers,
#             noise_level,
#             mitigation_runs
#         )
#     else:
#         return create_qrnn_model_clean(
#             n_qubits,
#             num_classes,
#             n_layers
#         )


# def train_qrnn(*args, noise_level=0.0, mitigation_runs=1, **kwargs):
#     """
#     Choisit automatiquement clean ou noisy pour l'entraînement
#     """
#     if noise_level > 0:
#         return train_qrnn_noisy(
#             *args,
#             noise_level=noise_level,
#             mitigation_runs=mitigation_runs,
#             **kwargs
#         )
#     else:
#         return train_qrnn_clean(*args, **kwargs)


# __all__ = [
#     # Clean
#     "create_qrnn_model_clean",
#     "train_qrnn_clean",

#     # Noisy
#     "create_qrnn_model_noisy",
#     "train_qrnn_noisy",

#     # Auto (recommandé)
#     "create_qrnn_model",
#     "train_qrnn",
# ]


#NEWW CUZ OF ERROR FLOT 64 ABOVE TRYING THIS

# """
# QRNN PennyLane - Point d'entrée principal (routing clean / noisy)
# """
# from .clean.model import create_qrnn_model as create_clean
# from .clean.trainer import train_qrnn as train_clean
# from .noisy.model import create_qrnn_model as create_noisy
# from .noisy.trainer import train_qrnn as train_noisy


# def create_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1, learning_rate=0.001):
#     if noise_level > 0.0:
#         return create_noisy(
#             n_qubits=n_qubits,
#             num_classes=num_classes,
#             n_layers=n_layers,
#             learning_rate=learning_rate,
#             noise_level=noise_level,
#             mitigation_runs=mitigation_runs
#         )
#     else:
#         return create_clean(
#             n_qubits=n_qubits,
#             num_classes=num_classes,
#             n_layers=n_layers
#         )


# def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
#     if hasattr(model, 'noise_level') and model.noise_level > 0.0:
#         return train_noisy(model, X_train, y_train, X_val, y_val, epochs, batch_size, lr, verbose)
#     else:
#         return train_clean(model, X_train, y_train, X_val, y_val, epochs, batch_size, lr, verbose)


# __all__ = ['create_qrnn_model', 'train_qrnn']

#GROK CODE  POUR LR MISTAKE 
"""
QRNN PennyLane - Point d'entrée principal (routing clean / noisy)
Version corrigée - sans learning_rate dans create_noisy
"""

from .clean.model import create_qrnn_model as create_clean
from .clean.trainer import train_qrnn as train_clean
from .noisy.model import create_qrnn_model as create_noisy
from .noisy.trainer import train_qrnn as train_noisy


def create_qrnn_model(n_qubits, num_classes=2, n_layers=3, noise_level=0.0, mitigation_runs=1):
    """Factory unique - choisit clean ou noisy"""
    if noise_level > 0.0:
        # create_noisy n'accepte PAS learning_rate
        return create_noisy(
            n_qubits=n_qubits,
            num_classes=num_classes,
            n_layers=n_layers,
            noise_level=noise_level,
            mitigation_runs=mitigation_runs
        )
    else:
        return create_clean(
            n_qubits=n_qubits,
            num_classes=num_classes,
            n_layers=n_layers
        )


def train_qrnn(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32, lr=0.001, verbose=True):
    """Trainer unique selon le type de modèle"""
    if hasattr(model, 'noise_level') and model.noise_level > 0.0:
        return train_noisy(model, X_train, y_train, X_val, y_val, epochs, batch_size, lr, verbose)
    else:
        return train_clean(model, X_train, y_train, X_val, y_val, epochs, batch_size, lr, verbose)


__all__ = ['create_qrnn_model', 'train_qrnn']