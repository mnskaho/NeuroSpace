# """
# QRNN Qiskit - Point d'entrée principal
# Permet d'importer facilement la version clean ou noisy
# """

# # Version sans bruit (recommandée par défaut)
# from .clean.model import create_qiskit_qrnn_model as create_qiskit_qrnn_model_clean
# from .clean.trainer import train_qiskit_qrnn as train_qiskit_qrnn_clean

# # Version avec bruit + mitigation
# from .noisy.model import create_qiskit_qrnn_model as create_qiskit_qrnn_model_noisy
# from .noisy.trainer import train_qiskit_qrnn as train_qiskit_qrnn_noisy

# __all__ = [
#     # Clean (sans bruit)
#     'create_qiskit_qrnn_model_clean',
#     'train_qiskit_qrnn_clean',
    
#     # Noisy (avec bruit)
#     'create_qiskit_qrnn_model_noisy',
#     'train_qiskit_qrnn_noisy',
    
#     # Alias pratiques
#     'create_qiskit_qrnn_model',      # par défaut = clean
#     'train_qiskit_qrnn',
# ]

# # Alias par défaut (clean)
# create_qiskit_qrnn_model = create_qiskit_qrnn_model_clean
# train_qiskit_qrnn = train_qiskit_qrnn_clean

"""
QRNN Qiskit - Point d'entrée principal
Permet d'importer automatiquement clean ou noisy selon le bruit
"""

# Version sans bruit
from .clean.model import create_qiskit_qrnn_model as create_qiskit_qrnn_model_clean
from .clean.trainer import train_qiskit_qrnn as train_qiskit_qrnn_clean

# Version avec bruit
from .noisy.model import create_qiskit_qrnn_model as create_qiskit_qrnn_model_noisy
from .noisy.trainer import train_qiskit_qrnn as train_qiskit_qrnn_noisy


# 🔥 ROUTER INTELLIGENT
def create_qiskit_qrnn_model(n_qubits, num_classes=2, n_layers=3,
                            noise_level=0.0, mitigation_runs=1):
    """
    Choisit automatiquement clean ou noisy
    """
    if noise_level > 0:
        return create_qiskit_qrnn_model_noisy(
            n_qubits,
            num_classes,
            n_layers,
            noise_level,
            mitigation_runs
        )
    else:
        return create_qiskit_qrnn_model_clean(
            n_qubits,
            num_classes,
            n_layers
        )


def train_qiskit_qrnn(*args, noise_level=0.0, mitigation_runs=1, **kwargs):
    """
    Choisit automatiquement clean ou noisy pour l'entraînement
    """
    if noise_level > 0:
        return train_qiskit_qrnn_noisy(
            *args,
            noise_level=noise_level,
            mitigation_runs=mitigation_runs,
            **kwargs
        )
    else:
        return train_qiskit_qrnn_clean(*args, **kwargs)


__all__ = [
    # Clean
    "create_qiskit_qrnn_model_clean",
    "train_qiskit_qrnn_clean",

    # Noisy
    "create_qiskit_qrnn_model_noisy",
    "train_qiskit_qrnn_noisy",

    # Auto
    "create_qiskit_qrnn_model",
    "train_qiskit_qrnn",
]
