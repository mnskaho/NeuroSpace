# # backend/models.py
# from pydantic import BaseModel
# from typing import Optional, List, Dict, Any
# from datetime import datetime

# class DatasetInfo(BaseModel):
#     """Informations sur le dataset"""
#     samples: int
#     features: int
#     classes: int
#     target_column: str
#     recommended_qubits: int
#     pca_dimension: int

# class TrainingConfig(BaseModel):
#     """Configuration d'entraînement"""
#     model_types: List[str]
#     rnn_epochs: int = 30
#     qrnn_epochs: int = 20
#     batch_size: int = 32

# class TrainingRequest(BaseModel):
#     """Requête d'entraînement - SANS file_id car il est dans l'URL"""
#     model_types: List[str] = ["rnn", "qrnn"]
#     rnn_epochs: int = 50
#     qrnn_epochs: int = 30
#     batch_size: int = 32
#     comparison_mode: str = "pca"  # "pca" ou "mi"
#     qrnn_backend: str = "pennylane"  # "pennylane" ou "qiskit"
# class JobStatus:
#     """Constantes pour les statuts"""
#     UPLOADED = "uploaded"
#     QUEUED = "queued"
#     PROCESSING = "processing"
#     COMPLETED = "completed"
#     FAILED = "failed"

# class Job(BaseModel):
#     """Job d'entraînement"""
#     id: str
#     filename: str
#     file_path: str
#     status: str = JobStatus.UPLOADED
#     dataset_info: Optional[DatasetInfo] = None
#     config: Optional[Dict[str, Any]] = None
#     results: Optional[Dict[str, Any]] = None
#     plots: Optional[Dict[str, Any]] = None
#     message: Optional[str] = None
#     error: Optional[str] = None
#     progress: int = 0
#     created_at: datetime = datetime.now()
#     started_at: Optional[datetime] = None
#     completed_at: Optional[datetime] = None
#     results_path: Optional[str] = None
    
#     class Config:
#         arbitrary_types_allowed = True

# class JobResponse(BaseModel):
#     """Réponse pour un job"""
#     job_id: str
#     status: str
#     message: Optional[str] = None
#     progress: Optional[int] = 0


#OLD CODE BEFORE BRUIT 
# backend/models.py
# from pydantic import BaseModel
# from typing import Optional, List, Dict, Any
# from datetime import datetime

# class DatasetInfo(BaseModel):
#     samples: int
#     features: int
#     classes: int
#     target_column: str
#     recommended_qubits: int
#     pca_dimension: int

# class TrainingConfig(BaseModel):
#     model_types: List[str]
#     rnn_epochs: int = 30
#     qrnn_epochs: int = 20
#     batch_size: int = 32

# class TrainingRequest(BaseModel):
#     """Requête d'entraînement - CORRIGÉE"""
#     model_types: List[str] = ["rnn", "qrnn"]
#     rnn_epochs: int = 30
#     qrnn_epochs: int = 20
#     batch_size: int = 32
#     comparison_mode: str = "pca"  # "pca" ou "mi"
#     qrnn_backend: str = "pennylane"  # "pennylane" ou "qiskit"

# class JobStatus:
#     UPLOADED = "uploaded"
#     QUEUED = "queued"
#     PROCESSING = "processing"
#     COMPLETED = "completed"
#     FAILED = "failed"

# class Job(BaseModel):
#     id: str
#     filename: str
#     file_path: str
#     status: str = JobStatus.UPLOADED
#     dataset_info: Optional[DatasetInfo] = None
#     config: Optional[Dict[str, Any]] = None
#     results: Optional[Dict[str, Any]] = None
#     plots: Optional[Dict[str, Any]] = None
#     message: Optional[str] = None
#     error: Optional[str] = None
#     progress: int = 0
#     created_at: datetime = datetime.now()
#     started_at: Optional[datetime] = None
#     completed_at: Optional[datetime] = None
#     results_path: Optional[str] = None
    
#     class Config:
#         arbitrary_types_allowed = True

# class JobResponse(BaseModel):
#     job_id: str
#     status: str
#     message: Optional[str] = None
#     progress: Optional[int] = 0

# backend/models.py
# from pydantic import BaseModel
# from typing import Optional, List, Dict, Any
# from datetime import datetime

# class DatasetInfo(BaseModel):
#     samples: int
#     features: int
#     classes: int
#     target_column: str
#     recommended_qubits: int
#     pca_dimension: int

# class TrainingConfig(BaseModel):
#     model_types: List[str]
#     rnn_epochs: int = 30
#     qrnn_epochs: int = 20
#     batch_size: int = 32

# class TrainingRequest(BaseModel):
#     """Requête d'entraînement - AVEC SUPPORT DU BRUIT"""
#     model_types: List[str] = ["rnn", "qrnn"]
#     rnn_epochs: int = 30
#     qrnn_epochs: int = 20
#     batch_size: int = 32
#     comparison_mode: str = "pca"
#     qrnn_backend: str = "pennylane"
#     # 🔥 NOUVEAUX CHAMPS POUR LE BRUIT
#     noise_enabled: bool = False
#     noise_level: float = 0.0
#     mitigation_runs: int = 1
#     mitigation_enabled: bool = False

# class JobStatus:
#     UPLOADED = "uploaded"
#     QUEUED = "queued"
#     PROCESSING = "processing"
#     COMPLETED = "completed"
#     FAILED = "failed"

# class Job(BaseModel):
#     id: str
#     filename: str
#     file_path: str
#     status: str = JobStatus.UPLOADED
#     dataset_info: Optional[DatasetInfo] = None
#     config: Optional[Dict[str, Any]] = None
#     results: Optional[Dict[str, Any]] = None
#     plots: Optional[Dict[str, Any]] = None
#     message: Optional[str] = None
#     error: Optional[str] = None
#     progress: int = 0
#     created_at: datetime = datetime.now()
#     started_at: Optional[datetime] = None
#     completed_at: Optional[datetime] = None
#     results_path: Optional[str] = None
    
#     class Config:
#         arbitrary_types_allowed = True

# class JobResponse(BaseModel):
#     job_id: str
#     status: str
#     message: Optional[str] = None
#     progress: Optional[int] = 0

#NEW CODE FOR FLEXIBILITY IN QRNN BACKENDS _____________________________________________________________________

# backend/models.py
# from pydantic import BaseModel
# from typing import Optional, List, Dict, Any
# from datetime import datetime

# class DatasetInfo(BaseModel):
#     samples: int
#     features: int
#     classes: int
#     target_column: str
#     recommended_qubits: int
#     pca_dimension: int
#     # 🔥 Paramètres adaptatifs RNN (calculés par AdaptiveConfig)
#     rnn_hidden_size: Optional[int] = None
#     rnn_num_layers: Optional[int] = None
#     rnn_dropout: Optional[float] = None
#     rnn_learning_rate: Optional[float] = None
#     recommended_epochs_rnn: Optional[int] = None
#     # 🔥 Paramètres adaptatifs QRNN (calculés par AdaptiveConfig)
#     qrnn_layers: Optional[int] = None
#     qrnn_learning_rate: Optional[float] = None
#     recommended_epochs_qrnn: Optional[int] = None
#     recommended_batch_size: Optional[int] = None

# class TrainingConfig(BaseModel):
#     model_types: List[str]
#     rnn_epochs: Optional[int] = None
#     qrnn_epochs: Optional[int] = None
#     batch_size: Optional[int] = None

# class TrainingRequest(BaseModel):
#     """
#     Requête d'entraînement.
#     Règle : None = auto-calculé par AdaptiveConfig
#            Valeur = override utilisateur explicite
#     """
#     model_types: List[str] = ["rnn", "qrnn"]
#     # 🔥 None = auto (plus de 20/30 en dur)
#     rnn_epochs: Optional[int] = None
#     qrnn_epochs: Optional[int] = None
#     batch_size: Optional[int] = None
    
#     comparison_mode: str = "pca"
#     qrnn_backend: str = "pennylane"
    
#     # Bruit quantique
#     noise_enabled: bool = False
#     noise_level: float = 0.0
#     mitigation_enabled: bool = False
#     mitigation_runs: int = 1
    
#     # 🔥 Paramètres adaptatifs (None = auto-calcul)
#     qrnn_layers: Optional[int] = None
#     qrnn_learning_rate: Optional[float] = None
#     rnn_hidden_size: Optional[int] = None
#     rnn_num_layers: Optional[int] = None
#     rnn_dropout: Optional[float] = None
#     rnn_learning_rate: Optional[float] = None

# class JobStatus:
#     UPLOADED = "uploaded"
#     QUEUED = "queued"
#     PROCESSING = "processing"
#     COMPLETED = "completed"
#     FAILED = "failed"

# class Job(BaseModel):
#     id: str
#     filename: str
#     file_path: str
#     status: str = JobStatus.UPLOADED
#     dataset_info: Optional[DatasetInfo] = None
#     config: Optional[Dict[str, Any]] = None
#     results: Optional[Dict[str, Any]] = None
#     plots: Optional[Dict[str, Any]] = None
#     message: Optional[str] = None
#     error: Optional[str] = None
#     progress: int = 0
#     created_at: datetime = datetime.now()
#     started_at: Optional[datetime] = None
#     completed_at: Optional[datetime] = None
#     results_path: Optional[str] = None
    
#     class Config:
#         arbitrary_types_allowed = True

# class JobResponse(BaseModel):
#     job_id: str
#     status: str
#     message: Optional[str] = None
#     progress: Optional[int] = 0

#NEW CODE FOR FLEXIBILITY IN QRNN BACKENDS TO GET RID OF UPLOAD ISSUE  _____________________________________________________________________#

# backend/models.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class DatasetInfo(BaseModel):
    """
    Informations BRUTES du dataset (sans calcul adaptatif)
    L'intelligence adaptative est 100% dans ml_pipeline
    """
    samples: int
    features: int
    classes: int
    target_column: str
    
    # ⚠️ Champs calculés par ml_pipeline - Peuvent être None
    # Utiliser Union[int, None] ou Optional[int] avec default None
    recommended_qubits: Optional[int] = None
    pca_dimension: Optional[int] = None
    
    # Paramètres adaptatifs RNN
    rnn_hidden_size: Optional[int] = None
    rnn_num_layers: Optional[int] = None
    rnn_dropout: Optional[float] = None
    rnn_learning_rate: Optional[float] = None
    recommended_epochs_rnn: Optional[int] = None
    
    # Paramètres adaptatifs QRNN
    qrnn_layers: Optional[int] = None
    qrnn_learning_rate: Optional[float] = None
    recommended_epochs_qrnn: Optional[int] = None
    
    # ✅ Batch sizes SÉPARÉS (RNN ≠ QRNN)
    recommended_batch_size_rnn: Optional[int] = None
    recommended_batch_size_qrnn: Optional[int] = None


class UserPreferences(BaseModel):
    """
    Préférences utilisateur (choix du modèle, backend, etc.)
    """
    model_types: List[str] = ["rnn", "qrnn"]
    comparison_mode: str = "pca"
    qrnn_backend: str = "pennylane"
    feature_selector: str = "mi"  # 'mi' ou 'pca'
    
    # Bruit quantique
    noise_enabled: bool = False
    noise_level: float = 0.0
    mitigation_enabled: bool = False
    mitigation_runs: int = 1


class ManualOverrides(BaseModel):
    """
    Overrides manuels de l'utilisateur (Expert mode)
    None = laisser ml_pipeline décider automatiquement
    """
    # RNN overrides
    rnn_epochs: Optional[int] = None
    rnn_batch_size: Optional[int] = None
    rnn_hidden_size: Optional[int] = None
    rnn_num_layers: Optional[int] = None
    rnn_dropout: Optional[float] = None
    rnn_learning_rate: Optional[float] = None
    
    # QRNN overrides
    qrnn_epochs: Optional[int] = None
    qrnn_batch_size: Optional[int] = None
    qrnn_layers: Optional[int] = None
    qrnn_learning_rate: Optional[float] = None


class TrainingRequest(BaseModel):
    """
    Requête d'entraînement envoyée par le frontend
    Règle : None = auto-calculé par AdaptiveConfig dans le worker
           Valeur = override utilisateur explicite
    """
    # Modèles à entraîner
    model_types: List[str] = ["rnn", "qrnn"]
    
    # Configuration générale
    comparison_mode: str = "pca"
    qrnn_backend: str = "pennylane"
    feature_selector: str = "mi"  # 'mi' ou 'pca'
    
    # Bruit quantique
    noise_enabled: bool = False
    noise_level: float = 0.0
    mitigation_enabled: bool = False
    mitigation_runs: int = 1
    
    # ✅ RNN overrides (None = auto)
    rnn_epochs: Optional[int] = None
    rnn_batch_size: Optional[int] = None
    rnn_hidden_size: Optional[int] = None
    rnn_num_layers: Optional[int] = None
    rnn_dropout: Optional[float] = None
    rnn_learning_rate: Optional[float] = None
    
    # ✅ QRNN overrides (None = auto)
    qrnn_epochs: Optional[int] = None
    qrnn_batch_size: Optional[int] = None
    qrnn_layers: Optional[int] = None
    qrnn_learning_rate: Optional[float] = None
    
    # ⚠️ Déprécié - gardé pour compatibilité
    batch_size: Optional[int] = None  # Remplacé par rnn_batch_size + qrnn_batch_size


class ColabPackage(BaseModel):
    """
    Package envoyé au worker Colab
    """
    file_id: str
    dataset_info: Dict[str, Any]  # Données brutes du dataset
    user_preferences: Dict[str, Any]  # Préférences utilisateur
    manual_overrides: Dict[str, Any]  # Overrides manuels


class JobStatus:
    """Statuts possibles d'un job"""
    UPLOADED = "uploaded"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(BaseModel):
    """
    Job d'entraînement complet
    """
    id: str
    filename: str
    file_path: str
    status: str = JobStatus.UPLOADED
    
    # Données
    dataset_info: Optional[DatasetInfo] = None
    
    # Configuration (package envoyé au worker)
    config: Optional[Dict[str, Any]] = None
    
    # Résultats
    results: Optional[Dict[str, Any]] = None
    plots: Optional[Dict[str, Any]] = None
    
    # Status
    message: Optional[str] = None
    error: Optional[str] = None
    progress: int = 0

    # Propriétaire du job
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    
    # Timestamps
    created_at: datetime = datetime.now()
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Fichiers
    results_path: Optional[str] = None
    pdf_path: Optional[str] = None
    json_path: Optional[str] = None

    # Email report
    email_sent: bool = False
    email_sent_to: Optional[str] = None
    email_sent_at: Optional[datetime] = None
    email_error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True


class JobResponse(BaseModel):
    """
    Réponse légère pour le polling de statut
    """
    job_id: str
    status: str
    message: Optional[str] = None
    progress: Optional[int] = 0


class TrainingResults(BaseModel):
    """
    Résultats d'entraînement formatés pour le frontend
    """
    job_id: str
    status: str
    
    # RNN results
    rnn: Optional[Dict[str, Any]] = None
    
    # QRNN results
    qrnn: Optional[Dict[str, Any]] = None
    
    # Comparaison
    comparison: Optional[Dict[str, Any]] = None
    
    # Configuration utilisée
    config: Optional[Dict[str, Any]] = None
    
    # Timestamp
    timestamp: datetime = datetime.now()

