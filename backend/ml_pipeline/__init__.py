# """
# ML Pipeline for NeuroSpace - Quantum RNN Platform
# """

# from .preprocessing import DataPreprocessor
# from .evaluator import Evaluator
# from .trainer import Trainer
# from .report_generator import PDFReport, generate_report

# from .feature_engineering.mi_selector import MISelector
# from .feature_engineering.pca_reducer import PCAReducer

# from .models.rnn_model import RNNClassifier, create_rnn_model
# from .models.qrnn.pennylane_qrnn import QRNNClassifier, create_qrnn_model

# __all__ = [
#     'DataPreprocessor',
#     'Evaluator',
#     'Trainer',
#     'PDFReport',
#     'generate_report',
#     'MISelector',
#     'PCAReducer',
#     'RNNClassifier',
#     'create_rnn_model',
#     'QRNNClassifier',
#     'create_qrnn_model'
# ]

# """
# ML Pipeline for NeuroSpace - Quantum RNN Platform
# """

# from .preprocessing import DataPreprocessor
# from .evaluator import Evaluator
# from .trainer import Trainer
# from .report_generator import PDFReport, generate_report

# from .feature_engineering.mi_selector import MISelector
# from .feature_engineering.pca_reducer import PCAReducer

# # CORRECTION: importer depuis models/
# from .models.rnn_model import RNNClassifier, create_rnn_model
# from .models.qrnn.pennylane.model import QRNNClassifier, create_qrnn_model

# __all__ = [
#     'DataPreprocessor',
#     'Evaluator',
#     'Trainer',
#     'PDFReport',
#     'generate_report',
#     'MISelector',
#     'PCAReducer',
#     'RNNClassifier',
#     'create_rnn_model',
#     'QRNNClassifier',
#     'create_qrnn_model'
# ]

#OLD ONE THAT WORKS BEFORE NOISE IMPLEMENTATION

# """
# ML Pipeline for NeuroSpace - Quantum RNN Platform
# """

# from .preprocessing import DataPreprocessor
# from .evaluator import Evaluator
# from .trainer import Trainer
# from .report_generator import PDFReport, generate_report

# from .feature_engineering.mi_selector import MISelector
# from .feature_engineering.pca_reducer import PCAReducer

# # CORRECTION: importer depuis models/ (pas directement)
# from .models.rnn_model import RNNClassifier, create_rnn_model
# from .models.qrnn.pennylane.clean.model import QRNNClassifier, create_qrnn_model

# __all__ = [
#     'DataPreprocessor',
#     'Evaluator',
#     'Trainer',
#     'PDFReport',
#     'generate_report',
#     'MISelector',
#     'PCAReducer',
#     'RNNClassifier',
#     'create_rnn_model',
#     'QRNNClassifier',
#     'create_qrnn_model'
# ]

#WITH NOISE IMPLEMENTATION, IMPORTS POINT TO __init__.py PRINCIPAL DE CHAQUE BACKEND (CLEAN + NOISY)
# """
# ML Pipeline for NeuroSpace - Quantum RNN Platform
# """

# from .preprocessing import DataPreprocessor
# from .evaluator import Evaluator
# from .trainer import Trainer
# from .report_generator import PDFReport, generate_report

# from .feature_engineering.mi_selector import MISelector
# from .feature_engineering.pca_reducer import PCAReducer

# # RNN
# from .models.rnn_model import RNNClassifier, create_rnn_model

# # 🔥 QRNN - Import unifié (sélectionne clean ou noisy automatiquement)
# from .models.qrnn.pennylane import create_qrnn_model as create_pennylane_qrnn
# from .models.qrnn.pennylane import train_qrnn as train_pennylane_qrnn
# from .models.qrnn.qiskit import create_qiskit_qrnn_model as create_qiskit_qrnn
# from .models.qrnn.qiskit import train_qiskit_qrnn


# def get_qrnn_model(backend='pennylane', n_qubits=4, num_classes=2, n_layers=3,
#                    noise_level=0.0, mitigation_runs=1):
#     """
#     Factory unifiée pour créer un modèle QRNN (clean ou noisy selon noise_level)
#     """
#     if backend == 'pennylane':
#         return create_pennylane_qrnn(n_qubits, num_classes, n_layers, noise_level, mitigation_runs)
#     elif backend == 'qiskit':
#         return create_qiskit_qrnn(n_qubits, num_classes, n_layers, noise_level, mitigation_runs)
#     else:
#         raise ValueError(f"Backend inconnu: {backend}")


# def get_qrnn_trainer(backend='pennylane'):
#     """
#     Factory unifiée pour obtenir l'entraîneur QRNN
#     """
#     if backend == 'pennylane':
#         return train_pennylane_qrnn
#     elif backend == 'qiskit':
#         return train_qiskit_qrnn
#     else:
#         raise ValueError(f"Backend inconnu: {backend}")


# __all__ = [
#     'DataPreprocessor',
#     'Evaluator',
#     'Trainer',
#     'PDFReport',
#     'generate_report',
#     'MISelector',
#     'PCAReducer',
#     'RNNClassifier',
#     'create_rnn_model',
#     'get_qrnn_model',
#     'get_qrnn_trainer'
# ]


#FLEXIBLE essaie hope this works version 1.0__________________________________________________________________________________#

# """
# ML Pipeline for NeuroSpace - Quantum RNN Platform
# Import léger uniquement - pas de qiskit/pennylane au démarrage
# Les imports lourds se font en lazy (uniquement dans Colab worker)
# """

# # ✅ Seul import au démarrage - pas de dépendances lourdes
# from .adaptive_config import AdaptiveConfig


# def _validate_and_extract_params(dataset_info, adaptive_params, kwargs):
#     """
#     Validation et extraction des paramètres avec priorité kwargs > adaptatif > défaut
    
#     Returns:
#         dict avec tous les paramètres validés
#     """
#     # Validation noise_level
#     noise_level = kwargs.get('noise_level', 0.0)
#     if not 0.0 <= noise_level <= 1.0:
#         raise ValueError(f"noise_level doit être entre 0.0 et 1.0, reçu: {noise_level}")
    
#     # Validation mitigation_runs
#     mitigation_runs = kwargs.get('mitigation_runs', 1)
#     if mitigation_runs <= 0:
#         raise ValueError(f"mitigation_runs doit être > 0, reçu: {mitigation_runs}")
    
#     # Paramètres avec priorité: kwargs > adaptatif > défaut
#     params = {
#         'n_qubits': kwargs.get('n_qubits', adaptive_params['n_qubits']),
#         'n_layers': kwargs.get('n_layers', adaptive_params['n_layers']),
#         'num_classes': kwargs.get('num_classes', dataset_info.get('classes', 2)),
#         'learning_rate': kwargs.get('learning_rate', adaptive_params['learning_rate']),
#         'epochs': kwargs.get('epochs', adaptive_params.get('epochs', None)),
#         'noise_level': noise_level,
#         'mitigation_runs': mitigation_runs,
#     }
    
#     # Validation n_qubits
#     if params['n_qubits'] < 2:
#         raise ValueError(f"n_qubits doit être >= 2, reçu: {params['n_qubits']}")
    
#     # Validation num_classes
#     if params['num_classes'] < 2:
#         raise ValueError(f"num_classes doit être >= 2, reçu: {params['num_classes']}")
    
#     return params


# def get_qrnn_model(backend='pennylane', dataset_info=None, **kwargs):
#     """
#     Factory unifiée pour créer un modèle QRNN - Fully Adaptive
    
#     Args:
#         backend: 'pennylane' ou 'qiskit'
#         dataset_info: dict avec 'samples', 'features', 'classes'
#                       TOUS les paramètres seront auto-calculés si dataset_info est fourni
#         **kwargs: paramètres manuels optionnels (override)
#             - n_qubits: nombre de qubits (min 2)
#             - num_classes: nombre de classes (min 2)
#             - n_layers: nombre de couches quantiques
#             - learning_rate: taux d'apprentissage
#             - noise_level: 0.0-1.0 (0=clean, >0=noisy)
#             - mitigation_runs: nombre de runs pour mitigation (>0)
    
#     Returns:
#         Modèle QRNN configuré
    
#     Example:
#         # Tout automatique
#         model = get_qrnn_model(backend='pennylane', 
#                                dataset_info={'samples': 1000, 'features': 16, 'classes': 2})
        
#         # Avec override partiel
#         model = get_qrnn_model(backend='qiskit', 
#                                dataset_info={'samples': 500, 'features': 8, 'classes': 3},
#                                n_qubits=6, noise_level=0.1)
#     """
#     if dataset_info is None:
#         raise ValueError(
#             "dataset_info est obligatoire pour la configuration adaptative.\n"
#             "Exemple: {'samples': 1000, 'features': 16, 'classes': 2}"
#         )
    
#     # Validation dataset_info
#     required_keys = ['samples', 'features', 'classes']
#     missing_keys = [k for k in required_keys if k not in dataset_info]
#     if missing_keys:
#         raise ValueError(
#             f"dataset_info incomplet. Clés manquantes: {missing_keys}\n"
#             f"Clés requises: {required_keys}"
#         )
    
#     # 🧠 CERVEAU ADAPTATIF : Calcule tous les hyperparamètres optimaux
#     adaptive_params = AdaptiveConfig.compute_all_params(dataset_info)
    
#     # Extraire et valider les paramètres (avec priorité kwargs > adaptatif)
#     params = _validate_and_extract_params(dataset_info, adaptive_params, kwargs)
    
#     print(f"🎯 Configuration adaptative: qubits={params['n_qubits']}, "
#           f"classes={params['num_classes']}, layers={params['n_layers']}, "
#           f"lr={params['learning_rate']:.5f}, backend={backend}, "
#           f"noise={params['noise_level']}, mitigation={params['mitigation_runs']}")
    
#     # Création du modèle selon le backend
#     if backend == 'pennylane':
#         if params['noise_level'] > 0.0:
#             from .models.qrnn.pennylane.noisy.model import create_qrnn_model
            
#             return create_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 noise_level=params['noise_level'],
#                 mitigation_runs=params['mitigation_runs'],
#                 dataset_info=dataset_info
#             )
#         else:
#             from .models.qrnn.pennylane.clean.model import create_qrnn_model
            
#             return create_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 dataset_info=dataset_info
#             )

#     elif backend == 'qiskit':
#         if params['noise_level'] > 0.0:
#             from .models.qrnn.qiskit.noisy.model import create_qiskit_qrnn_model
            
#             return create_qiskit_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 noise_level=params['noise_level'],
#                 mitigation_runs=params['mitigation_runs'],
#                 dataset_info=dataset_info
#             )
#         else:
#             from .models.qrnn.qiskit.clean.model import create_qiskit_qrnn_model
            
#             return create_qiskit_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 dataset_info=dataset_info
#             )
#     else:
#         raise ValueError(f"Backend inconnu: '{backend}'. Utilisez 'pennylane' ou 'qiskit'")


# def get_qrnn_trainer(backend='pennylane', noise_level=0.0):
#     """
#     Factory unifiée pour obtenir le bon trainer
    
#     Args:
#         backend: 'pennylane' ou 'qiskit'
#         noise_level: 0.0 = clean trainer, >0 = noisy trainer
    
#     Returns:
#         Fonction d'entraînement appropriée
#     """
#     if not 0.0 <= noise_level <= 1.0:
#         raise ValueError(f"noise_level doit être entre 0.0 et 1.0, reçu: {noise_level}")
    
#     if backend == 'pennylane':
#         if noise_level > 0.0:
#             from .models.qrnn.pennylane.noisy.trainer import train_qrnn
#         else:
#             from .models.qrnn.pennylane.clean.trainer import train_qrnn
#         return train_qrnn

#     elif backend == 'qiskit':
#         if noise_level > 0.0:
#             from .models.qrnn.qiskit.noisy.trainer import train_qiskit_qrnn
#         else:
#             from .models.qrnn.qiskit.clean.trainer import train_qiskit_qrnn
#         return train_qiskit_qrnn

#     else:
#         raise ValueError(f"Backend inconnu: '{backend}'. Utilisez 'pennylane' ou 'qiskit'")


# def get_rnn_model(dataset_info=None, **kwargs):
#     """
#     Factory pour RNN - Fully Adaptive
    
#     Args:
#         dataset_info: dict avec 'samples', 'features', 'classes'
#         **kwargs: override manuels (input_size, hidden_size, etc.)
    
#     Returns:
#         Modèle RNN classique configuré
#     """
#     from .models.rnn_model import create_rnn_model
    
#     if dataset_info is None:
#         raise ValueError(
#             "dataset_info est obligatoire pour la configuration adaptative.\n"
#             "Exemple: {'samples': 1000, 'features': 16, 'classes': 2}"
#         )
    
#     # 🧠 Calcul adaptatif complet
#     adaptive_params = AdaptiveConfig.compute_all_params(dataset_info)
    
#     # Utiliser les paramètres adaptatifs avec possibilité d'override
#     params = {
#         'input_size': kwargs.get('input_size', dataset_info.get('features', 64)),
#         'num_classes': kwargs.get('num_classes', dataset_info.get('classes', 2)),
#         'hidden_size': kwargs.get('hidden_size', adaptive_params.get('hidden_size', None)),
#         'num_layers': kwargs.get('num_layers', adaptive_params.get('rnn_layers', None)),
#         'dropout': kwargs.get('dropout', adaptive_params.get('dropout', None)),
#         'learning_rate': kwargs.get('learning_rate', adaptive_params.get('learning_rate', None)),
#     }
    
#     print(f"🎯 RNN Configuration: input={params['input_size']}, "
#           f"classes={params['num_classes']}, hidden={params['hidden_size']}, "
#           f"layers={params['num_layers']}, lr={params['learning_rate']}")
    
#     return create_rnn_model(
#         input_size=params['input_size'],
#         num_classes=params['num_classes'],
#         hidden_size=params['hidden_size'],
#         num_layers=params['num_layers'],
#         dropout=params['dropout'],
#         learning_rate=params['learning_rate'],
#         dataset_info=dataset_info
#     )


# def compute_adaptive_params(dataset_info):
#     """
#     Calcule tous les hyperparamètres adaptatifs pour un dataset
    
#     Args:
#         dataset_info: dict avec 'samples', 'features', 'classes'
    
#     Returns:
#         dict complet avec params RNN et QRNN
#     """
#     if dataset_info is None:
#         raise ValueError("dataset_info est obligatoire")
    
#     return AdaptiveConfig.compute_all_params(dataset_info)


# __all__ = [
#     'AdaptiveConfig',
#     'get_qrnn_model',
#     'get_qrnn_trainer',
#     'get_rnn_model',
#     'compute_adaptive_params',
# ]

#VERSION 2.0 OF GROK HOPE THIS WORKS BETTER THAN 1.0__________________________________________________________________________________#
# """
# ML Pipeline for NeuroSpace - Quantum RNN Platform
# Import léger uniquement - pas de qiskit/pennylane au démarrage
# Les imports lourds se font en lazy (uniquement dans Colab worker)
# """

# # ✅ Seul import au démarrage - pas de dépendances lourdes
# from .adaptive_config import AdaptiveConfig


# def _validate_and_extract_params(dataset_info, adaptive_params, kwargs):
#     """
#     Validation et extraction sécurisée des paramètres
#     PRIORITÉ : kwargs (manuel) > adaptive_params['qrnn'] > défauts
#     """
#     # Debug
#     print(f"   🔍 DEBUG _validate_and_extract_params:")
#     print(f"      adaptive_params keys: {list(adaptive_params.keys())}")
#     print(f"      kwargs keys: {list(kwargs.keys())}")
    
#     # Extraire la partie QRNN si on a reçu tout le dict adaptatif
#     if isinstance(adaptive_params, dict) and 'qrnn' in adaptive_params:
#         adaptive_params = adaptive_params['qrnn']
#         print(f"      → Extraction de adaptive_params['qrnn'] effectuée")
#         print(f"      → adaptive_params (qrnn) keys: {list(adaptive_params.keys())}")
    
#     # ====================== EXTRACTION SÉCURISÉE ======================
#     # ✅ Éviter le piège de dict.get() qui évalue l'argument par défaut
#     n_qubits = kwargs.get('n_qubits')
#     if n_qubits is None:
#         n_qubits = adaptive_params.get('n_qubits')
#     if n_qubits is None:
#         n_qubits = dataset_info.get('recommended_qubits', 4)

#     n_layers = kwargs.get('n_layers')
#     if n_layers is None:
#         n_layers = adaptive_params.get('n_layers', 3)

#     learning_rate = kwargs.get('learning_rate')
#     if learning_rate is None:
#         learning_rate = adaptive_params.get('learning_rate', 0.01)

#     num_classes = kwargs.get('num_classes')
#     if num_classes is None:
#         num_classes = dataset_info.get('classes', 2)

#     noise_level = kwargs.get('noise_level', 0.0)
#     mitigation_runs = kwargs.get('mitigation_runs', 1)

#     params = {
#         'n_qubits': int(n_qubits),
#         'n_layers': int(n_layers),
#         'num_classes': int(num_classes),
#         'learning_rate': float(learning_rate),
#         'noise_level': float(noise_level),
#         'mitigation_runs': int(mitigation_runs),
#     }

#     print(f"   ✅ Params finaux extraits: qubits={params['n_qubits']}, "
#           f"layers={params['n_layers']}, lr={params['learning_rate']:.5f}")

#     # Validations
#     if params['n_qubits'] < 2:
#         raise ValueError(f"n_qubits doit être >= 2, reçu: {params['n_qubits']}")
#     if params['num_classes'] < 2:
#         raise ValueError(f"num_classes doit être >= 2, reçu: {params['num_classes']}")

#     return params


# def get_qrnn_model(backend='pennylane', dataset_info=None, **kwargs):
#     """
#     Factory unifiée pour créer un modèle QRNN - Fully Adaptive
    
#     Args:
#         backend: 'pennylane' ou 'qiskit'
#         dataset_info: dict avec 'samples', 'features', 'classes', 'recommended_qubits'
#         **kwargs: paramètres manuels optionnels (override)
    
#     Returns:
#         Modèle QRNN configuré
#     """
#     if dataset_info is None:
#         raise ValueError(
#             "dataset_info est obligatoire pour la configuration adaptative.\n"
#             "Exemple: {'samples': 1000, 'features': 16, 'classes': 2, 'recommended_qubits': 4}"
#         )
    
#     # Validation dataset_info
#     required_keys = ['samples', 'features', 'classes']
#     missing_keys = [k for k in required_keys if k not in dataset_info]
#     if missing_keys:
#         raise ValueError(
#             f"dataset_info incomplet. Clés manquantes: {missing_keys}\n"
#             f"Clés requises: {required_keys}"
#         )
    
#     # 🧠 Calcul adaptatif complet
#     adaptive_all = AdaptiveConfig.compute_all_params(dataset_info)
    
#     print(f"   🔍 adaptive_all keys: {list(adaptive_all.keys())}")
    
#     # Extraction des paramètres
#     params = _validate_and_extract_params(dataset_info, adaptive_all, kwargs)

#     print(f"🎯 Configuration QRNN finale: qubits={params['n_qubits']}, "
#           f"classes={params['num_classes']}, layers={params['n_layers']}, "
#           f"lr={params['learning_rate']:.5f}, backend={backend}, "
#           f"noise={params['noise_level']}, mitigation={params['mitigation_runs']}")

#     # Création du modèle selon le backend
#     if backend == 'pennylane':
#         if params['noise_level'] > 0.0:
#             from .models.qrnn.pennylane.noisy.model import create_qrnn_model
#             return create_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 noise_level=params['noise_level'],
#                 mitigation_runs=params['mitigation_runs'],
#                 dataset_info=dataset_info
#             )
#         else:
#             from .models.qrnn.pennylane.clean.model import create_qrnn_model
#             return create_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 dataset_info=dataset_info
#             )

#     elif backend == 'qiskit':
#         if params['noise_level'] > 0.0:
#             from .models.qrnn.qiskit.noisy.model import create_qiskit_qrnn_model
#             return create_qiskit_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 noise_level=params['noise_level'],
#                 mitigation_runs=params['mitigation_runs'],
#                 dataset_info=dataset_info
#             )
#         else:
#             from .models.qrnn.qiskit.clean.model import create_qiskit_qrnn_model
#             return create_qiskit_qrnn_model(
#                 n_qubits=params['n_qubits'],
#                 num_classes=params['num_classes'],
#                 n_layers=params['n_layers'],
#                 learning_rate=params['learning_rate'],
#                 dataset_info=dataset_info
#             )
#     else:
#         raise ValueError(f"Backend inconnu: '{backend}'. Utilisez 'pennylane' ou 'qiskit'")


# def get_qrnn_trainer(backend='pennylane', noise_level=0.0):
#     """
#     Factory unifiée pour obtenir le bon trainer
    
#     Args:
#         backend: 'pennylane' ou 'qiskit'
#         noise_level: 0.0 = clean trainer, >0 = noisy trainer
#     """
#     if not 0.0 <= noise_level <= 1.0:
#         raise ValueError(f"noise_level doit être entre 0.0 et 1.0, reçu: {noise_level}")
    
#     if backend == 'pennylane':
#         if noise_level > 0.0:
#             from .models.qrnn.pennylane.noisy.trainer import train_qrnn
#         else:
#             from .models.qrnn.pennylane.clean.trainer import train_qrnn
#         return train_qrnn

#     elif backend == 'qiskit':
#         if noise_level > 0.0:
#             from .models.qrnn.qiskit.noisy.trainer import train_qiskit_qrnn
#         else:
#             from .models.qrnn.qiskit.clean.trainer import train_qiskit_qrnn
#         return train_qiskit_qrnn

#     else:
#         raise ValueError(f"Backend inconnu: '{backend}'. Utilisez 'pennylane' ou 'qiskit'")


# def get_rnn_model(dataset_info=None, **kwargs):
#     """
#     Factory pour RNN/MLP - Fully Adaptive
    
#     Args:
#         dataset_info: dict avec 'samples', 'features', 'classes'
#         **kwargs: override manuels (input_size, hidden_size, num_layers, dropout, learning_rate, num_classes)
    
#     Returns:
#         Modèle MLP configuré
#     """
#     from .models.rnn_model import create_rnn_model
    
#     if dataset_info is None:
#         raise ValueError(
#             "dataset_info est obligatoire pour la configuration adaptative.\n"
#             "Exemple: {'samples': 1000, 'features': 16, 'classes': 2}"
#         )
    
#     # ✅ Extraire les paramètres de kwargs, PUIS les supprimer pour éviter le double passage
#     input_size = kwargs.pop('input_size', dataset_info.get('features', 64))
#     num_classes = kwargs.pop('num_classes', dataset_info.get('classes', 2))
#     hidden_size = kwargs.pop('hidden_size', None)
#     num_layers = kwargs.pop('num_layers', None)
#     dropout = kwargs.pop('dropout', None)
#     learning_rate = kwargs.pop('learning_rate', None)
    
#     print(f"🎯 RNN Configuration: input={input_size}, classes={num_classes}, "
#           f"hidden={hidden_size}, layers={num_layers}, dropout={dropout}, lr={learning_rate}")
    
#     # ✅ Maintenant kwargs ne contient PLUS input_size/num_classes → pas de doublon
#     return create_rnn_model(
#         input_size=input_size,
#         num_classes=num_classes,
#         hidden_size=hidden_size,        # None → auto via AdaptiveConfig
#         num_layers=num_layers,          # None → auto via AdaptiveConfig
#         dropout=dropout,                # None → auto via AdaptiveConfig
#         learning_rate=learning_rate,    # None → auto via AdaptiveConfig
#         dataset_info=dataset_info       # Pour l'adaptation automatique
#     )


# def compute_adaptive_params(dataset_info):
#     """
#     Calcule tous les hyperparamètres adaptatifs pour un dataset
    
#     Args:
#         dataset_info: dict avec 'samples', 'features', 'classes'
    
#     Returns:
#         dict complet avec params RNN et QRNN
#     """
#     if dataset_info is None:
#         raise ValueError("dataset_info est obligatoire")
    
#     return AdaptiveConfig.compute_all_params(dataset_info)


# __all__ = [
#     'AdaptiveConfig',
#     'get_qrnn_model',
#     'get_qrnn_trainer',
#     'get_rnn_model',
#     'compute_adaptive_params',
# ]


#NEW CODE WITH GPT5 FOR FLEXIBLE VERSION TEST_____________________________________________________________#

"""
ML Pipeline for NeuroSpace - Quantum RNN Platform

Import léger uniquement :
- Pas d'import Qiskit/PennyLane au démarrage.
- Les imports lourds sont faits en lazy loading uniquement quand on crée un modèle.
- Compatible avec Colab.
"""

from .adaptive_config import AdaptiveConfig


def _normalize_backend(backend: str) -> str:
    backend = (backend or "pennylane").lower().strip()

    if backend not in ["pennylane", "qiskit"]:
        raise ValueError(
            f"Backend inconnu: '{backend}'. Utilisez 'pennylane' ou 'qiskit'."
        )

    return backend


def _should_use_noisy(noisy=None, noise_level=0.0, mitigation_runs=1):
    """
    Détermine si on doit utiliser la version noisy.

    Priorité :
    - si noisy est explicitement donné, on le respecte
    - sinon noise_level > 0 ou mitigation_runs > 1 active noisy
    """
    if noisy is not None:
        return bool(noisy)

    try:
        noise_level = float(noise_level)
    except Exception:
        noise_level = 0.0

    try:
        mitigation_runs = int(mitigation_runs)
    except Exception:
        mitigation_runs = 1

    return noise_level > 0.0 or mitigation_runs > 1


def _validate_and_extract_qrnn_params(dataset_info, kwargs):
    """
    Validation et extraction sécurisée des paramètres QRNN.

    Priorité :
    1. kwargs envoyés par le worker
    2. dataset_info
    3. AdaptiveConfig pour n_layers / learning_rate / batch
    """

    if dataset_info is None:
        raise ValueError(
            "dataset_info est obligatoire pour créer un QRNN. "
            "Exemple: {'samples': 1000, 'features': 8, 'classes': 2, 'recommended_qubits': 5}"
        )

    required_keys = ["samples", "features", "classes"]
    missing_keys = [key for key in required_keys if key not in dataset_info]

    if missing_keys:
        raise ValueError(
            f"dataset_info incomplet. Clés manquantes: {missing_keys}. "
            f"Clés requises: {required_keys}"
        )

    # n_qubits doit venir explicitement du worker ou du MISelector via dataset_info
    n_qubits = kwargs.get("n_qubits")

    if n_qubits is None:
        n_qubits = dataset_info.get("recommended_qubits")

    if n_qubits is None:
        raise ValueError(
            "n_qubits est obligatoire. "
            "Passe n_qubits depuis MISelector ou ajoute dataset_info['recommended_qubits']."
        )

    # num_classes
    num_classes = kwargs.get("num_classes")

    if num_classes is None:
        num_classes = dataset_info.get("classes")

    if num_classes is None:
        raise ValueError(
            "num_classes est obligatoire ou dataset_info['classes'] doit exister."
        )

    # Adaptive params structurels
    adaptive_all = AdaptiveConfig.compute_all_params(
        {
            "samples": dataset_info.get("samples", 1000),
            "features": dataset_info.get("features", 10),
            "classes": int(num_classes),
            "recommended_qubits": int(n_qubits),
        }
    )

    qrnn_adaptive = adaptive_all["qrnn"]

    n_layers = kwargs.get("n_layers")
    if n_layers is None:
        n_layers = qrnn_adaptive.get("n_layers", 3)

    learning_rate = kwargs.get("learning_rate")
    if learning_rate is None:
        learning_rate = qrnn_adaptive.get("learning_rate", 0.01)

    noise_level = kwargs.get("noise_level", 0.0)
    mitigation_runs = kwargs.get("mitigation_runs", 1)

    params = {
        "n_qubits": int(n_qubits),
        "num_classes": int(num_classes),
        "n_layers": int(n_layers),
        "learning_rate": float(learning_rate),
        "noise_level": float(noise_level),
        "mitigation_runs": int(mitigation_runs),
    }

    if params["n_qubits"] < 2:
        raise ValueError(f"n_qubits doit être >= 2, reçu: {params['n_qubits']}")

    if params["num_classes"] < 2:
        raise ValueError(f"num_classes doit être >= 2, reçu: {params['num_classes']}")

    print(
        "🎯 QRNN params finaux: "
        f"qubits={params['n_qubits']}, "
        f"classes={params['num_classes']}, "
        f"layers={params['n_layers']}, "
        f"lr={params['learning_rate']:.5f}, "
        f"noise={params['noise_level']}, "
        f"mitigation={params['mitigation_runs']}"
    )

    return params


def get_qrnn_model(
    backend="pennylane",
    dataset_info=None,
    noisy=None,
    **kwargs,
):
    """
    Factory unifiée QRNN.

    Compatible avec :
    get_qrnn_model(backend="pennylane", noisy=True, ...)
    get_qrnn_model(backend="pennylane", noise_level=0.01, ...)
    get_qrnn_model(backend="qiskit", noisy=False, ...)
    """

    backend = _normalize_backend(backend)

    params = _validate_and_extract_qrnn_params(dataset_info, kwargs)

    use_noisy = _should_use_noisy(
        noisy=noisy,
        noise_level=params["noise_level"],
        mitigation_runs=params["mitigation_runs"],
    )

    print(
        f"⚛️ Création QRNN: backend={backend}, "
        f"mode={'noisy' if use_noisy else 'clean'}"
    )

    if backend == "pennylane":
        if use_noisy:
            from .models.qrnn.pennylane.noisy.model import create_qrnn_model

            return create_qrnn_model(
                dataset_info=dataset_info,
                n_qubits=params["n_qubits"],
                num_classes=params["num_classes"],
                n_layers=params["n_layers"],
                learning_rate=params["learning_rate"],
                noise_level=params["noise_level"],
                mitigation_runs=params["mitigation_runs"],
            )

        from .models.qrnn.pennylane.clean.model import create_qrnn_model

        return create_qrnn_model(
            dataset_info=dataset_info,
            n_qubits=params["n_qubits"],
            num_classes=params["num_classes"],
            n_layers=params["n_layers"],
            learning_rate=params["learning_rate"],
        )

    if backend == "qiskit":
        if use_noisy:
            from .models.qrnn.qiskit.noisy.model import create_qiskit_qrnn_model

            return create_qiskit_qrnn_model(
                dataset_info=dataset_info,
                n_qubits=params["n_qubits"],
                num_classes=params["num_classes"],
                n_layers=params["n_layers"],
                learning_rate=params["learning_rate"],
                noise_level=params["noise_level"],
                mitigation_runs=params["mitigation_runs"],
            )

        from .models.qrnn.qiskit.clean.model import create_qiskit_qrnn_model

        return create_qiskit_qrnn_model(
            dataset_info=dataset_info,
            n_qubits=params["n_qubits"],
            num_classes=params["num_classes"],
            n_layers=params["n_layers"],
            learning_rate=params["learning_rate"],
        )


def get_qrnn_trainer(
    backend="pennylane",
    noisy=None,
    noise_level=0.0,
    mitigation_runs=1,
):
    """
    Factory unifiée pour obtenir le bon trainer QRNN.

    Compatible avec :
    get_qrnn_trainer(backend="pennylane", noisy=True)
    get_qrnn_trainer(backend="pennylane", noise_level=0.01)
    """

    backend = _normalize_backend(backend)

    use_noisy = _should_use_noisy(
        noisy=noisy,
        noise_level=noise_level,
        mitigation_runs=mitigation_runs,
    )

    print(
        f"🎯 QRNN trainer: backend={backend}, "
        f"mode={'noisy' if use_noisy else 'clean'}"
    )

    if backend == "pennylane":
        if use_noisy:
            from .models.qrnn.pennylane.noisy.trainer import train_qrnn
        else:
            from .models.qrnn.pennylane.clean.trainer import train_qrnn

        return train_qrnn

    if backend == "qiskit":
        if use_noisy:
            from .models.qrnn.qiskit.noisy.trainer import train_qiskit_qrnn
        else:
            from .models.qrnn.qiskit.clean.trainer import train_qiskit_qrnn

        return train_qiskit_qrnn


def get_rnn_model(dataset_info=None, **kwargs):
    """
    Factory MLP/RNN classique.

    Le nom get_rnn_model est gardé pour compatibilité,
    mais le modèle classique est ton MLP.
    """

    from .models.rnn_model import create_rnn_model

    if dataset_info is None:
        raise ValueError(
            "dataset_info est obligatoire pour la configuration adaptative. "
            "Exemple: {'samples': 1000, 'features': 8, 'classes': 2}"
        )

    input_size = kwargs.pop("input_size", dataset_info.get("features"))
    num_classes = kwargs.pop("num_classes", dataset_info.get("classes", 2))

    if input_size is None:
        raise ValueError("input_size est obligatoire pour le modèle MLP/RNN.")

    hidden_size = kwargs.pop("hidden_size", None)
    num_layers = kwargs.pop("num_layers", None)
    dropout = kwargs.pop("dropout", None)
    learning_rate = kwargs.pop("learning_rate", None)

    print(
        "🎯 MLP/RNN params: "
        f"input={input_size}, classes={num_classes}, "
        f"hidden={hidden_size}, layers={num_layers}, "
        f"dropout={dropout}, lr={learning_rate}"
    )

    return create_rnn_model(
        input_size=input_size,
        num_classes=num_classes,
        hidden_size=hidden_size,
        num_layers=num_layers,
        dropout=dropout,
        learning_rate=learning_rate,
        dataset_info=dataset_info,
    )


def compute_adaptive_params(dataset_info):
    if dataset_info is None:
        raise ValueError("dataset_info est obligatoire")

    return AdaptiveConfig.compute_all_params(dataset_info)


__all__ = [
    "AdaptiveConfig",
    "get_qrnn_model",
    "get_qrnn_trainer",
    "get_rnn_model",
    "compute_adaptive_params",
]