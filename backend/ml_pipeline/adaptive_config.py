# # """
# # Configuration adaptative pour les modèles ML/Quantum
# # Calcule automatiquement les hyperparamètres optimaux selon le dataset

# # SOURCE UNIQUE DE VÉRITÉ - Utilisé par le backend ET les modèles
# # """
# # import math
# # import numpy as np

# # class AdaptiveConfig:
# #     """
# #     Calcule les paramètres optimaux selon:
# #     - Nombre de features
# #     - Nombre d'échantillons
# #     - Nombre de classes
# #     - Nombre de qubits
# #     """
    
# #     @staticmethod
# #     def compute_rnn_params(n_features, n_samples, n_classes):
# #         """
# #         Calcule les paramètres optimaux pour le RNN
        
# #         Args:
# #             n_features: nombre de features
# #             n_samples: nombre d'échantillons TOTAL
# #             n_classes: nombre de classes
# #         """
# #         # Hidden size adaptatif
# #         if n_features <= 10:
# #             hidden_size = 32
# #         elif n_features <= 50:
# #             hidden_size = 64
# #         elif n_features <= 100:
# #             hidden_size = 128
# #         else:
# #             hidden_size = 256
            
# #         # Nombre de couches LSTM
# #         if n_features <= 20:
# #             num_layers = 1
# #         elif n_features <= 100:
# #             num_layers = 2
# #         else:
# #             num_layers = 3
            
# #         # Dropout adaptatif - dépend du nombre d'échantillons
# #         if n_samples < 500:
# #             dropout = 0.3
# #         elif n_samples < 2000:
# #             dropout = 0.2
# #         else:
# #             dropout = 0.1
            
# #         # Learning rate
# #         learning_rate = 0.001 * (32 / max(16, hidden_size))
        
# #         # Batch size - dépend du nombre d'échantillons
# #         if n_samples < 200:
# #             batch_size = 16
# #         elif n_samples < 1000:
# #             batch_size = 32
# #         elif n_samples < 5000:
# #             batch_size = 64
# #         else:
# #             batch_size = 128
            
# #         # Époques recommandées - dépend du nombre d'échantillons
# #         if n_samples < 500:
# #             epochs = 50
# #         elif n_samples < 2000:
# #             epochs = 30
# #         elif n_samples < 10000:
# #             epochs = 20
# #         else:
# #             epochs = 15
            
# #         return {
# #             'hidden_size': hidden_size,
# #             'num_layers': num_layers,
# #             'dropout': dropout,
# #             'learning_rate': round(learning_rate, 5),
# #             'batch_size': batch_size,
# #             'epochs': epochs
# #         }
    
# #     @staticmethod
# #     def compute_qrnn_params(n_qubits, n_samples, n_classes):
# #         """
# #         Calcule les paramètres optimaux pour le QRNN (PennyLane & Qiskit)
        
# #         Règles:
# #         - n_layers = min(4, max(2, ceil(log2(n_qubits))))  → évite barren plateau
# #         - learning_rate = base_lr / sqrt(n_qubits)
# #         - epochs adapté à n_samples
        
# #         Args:
# #             n_qubits: nombre de qubits
# #             n_samples: nombre d'échantillons TOTAL
# #             n_classes: nombre de classes
# #         """
# #         # Nombre de couches quantiques (entre 2 et 4 pour éviter barren plateau)
# #         n_layers = min(4, max(2, int(math.ceil(math.log2(max(1, n_qubits))))))
        
# #         # Learning rate adaptatif
# #         base_lr = 0.01
# #         learning_rate = base_lr / math.sqrt(max(1, n_qubits))
        
# #         # Batch size
# #         if n_qubits <= 2:
# #             batch_size = 16
# #         elif n_qubits == 3:
# #             batch_size = 32
# #         elif n_qubits == 4:
# #             batch_size = 32
# #         elif n_qubits == 5:
# #             batch_size = 64
# #         else:
# #             batch_size = 64
            
# #         # Ajuster selon la taille du dataset
# #         if n_samples < 200:
# #             batch_size = min(batch_size, 8)
# #         elif n_samples < 1000:
# #             batch_size = min(batch_size, 32)
            
# #         # Époques recommandées - dépend de n_samples
# #         base_epochs = 20
# #         if n_qubits <= 2:
# #             base_epochs = 40
# #         elif n_qubits == 3:
# #             base_epochs = 30
# #         elif n_qubits == 4:
# #             base_epochs = 20
# #         elif n_qubits == 5:
# #             base_epochs = 15
# #         else:
# #             base_epochs = 10
            
# #         # Ajuster selon la taille du dataset
# #         if n_samples < 500:
# #             epochs = int(base_epochs * 1.5)
# #         elif n_samples > 5000:
# #             epochs = max(10, int(base_epochs * 0.7))
# #         else:
# #             epochs = base_epochs
            
# #         return {
# #             'n_layers': n_layers,
# #             'learning_rate': round(learning_rate, 5),
# #             'batch_size': batch_size,
# #             'epochs': epochs,
# #             'n_qubits': n_qubits
# #         }
    
# #     @staticmethod
# #     def compute_all_params(dataset_info):
# #         """
# #         Calcule tous les paramètres à partir des infos du dataset
        
# #         Args:
# #             dataset_info: dict avec 'samples', 'features', 'classes', 'recommended_qubits'
        
# #         Returns:
# #             dict complet avec tous les paramètres adaptatifs
# #         """
# #         n_samples = dataset_info.get('samples', 1000)
# #         n_features = dataset_info.get('features', 10)
# #         n_classes = dataset_info.get('classes', 2)
# #         n_qubits = dataset_info.get('recommended_qubits', 4)
        
# #         rnn_params = AdaptiveConfig.compute_rnn_params(n_features, n_samples, n_classes)
# #         qrnn_params = AdaptiveConfig.compute_qrnn_params(n_qubits, n_samples, n_classes)
        
# #         return {
# #             'rnn': rnn_params,
# #             'qrnn': qrnn_params,
# #             'dataset_summary': {
# #                 'samples': n_samples,
# #                 'features': n_features,
# #                 'classes': n_classes,
# #                 'qubits': n_qubits
# #             }
# #         }
    
# #     @staticmethod
# #     def print_config(params):
# #         """Affiche la configuration calculée"""
# #         print("\n" + "="*60)
# #         print("📊 CONFIGURATION ADAPTATIVE CALCULÉE")
# #         print("="*60)
# #         print(f"Dataset: {params['dataset_summary']['samples']} samples, "
# #               f"{params['dataset_summary']['features']} features, "
# #               f"{params['dataset_summary']['classes']} classes, "
# #               f"{params['dataset_summary']['qubits']} qubits")
        
# #         print(f"\n📈 RNN:")
# #         for k, v in params['rnn'].items():
# #             print(f"   {k}: {v}")
            
# #         print(f"\n⚛️ QRNN:")
# #         for k, v in params['qrnn'].items():
# #             print(f"   {k}: {v}")
# #         print("="*60 + "\n")


# #NEW CODE AVEC GPT5 POUR FLEXIBILITY AND NO EPOCH NOT LIKE PREVIOUS ONE _________________________________________________________________________________________#

# # backend/app.py
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# import pandas as pd
# import numpy as np
# import uuid
# import shutil
# import json
# import base64
# import re
# import sys
# from datetime import datetime
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent.parent))

# from config import config
# from models import Job, JobStatus, DatasetInfo, TrainingRequest
# from database import db
# from ml_pipeline.adaptive_config import AdaptiveConfig

# app = FastAPI(title="Quantum RNN Platform API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def is_feature_column(column_name: str) -> bool:
#     column_lower = column_name.lower().strip()
#     ignore_words = ['id', 'identifier', 'index', 'unnamed', 'row', 'rowid',
#                     'class', 'target', 'output', 'label', 'prediction', 'result',
#                     'y', 'response', 'dependent', 'outcome',
#                     'date', 'time', 'timestamp', 'created_at', 'updated_at']
#     for word in ignore_words:
#         if (word == column_lower or 
#             column_lower.startswith(word + '_') or 
#             column_lower.endswith('_' + word) or 
#             f'_{word}_' in column_lower):
#             return False
#     return True


# @app.get("/")
# async def root():
#     return {"message": "Quantum RNN Platform API", "status": "operational"}


# @app.post("/api/upload")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         if not file.filename.endswith('.csv'):
#             raise HTTPException(400, "Seuls les fichiers CSV sont acceptés")
        
#         file_id = str(uuid.uuid4())
#         file_path = config.UPLOAD_DIR / f"{file_id}_{file.filename}"
        
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         with open(file_path, 'r') as f:
#             first_line = f.readline().strip()
#         separator = ';' if ';' in first_line else ','

#         df = pd.read_csv(file_path, sep=separator)

#         target_col = None
#         target_keywords = ['class', 'target', 'output', 'label', 'y', 'result']
#         for col in df.columns:
#             if any(k in col.lower() for k in target_keywords):
#                 target_col = col
#                 break
#         if not target_col:
#             target_col = df.columns[-1]

#         feature_cols = [col for col in df.columns if col != target_col and is_feature_column(col)]

#         n_samples = len(df)
#         n_features = len(feature_cols)
#         n_classes = df[target_col].nunique()
#         n_qubits = max(2, min(6, int(np.log2(n_features)) if n_features > 0 else 2))

#         adaptive_params = AdaptiveConfig.compute_all_params({
#             "samples": n_samples,
#             "features": n_features,
#             "classes": n_classes,
#             "recommended_qubits": n_qubits
#         })
        
#         AdaptiveConfig.print_config(adaptive_params)

#         rnn = adaptive_params['rnn']
#         qrnn = adaptive_params['qrnn']

#         dataset_info = DatasetInfo(
#             samples=n_samples,
#             features=n_features,
#             classes=n_classes,
#             target_column=target_col,
#             recommended_qubits=n_qubits,
#             pca_dimension=2**n_qubits,
#             rnn_hidden_size=rnn.get('hidden_size'),
#             rnn_num_layers=rnn.get('num_layers'),
#             rnn_dropout=rnn.get('dropout'),
#             rnn_learning_rate=rnn.get('learning_rate'),
#             qrnn_layers=qrnn.get('n_layers'),
#             qrnn_learning_rate=qrnn.get('learning_rate'),
#             recommended_batch_size=qrnn.get('batch_size')
#         )

#         job = Job(
#             id=file_id,
#             filename=file.filename,
#             file_path=str(file_path),
#             dataset_info=dataset_info,
#             status=JobStatus.UPLOADED
#         )
#         db.create_job(job)

#         return {
#             "success": True,
#             "file_id": file_id,
#             "dataset_info": dataset_info.dict()
#         }
#     except Exception as e:
#         raise HTTPException(500, str(e))


# @app.post("/api/train/{file_id}")
# async def start_training(file_id: str, request: TrainingRequest):
#     job = db.get_job(file_id)
#     if not job:
#         raise HTTPException(404, "Job non trouvé")

#     config_data = request.dict()
#     di = job.dataset_info
    
#     # Construire manual_overrides (user ONLY)
#     manual_overrides = {}

#     if config_data.get("rnn_epochs") is not None:
#         manual_overrides["rnn_epochs"] = config_data["rnn_epochs"]
#     if config_data.get("qrnn_epochs") is not None:
#         manual_overrides["qrnn_epochs"] = config_data["qrnn_epochs"]
#     if config_data.get("rnn_batch_size") is not None:
#         manual_overrides["rnn_batch_size"] = config_data["rnn_batch_size"]
#     if config_data.get("qrnn_batch_size") is not None:
#         manual_overrides["qrnn_batch_size"] = config_data["qrnn_batch_size"]
#     if config_data.get("batch_size") is not None:
#         manual_overrides.setdefault("rnn_batch_size", config_data["batch_size"])
#         manual_overrides.setdefault("qrnn_batch_size", config_data["batch_size"])
#     if config_data.get("qrnn_layers") is not None:
#         manual_overrides["qrnn_layers"] = config_data["qrnn_layers"]
#     if config_data.get("qrnn_learning_rate") is not None:
#         manual_overrides["qrnn_learning_rate"] = config_data["qrnn_learning_rate"]
#     if config_data.get("rnn_hidden_size") is not None:
#         manual_overrides["rnn_hidden_size"] = config_data["rnn_hidden_size"]
#     if config_data.get("rnn_num_layers") is not None:
#         manual_overrides["rnn_num_layers"] = config_data["rnn_num_layers"]
#     if config_data.get("rnn_dropout") is not None:
#         manual_overrides["rnn_dropout"] = config_data["rnn_dropout"]

#     # 🔥 FIX 1 : Garder le package complet dans job.config
#     colab_package = {
#         "config": {
#             "model_types": config_data.get("model_types", ["rnn", "qrnn"]),
#             "comparison_mode": config_data.get("comparison_mode", "pca"),
#             "qrnn_backend": config_data.get("qrnn_backend", "pennylane"),
#             "noise_enabled": config_data.get("noise_enabled", False),
#             "noise_level": config_data.get("noise_level", 0.0),
#             "mitigation_enabled": config_data.get("mitigation_enabled", False),
#             "mitigation_runs": config_data.get("mitigation_runs", 1),
#             "manual_overrides": manual_overrides,
#         },
#         "dataset_info": di.dict() if di else {},
#         "adaptive_config": AdaptiveConfig.compute_all_params({
#             "samples": di.samples if di else 1000,
#             "features": di.features if di else 10,
#             "classes": di.classes if di else 2,
#             "recommended_qubits": di.recommended_qubits if di else 4,
#         }) if di else {}
#     }

#     # 🔥 FIX 1 : Stocker le package complet
#     job.config = colab_package
#     db.update_status(file_id, JobStatus.QUEUED)

#     return {"success": True, "job_id": file_id}


# @app.get("/api/next-job")
# async def get_next_job():
#     for job_id, job in db.jobs.items():
#         if job.status == JobStatus.QUEUED:
#             db.update_status(job_id, JobStatus.PROCESSING)
#             # 🔥 FIX 1 : Extraire le config propre du package complet
#             return {
#                 "file_id": job_id,
#                 "config": job.config.get("config", {}) if isinstance(job.config, dict) else job.config,
#                 "dataset_info": job.dataset_info.dict() if job.dataset_info else {},
#                 "adaptive_config": job.config.get("adaptive_config", {}) if isinstance(job.config, dict) else {}
#             }
#     return {"message": "Aucun job en attente"}


# @app.get("/api/dataset/{file_id}")
# async def download_dataset(file_id: str):
#     job = db.get_job(file_id)
#     if not job or not Path(job.file_path).exists():
#         raise HTTPException(404, "Fichier non trouvé")
#     return FileResponse(job.file_path, media_type='text/csv', filename=job.filename)


# @app.post("/api/job/{file_id}/complete")
# async def complete_job(file_id: str, results: dict):
#     job = db.get_job(file_id)
#     if not job:
#         raise HTTPException(404, "Job non trouvé")

#     results_path = config.RESULTS_DIR / f"{file_id}_results.json"
#     with open(results_path, 'w') as f:
#         json.dump(results, f, indent=2)

#     db.update_status(file_id, JobStatus.COMPLETED, results_path=str(results_path), results=results)
#     return {"success": True}


# @app.get("/api/job/{job_id}/status")
# async def get_job_status(job_id: str):
#     job = db.get_job(job_id)
#     if not job:
#         raise HTTPException(404, "Job non trouvé")
    
#     return {
#         "job_id": job.id,
#         "status": job.status,
#         "progress": job.progress,
#         "message": "En cours..." if job.status == JobStatus.PROCESSING else "Terminé"
#     }


# @app.get("/api/results/{job_id}")
# async def get_results_frontend(job_id: str):
#     job = db.get_job(job_id)
#     if not job or job.status != JobStatus.COMPLETED:
#         raise HTTPException(404, "Résultats non disponibles")

#     with open(job.results_path, 'r') as f:
#         results = json.load(f)

#     formatted = {}

#     if 'rnn' in results:
#         r = results['rnn']
#         formatted['rnn'] = {
#             'accuracy': r.get('accuracy', 0),
#             'f1_score': r.get('f1_score', 0),
#             'precision': r.get('precision', 0),
#             'recall': r.get('recall', 0),
#             'loss': r.get('loss', None),
#             'classification_report': r.get('classification_report', None)
#         }

#     if 'qrnn' in results:
#         qrnn_data = results['qrnn']
        
#         if isinstance(qrnn_data, dict) and 'noisy' in qrnn_data:
#             noisy = qrnn_data['noisy']
#             mitigated = qrnn_data.get('mitigated', {})
            
#             formatted['qrnn'] = {
#                 'noisy': {
#                     'accuracy': noisy.get('accuracy', 0),
#                     'f1_score': noisy.get('f1_score', 0),
#                     'precision': noisy.get('precision', 0),
#                     'recall': noisy.get('recall', 0),
#                     'loss': noisy.get('loss', None),
#                     'classification_report': noisy.get('classification_report', None)
#                 },
#                 'mitigated': {
#                     'accuracy': mitigated.get('accuracy', 0),
#                     'f1_score': mitigated.get('f1_score', 0),
#                     'precision': mitigated.get('precision', 0),
#                     'recall': mitigated.get('recall', 0),
#                     'loss': mitigated.get('loss', None),
#                     'classification_report': mitigated.get('classification_report', None),
#                     'mitigation_runs': job.config.get('config', {}).get('mitigation_runs', 1) if isinstance(job.config, dict) else 1
#                 }
#             }
#         else:
#             formatted['qrnn'] = {
#                 'accuracy': qrnn_data.get('accuracy', 0),
#                 'f1_score': qrnn_data.get('f1_score', 0),
#                 'precision': qrnn_data.get('precision', 0),
#                 'recall': qrnn_data.get('recall', 0),
#                 'loss': qrnn_data.get('loss', None),
#                 'classification_report': qrnn_data.get('classification_report', None)
#             }

#     if 'comparison' in results:
#         formatted['comparison'] = results['comparison']

#     return formatted


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

#ABOVE ERROR NO MODULE CONFIG DANS COLAB UNDER NEW VERSION THAT SUPPOSED TO FIX ISSUE AND IMPORT CORRECTLY THE CONFIG MODULE___________________________________________________________#

"""
Configuration adaptative pour les modèles ML/Quantum.

Important:
- Les epochs ne sont PAS décidées ici.
- Les epochs viennent uniquement du frontend/user via manual_overrides.
- Le modèle classique est un MLP, pas un LSTM.
- AUCUN import de config backend (compatible Colab).
"""

import math


class AdaptiveConfig:
    """
    Calcule seulement les hyperparamètres structurels selon:
    - nombre de features
    - nombre d'échantillons
    - nombre de classes
    - nombre de qubits

    Les epochs restent contrôlées par l'utilisateur.
    """

    @staticmethod
    def compute_mlp_params(n_features, n_samples, n_classes):
        """
        Paramètres adaptatifs pour le MLP classique.

        hidden_size:
            largeur des couches cachées du MLP.

        num_layers:
            nombre de couches cachées du MLP.
            Ce n'est PAS un nombre de couches LSTM.
        """

        if n_features <= 10:
            hidden_size = 32
        elif n_features <= 50:
            hidden_size = 64
        elif n_features <= 100:
            hidden_size = 128
        else:
            hidden_size = 256

        if n_features <= 20:
            num_layers = 1
        elif n_features <= 100:
            num_layers = 2
        else:
            num_layers = 3

        if n_samples < 500:
            dropout = 0.3
        elif n_samples < 2000:
            dropout = 0.2
        else:
            dropout = 0.1

        learning_rate = 0.001 * (32 / max(16, hidden_size))

        if n_samples < 200:
            batch_size = 16
        elif n_samples < 1000:
            batch_size = 32
        elif n_samples < 5000:
            batch_size = 64
        else:
            batch_size = 128

        return {
            "hidden_size": hidden_size,
            "num_layers": num_layers,
            "dropout": dropout,
            "learning_rate": round(learning_rate, 5),
            "batch_size": batch_size,
            "epochs": None,  # Plus d'epochs calculées ici
        }

    @staticmethod
    def compute_rnn_params(n_features, n_samples, n_classes):
        """
        Compatibilité avec l'ancien code.

        Le nom historique est compute_rnn_params, mais le modèle utilisé
        côté classique est maintenant un MLP.
        """
        return AdaptiveConfig.compute_mlp_params(
            n_features=n_features,
            n_samples=n_samples,
            n_classes=n_classes,
        )

    @staticmethod
    def compute_qrnn_params(n_qubits, n_samples, n_classes):
        """
        Paramètres adaptatifs pour QRNN.

        Les epochs ne sont PAS calculées ici.
        Elles doivent venir du user via manual_overrides["qrnn_epochs"].
        """

        n_layers = min(
            4,
            max(2, int(math.ceil(math.log2(max(1, n_qubits)))))
        )

        base_lr = 0.01
        learning_rate = base_lr / math.sqrt(max(1, n_qubits))

        if n_qubits <= 2:
            batch_size = 16
        elif n_qubits <= 4:
            batch_size = 32
        else:
            batch_size = 64

        if n_samples < 200:
            batch_size = min(batch_size, 8)
        elif n_samples < 1000:
            batch_size = min(batch_size, 32)

        return {
            "n_layers": n_layers,
            "learning_rate": round(learning_rate, 5),
            "batch_size": batch_size,
            "epochs": None,  # Plus d'epochs calculées ici
            "n_qubits": n_qubits,
        }

    @staticmethod
    def compute_all_params(dataset_info):
        n_samples = dataset_info.get("samples", 1000)
        n_features = dataset_info.get("features", 10)
        n_classes = dataset_info.get("classes", 2)
        n_qubits = dataset_info.get("recommended_qubits", 4)

        mlp_params = AdaptiveConfig.compute_mlp_params(
            n_features=n_features,
            n_samples=n_samples,
            n_classes=n_classes,
        )

        qrnn_params = AdaptiveConfig.compute_qrnn_params(
            n_qubits=n_qubits,
            n_samples=n_samples,
            n_classes=n_classes,
        )

        return {
            "rnn": mlp_params,     # compatibilité ancien code
            "mlp": mlp_params,
            "qrnn": qrnn_params,
            "dataset_summary": {
                "samples": n_samples,
                "features": n_features,
                "classes": n_classes,
                "qubits": n_qubits,
            },
        }

    @staticmethod
    def print_config(params):
        print("\n" + "=" * 60)
        print("📊 CONFIGURATION ADAPTATIVE CALCULÉE")
        print("=" * 60)

        summary = params["dataset_summary"]
        print(
            f"Dataset: {summary['samples']} samples, "
            f"{summary['features']} features, "
            f"{summary['classes']} classes, "
            f"{summary['qubits']} qubits"
        )

        print("\n📈 MLP classique:")
        for k, v in params["rnn"].items():
            print(f"   {k}: {v}")

        print("\n⚛️ QRNN:")
        for k, v in params["qrnn"].items():
            print(f"   {k}: {v}")

        print("=" * 60 + "\n")