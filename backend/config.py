# backend/config.py
import os
from pathlib import Path


def load_local_env_files():
    base_dir = Path(__file__).parent.parent
    for env_path in [
        base_dir / "backend" / ".env.local",
        base_dir / "backend" / ".env",
        base_dir / "frontend" / ".env.local",
        base_dir / "frontend" / ".env",
    ]:
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_env_files()


class Config:
    # Chemins
    BASE_DIR = Path(__file__).parent.parent
    UPLOAD_DIR = BASE_DIR / "backend" / "uploads"
    RESULTS_DIR = BASE_DIR / "backend" / "results"

    # Configuration
    MAX_FILE_SIZE_MB = 100
    ALLOWED_EXTENSIONS = {".csv"}

    # URLs - pour que Colab puisse communiquer avec le backend
    COLAB_API_URL = os.getenv("COLAB_API_URL", "http://localhost:7000")
    SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "NeuroSpace <onboarding@resend.dev>")
    APP_URL = os.getenv("NEXT_PUBLIC_APP_URL", "http://localhost:3000")

    # Creer les dossiers
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    def __init__(self):
        print("Configuration chargee:")
        print(f"   - Uploads: {self.UPLOAD_DIR}")
        print(f"   - Results: {self.RESULTS_DIR}")
        print(f"   - Colab URL: {self.COLAB_API_URL}")


config = Config()
