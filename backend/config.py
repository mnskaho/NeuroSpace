# backend/config.py
import os
from pathlib import Path


def load_local_env_files():
    """
    Charge les fichiers .env uniquement en local.
    En production, Render/Vercel utilisent leurs Environment Variables.
    """
    base_dir = Path(__file__).parent.parent

    env_files = [
        base_dir / "backend" / ".env.local",
        base_dir / "backend" / ".env",
        base_dir / "frontend" / ".env.local",
        base_dir / "frontend" / ".env",
    ]

    for env_path in env_files:
        if not env_path.exists():
            continue

        for line in env_path.read_text(
            encoding="utf-8",
            errors="ignore"
        ).splitlines():
            stripped = line.strip()

            if (
                not stripped
                or stripped.startswith("#")
                or "=" not in stripped
            ):
                continue

            key, value = stripped.split("=", 1)

            os.environ.setdefault(
                key.strip(),
                value.strip().strip('"').strip("'")
            )


load_local_env_files()


class Config:
    # =========================
    # PATHS
    # =========================

    BASE_DIR = Path(__file__).parent.parent

    UPLOAD_DIR = Path(
        os.getenv(
            "UPLOAD_DIR",
            BASE_DIR / "backend" / "uploads"
        )
    )

    RESULTS_DIR = Path(
        os.getenv(
            "RESULTS_DIR",
            BASE_DIR / "backend" / "results"
        )
    )

    # =========================
    # FILE CONFIG
    # =========================

    MAX_FILE_SIZE_MB = int(
        os.getenv("MAX_FILE_SIZE_MB", "100")
    )

    ALLOWED_EXTENSIONS = {".csv"}

    # =========================
    # FRONTEND URL
    # =========================
    # Local:
    # http://localhost:3000
    #
    # Production:
    # https://neuro-space-teal.vercel.app

    APP_URL = os.getenv(
        "NEXT_PUBLIC_APP_URL",
        os.getenv(
            "APP_URL",
            "http://localhost:3000"
        )
    ).rstrip("/")

    # =========================
    # BACKEND URL
    # =========================
    # Local:
    # http://localhost:7000
    #
    # Production Render:
    # https://ton-backend.onrender.com

    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        os.getenv(
            "COLAB_API_URL",
            "http://localhost:7000"
        )
    ).rstrip("/")

    COLAB_API_URL = BACKEND_URL

    # =========================
    # SUPABASE
    # =========================

    SUPABASE_URL = os.getenv(
        "SUPABASE_URL",
        os.getenv("NEXT_PUBLIC_SUPABASE_URL", "")
    )

    SUPABASE_ANON_KEY = os.getenv(
        "SUPABASE_ANON_KEY",
        os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "")
    )

    SUPABASE_SERVICE_ROLE_KEY = os.getenv(
        "SUPABASE_SERVICE_ROLE_KEY",
        ""
    )

    # =========================
    # EMAIL
    # =========================

    RESEND_API_KEY = os.getenv(
        "RESEND_API_KEY",
        ""
    )

    EMAIL_FROM = os.getenv(
        "EMAIL_FROM",
        "NeuroSpace <onboarding@resend.dev>"
    )

    # =========================
    # CORS
    # =========================

    CORS_ORIGINS = [
        origin.strip().rstrip("/")
        for origin in os.getenv(
            "CORS_ORIGINS",
            ",".join(
                [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                    APP_URL,
                ]
            ),
        ).split(",")
        if origin.strip()
    ]

    # =========================
    # INIT
    # =========================

    def __init__(self):
        self.UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.RESULTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        print("Configuration chargée:")
        print(f"   - Uploads: {self.UPLOAD_DIR}")
        print(f"   - Results: {self.RESULTS_DIR}")
        print(f"   - App URL: {self.APP_URL}")
        print(f"   - Backend URL: {self.BACKEND_URL}")
        print(f"   - Colab URL: {self.COLAB_API_URL}")
        print(f"   - CORS Origins: {self.CORS_ORIGINS}")
        print(f"   - Supabase URL: {'OK' if self.SUPABASE_URL else 'Missing'}")
        print(f"   - Supabase anon key: {'OK' if self.SUPABASE_ANON_KEY else 'Missing'}")
        print(f"   - Supabase service key: {'OK' if self.SUPABASE_SERVICE_ROLE_KEY else 'Missing'}")


config = Config()
