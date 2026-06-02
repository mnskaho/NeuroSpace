# """
# Quantum RNN Models - Multi-backend support
# """

# def get_qrnn_model(backend='pennylane', n_qubits=4, n_layers=3, num_classes=2):
#     """
#     Factory function to get QRNN model based on backend
    
#     Args:
#         backend: 'pennylane', 'qiskit', or 'tfq'
#         n_qubits: number of qubits
#         n_layers: number of variational layers
#         num_classes: number of output classes
#     """
#     if backend == 'pennylane':
#         from .pennylane.model import QRNNClassifier, create_qrnn_model
#         return create_qrnn_model(n_qubits, num_classes, n_layers)
    
#     elif backend == 'qiskit':
#         from .qiskit.model import QiskitQRNN, create_qiskit_qrnn_model
#         return create_qiskit_qrnn_model(n_qubits, num_classes, n_layers)
    
#     elif backend == 'tfq':
#         from .tfq.model import TFQQRNN, create_tfq_qrnn_model
#         return create_tfq_qrnn_model(n_qubits, num_classes, n_layers)
    
#     else:
#         raise ValueError(f"Unknown backend: {backend}. Choose 'pennylane', 'qiskit', or 'tfq'")


# def get_qrnn_trainer(backend='pennylane'):
#     """
#     Factory function to get QRNN trainer based on backend
#     """
#     if backend == 'pennylane':
#         from .pennylane.trainer import train_qrnn
#         return train_qrnn
    
#     elif backend == 'qiskit':
#         from .qiskit.trainer import train_qiskit_qrnn
#         return train_qiskit_qrnn
    
#     elif backend == 'tfq':
#         from .tfq.trainer import train_tfq_qrnn
#         return train_tfq_qrnn
    
#     else:
#         raise ValueError(f"Unknown backend: {backend}")
# ml_pipeline/models/__init__.py
#OLD VERSION
# ml_pipeline/models/__init__.py
# from .rnn_model import RNNClassifier, create_rnn_model

# __all__ = ['RNNClassifier', 'create_rnn_model']

# QRNN module

from .pennylane import create_qrnn_model, train_qrnn
from .qiskit import create_qiskit_qrnn_model, train_qiskit_qrnn

__all__ = [
    'create_qrnn_model',
    'train_qrnn',
    'create_qiskit_qrnn_model',
    'train_qiskit_qrnn'
]
