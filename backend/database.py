# backend/database.py
import json
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

# Imports absolus (sans points)
from models import Job, JobStatus

class SimpleDB:
    """Base de données simple basée sur des fichiers JSON"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.jobs_file = self.db_path / "jobs.json"
        self._load_jobs()
    
    def _load_jobs(self):
        """Charge les jobs depuis le fichier"""
        if self.jobs_file.exists():
            with open(self.jobs_file, 'r') as f:
                data = json.load(f)
                self.jobs = {
                    k: Job(**v) for k, v in data.items()
                }
        else:
            self.jobs = {}
    
    def _save_jobs(self):
        """Sauvegarde les jobs"""
        data = {
            k: v.dict() for k, v in self.jobs.items()
        }
        with open(self.jobs_file, 'w') as f:
            json.dump(data, f, default=str, indent=2)
    
    def create_job(self, job: Job) -> Job:
        """Crée un nouveau job"""
        self.jobs[job.id] = job
        self._save_jobs()
        return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Récupère un job par son ID"""
        return self.jobs.get(job_id)
    
    def update_job(self, job_id: str, **kwargs) -> Optional[Job]:
        """Met à jour un job"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            for key, value in kwargs.items():
                setattr(job, key, value)
            self._save_jobs()
            return job
        return None
    
    def update_status(self, job_id: str, status: str, **kwargs):
        """Met à jour le statut d'un job"""
        return self.update_job(job_id, status=status, **kwargs)
    
    def delete_job(self, job_id: str):
        """Supprime un job"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            self._save_jobs()

# Instance globale
db = SimpleDB(Path(__file__).parent / "data")
