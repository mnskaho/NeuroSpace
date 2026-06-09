# import os
# import json
# import uuid
# import shutil
# import smtplib
# import sys
# import traceback
# from pathlib import Path
# from datetime import datetime, timezone
# from email.message import EmailMessage

# import requests
# import pandas as pd
# import numpy as np

# from fastapi import FastAPI, UploadFile, File, HTTPException, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse, Response

# if hasattr(sys.stdout, "reconfigure"):
#     sys.stdout.reconfigure(encoding="utf-8", errors="replace")
# if hasattr(sys.stderr, "reconfigure"):
#     sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# # ============================================================
# # LOAD .ENV FROM BACKEND FOLDER
# # ============================================================

# BASE_DIR = Path(__file__).resolve().parent
# ENV_PATH = BASE_DIR / ".env"

# try:
#     from dotenv import load_dotenv

#     load_dotenv(ENV_PATH)
#     print("✅ .env loaded from:", ENV_PATH)
# except Exception as e:
#     print("⚠️ dotenv not loaded:", e)


# # ============================================================
# # CONFIG
# # ============================================================

# UPLOAD_DIR = BASE_DIR / "uploads"
# RESULTS_DIR = BASE_DIR / "results"

# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# SUPABASE_URL = (
#     os.getenv("SUPABASE_URL")
#     or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
# )

# SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# SUPABASE_TABLE = "training_jobs"

# BREVO_SMTP_HOST = os.getenv("BREVO_SMTP_HOST", "smtp-relay.brevo.com")
# BREVO_SMTP_PORT = int(os.getenv("BREVO_SMTP_PORT", "587"))
# BREVO_SMTP_USER = os.getenv("BREVO_SMTP_USER")
# BREVO_SMTP_PASSWORD = os.getenv("BREVO_SMTP_PASSWORD")
# EMAIL_FROM = os.getenv("EMAIL_FROM")
# APP_URL = os.getenv("NEXT_PUBLIC_APP_URL") or os.getenv("APP_URL") or "http://localhost:3000"


# def now_iso():
#     return datetime.now(timezone.utc).isoformat()


# def require_supabase_env():
#     if not SUPABASE_URL:
#         raise RuntimeError(
#             "SUPABASE_URL manquant. Mets SUPABASE_URL dans backend/.env"
#         )

#     if not SUPABASE_SERVICE_ROLE_KEY:
#         raise RuntimeError(
#             "SUPABASE_SERVICE_ROLE_KEY manquant. Mets SUPABASE_SERVICE_ROLE_KEY dans backend/.env"
#         )


# def supabase_headers(prefer: str | None = None):
#     require_supabase_env()

#     headers = {
#         "apikey": SUPABASE_SERVICE_ROLE_KEY,
#         "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
#         "Content-Type": "application/json",
#     }

#     if prefer:
#         headers["Prefer"] = prefer

#     return headers


# def supabase_rest_url(table: str):
#     require_supabase_env()
#     return f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table}"


# def supabase_select_one_by_file_id(file_id: str):
#     url = supabase_rest_url(SUPABASE_TABLE)

#     params = {
#         "file_id": f"eq.{file_id}",
#         "select": "*",
#         "limit": "1",
#     }

#     response = requests.get(
#         url,
#         headers=supabase_headers(),
#         params=params,
#         timeout=30,
#     )

#     if response.status_code >= 400:
#         raise RuntimeError(
#             f"Supabase select error: {response.status_code} - {response.text}"
#         )

#     rows = response.json()

#     if not rows:
#         return None

#     return rows[0]


# def supabase_update_by_file_id(file_id: str, data: dict):
#     url = supabase_rest_url(SUPABASE_TABLE)

#     params = {
#         "file_id": f"eq.{file_id}",
#     }

#     payload = {
#         **data,
#         "updated_at": now_iso(),
#     }

#     response = requests.patch(
#         url,
#         headers=supabase_headers(prefer="return=representation"),
#         params=params,
#         json=payload,
#         timeout=30,
#     )

#     if response.status_code >= 400:
#         raise RuntimeError(
#             f"Supabase update error: {response.status_code} - {response.text}"
#         )

#     return response.json()


# def make_json_serializable(obj):
#     if isinstance(obj, dict):
#         return {str(k): make_json_serializable(v) for k, v in obj.items()}

#     if isinstance(obj, list):
#         return [make_json_serializable(v) for v in obj]

#     if isinstance(obj, tuple):
#         return [make_json_serializable(v) for v in obj]

#     if isinstance(obj, np.ndarray):
#         return obj.tolist()

#     if isinstance(obj, (np.integer,)):
#         return int(obj)

#     if isinstance(obj, (np.floating,)):
#         return float(obj)

#     if isinstance(obj, (np.bool_)):
#         return bool(obj)

#     return obj


# def format_training_time_seconds(value):
#     if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
#         return None

#     if value < 60:
#         return f"{value:.2f}s"

#     total_seconds = float(value)
#     hours = int(total_seconds // 3600)
#     minutes = int((total_seconds % 3600) // 60)
#     seconds = total_seconds % 60

#     if hours:
#         return f"{hours}h {minutes}m {seconds:.2f}s"
#     return f"{minutes}m {seconds:.2f}s"


# def get_training_time_formatted(block):
#     if not isinstance(block, dict):
#         return "-"

#     formatted = block.get("training_time_formatted")
#     if isinstance(formatted, str) and formatted.strip():
#         return formatted

#     formatted = format_training_time_seconds(block.get("training_time_seconds"))
#     return formatted or "-"


# def ensure_training_times(results):
#     if not isinstance(results, dict):
#         return results

#     def normalize_block(block):
#         if not isinstance(block, dict):
#             return
#         if isinstance(block.get("training_time_formatted"), str) and block["training_time_formatted"].strip():
#             return
#         formatted = format_training_time_seconds(block.get("training_time_seconds"))
#         if formatted:
#             block["training_time_formatted"] = formatted

#     def training_time_payload(block):
#         if not isinstance(block, dict):
#             return None

#         seconds = block.get("training_time_seconds")
#         formatted = get_training_time_formatted(block)

#         if formatted == "-" and not isinstance(seconds, (int, float)):
#             return None

#         payload = {"training_time_formatted": formatted}
#         if isinstance(seconds, (int, float)) and not isinstance(seconds, bool):
#             payload["training_time_seconds"] = seconds
#         return payload

#     normalize_block(results.get("rnn"))

#     qrnn = results.get("qrnn")
#     if isinstance(qrnn, dict):
#         has_variant = False
#         for variant in ["clean", "noisy", "mitigated"]:
#             if isinstance(qrnn.get(variant), dict):
#                 normalize_block(qrnn[variant])
#                 has_variant = True
#         if not has_variant:
#             normalize_block(qrnn)

#     training_times = {}
#     rnn_time = training_time_payload(results.get("rnn"))
#     if rnn_time:
#         training_times["rnn"] = rnn_time

#     qrnn_main_time = None
#     if isinstance(qrnn, dict):
#         for variant in ["clean", "noisy", "mitigated"]:
#             variant_time = training_time_payload(qrnn.get(variant))
#             if variant_time:
#                 training_times[f"qrnn_{variant}"] = variant_time
#                 if variant in ["mitigated", "noisy", "clean"]:
#                     qrnn_main_time = variant_time
#         if not training_times.get("qrnn_clean") and not training_times.get("qrnn_noisy") and not training_times.get("qrnn_mitigated"):
#             qrnn_main_time = training_time_payload(qrnn)
#             if qrnn_main_time:
#                 training_times["qrnn"] = qrnn_main_time

#     if training_times:
#         results["training_times"] = training_times

#     comparison = results.get("comparison")
#     if isinstance(comparison, dict):
#         if rnn_time:
#             comparison["rnn_training_time_formatted"] = rnn_time["training_time_formatted"]
#             if "training_time_seconds" in rnn_time:
#                 comparison["rnn_training_time_seconds"] = rnn_time["training_time_seconds"]

#         for key, prefix in [
#             ("qrnn_clean", "qrnn_clean"),
#             ("qrnn_noisy", "qrnn_noisy"),
#             ("qrnn_mitigated", "qrnn_mitigated"),
#         ]:
#             model_time = training_times.get(key)
#             if model_time:
#                 comparison[f"{prefix}_training_time_formatted"] = model_time["training_time_formatted"]
#                 if "training_time_seconds" in model_time:
#                     comparison[f"{prefix}_training_time_seconds"] = model_time["training_time_seconds"]

#         if qrnn_main_time:
#             comparison["qrnn_training_time_formatted"] = qrnn_main_time["training_time_formatted"]
#             if "training_time_seconds" in qrnn_main_time:
#                 comparison["qrnn_training_time_seconds"] = qrnn_main_time["training_time_seconds"]

#     return results


# def coerce_json_object(value):
#     if isinstance(value, dict):
#         return value

#     if isinstance(value, str) and value.strip():
#         try:
#             parsed = json.loads(value)
#             if isinstance(parsed, dict):
#                 return parsed
#         except json.JSONDecodeError:
#             pass

#     return {}


# def coerce_int(value, default):
#     if isinstance(value, bool):
#         return default

#     try:
#         if value is None or value == "":
#             return default
#         return int(value)
#     except (TypeError, ValueError):
#         return default


# def coerce_float(value, default):
#     if isinstance(value, bool):
#         return default

#     try:
#         if value is None or value == "":
#             return default
#         return float(value)
#     except (TypeError, ValueError):
#         return default


# def coerce_bool(value, default=False):
#     if isinstance(value, bool):
#         return value

#     if isinstance(value, str):
#         lower_value = value.strip().lower()
#         if lower_value in {"true", "1", "yes", "on"}:
#             return True
#         if lower_value in {"false", "0", "no", "off"}:
#             return False

#     return default


# def normalize_training_config(raw_config):
#     """
#     Retourne toujours une config compatible worker Colab.
#     Accepte les formats:
#     - {user_preferences, manual_overrides}
#     - config plate: {model_types, rnn_epochs, ...}
#     - {config: {...}}
#     - null / {}
#     """
#     config = coerce_json_object(raw_config)

#     if isinstance(config.get("config"), dict):
#         nested_config = coerce_json_object(config.get("config"))
#         if "user_preferences" not in config and "manual_overrides" not in config:
#             config = nested_config

#     user_preferences = coerce_json_object(config.get("user_preferences"))
#     manual_overrides = coerce_json_object(config.get("manual_overrides"))

#     comparison_mode = (
#         user_preferences.get("comparison_mode")
#         or config.get("comparison_mode")
#         or "pca"
#     )
#     feature_selector = (
#         user_preferences.get("feature_selector")
#         or config.get("feature_selector")
#         or comparison_mode
#     )
#     batch_size = coerce_int(
#         manual_overrides.get("batch_size", config.get("batch_size")),
#         32,
#     )

#     normalized_user_preferences = {
#         "model_types": (
#             user_preferences.get("model_types")
#             or config.get("model_types")
#             or ["rnn", "qrnn"]
#         ),
#         "comparison_mode": comparison_mode,
#         "feature_selector": feature_selector,
#         "qrnn_backend": (
#             user_preferences.get("qrnn_backend")
#             or config.get("qrnn_backend")
#             or "pennylane"
#         ),
#         "noise_enabled": coerce_bool(
#             user_preferences.get("noise_enabled", config.get("noise_enabled")),
#             False,
#         ),
#         "noise_level": coerce_float(
#             user_preferences.get("noise_level", config.get("noise_level")),
#             0.0,
#         ),
#         "mitigation_enabled": coerce_bool(
#             user_preferences.get("mitigation_enabled", config.get("mitigation_enabled")),
#             False,
#         ),
#         "mitigation_runs": coerce_int(
#             user_preferences.get("mitigation_runs", config.get("mitigation_runs")),
#             1,
#         ),
#     }

#     if not isinstance(normalized_user_preferences["model_types"], list):
#         normalized_user_preferences["model_types"] = ["rnn", "qrnn"]

#     normalized_manual_overrides = {
#         "rnn_epochs": coerce_int(
#             manual_overrides.get("rnn_epochs", config.get("rnn_epochs")),
#             30,
#         ),
#         "qrnn_epochs": coerce_int(
#             manual_overrides.get("qrnn_epochs", config.get("qrnn_epochs")),
#             20,
#         ),
#         "batch_size": batch_size,
#         "rnn_batch_size": coerce_int(
#             manual_overrides.get("rnn_batch_size", config.get("rnn_batch_size")),
#             batch_size,
#         ),
#         "qrnn_batch_size": coerce_int(
#             manual_overrides.get("qrnn_batch_size", config.get("qrnn_batch_size")),
#             batch_size,
#         ),
#     }

#     return {
#         "user_preferences": normalized_user_preferences,
#         "manual_overrides": normalized_manual_overrides,
#     }


# # ============================================================
# # FASTAPI APP
# # ============================================================

# app = FastAPI(title="NeuroSpace Backend API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/favicon.ico")
# async def favicon():
#     return Response(status_code=204)


# @app.get("/")
# async def root():
#     return {
#         "message": "NeuroSpace Backend API",
#         "status": "operational",
#         "env_path": str(ENV_PATH),
#         "supabase_url_exists": bool(SUPABASE_URL),
#         "service_role_exists": bool(SUPABASE_SERVICE_ROLE_KEY),
#         "upload_dir": str(UPLOAD_DIR),
#         "results_dir": str(RESULTS_DIR),
#     }


# # ============================================================
# # DATASET HELPERS
# # ============================================================

# def detect_separator(file_path: Path):
#     with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#         first_line = f.readline().strip()

#     if ";" in first_line:
#         return ";"

#     return ","


# def is_feature_column(column_name: str) -> bool:
#     column_lower = column_name.lower().strip()

#     ignore_words = [
#         "id",
#         "identifier",
#         "index",
#         "unnamed",
#         "row",
#         "rowid",
#         "class",
#         "target",
#         "output",
#         "label",
#         "prediction",
#         "result",
#         "y",
#         "response",
#         "dependent",
#         "outcome",
#         "date",
#         "time",
#         "timestamp",
#         "created_at",
#         "updated_at",
#     ]

#     for word in ignore_words:
#         if (
#             word == column_lower
#             or column_lower.startswith(word + "_")
#             or column_lower.endswith("_" + word)
#             or f"_{word}_" in column_lower
#         ):
#             return False

#     return True


# def build_dataset_info(file_path: Path):
#     separator = detect_separator(file_path)
#     df = pd.read_csv(file_path, sep=separator)

#     if df.isnull().any().any():
#         missing = df.columns[df.isnull().any()].tolist()
#         raise ValueError(f"Valeurs manquantes dans: {missing}")

#     all_columns = list(df.columns)

#     target_col = None
#     target_keywords = [
#         "class",
#         "target",
#         "output",
#         "label",
#         "y",
#         "result",
#         "outcome",
#     ]

#     for col in all_columns:
#         col_lower = col.lower().strip()

#         for keyword in target_keywords:
#             if (
#                 keyword == col_lower
#                 or col_lower.endswith("_" + keyword)
#                 or col_lower.startswith(keyword + "_")
#             ):
#                 target_col = col
#                 break

#         if target_col:
#             break

#     if not target_col:
#         target_col = all_columns[-1]

#     feature_cols = []

#     for col in all_columns:
#         if col == target_col:
#             continue

#         if is_feature_column(col):
#             feature_cols.append(col)

#     n_samples = int(len(df))
#     n_features = int(len(feature_cols))
#     n_classes = int(df[target_col].nunique())

#     if n_features > 0:
#         n_qubits = int(np.floor(np.log2(n_features)))
#         n_qubits = max(n_qubits, 1)
#     else:
#         n_qubits = 1

#     pca_dimension = int(2**n_qubits)

#     return {
#         "samples": n_samples,
#         "features": n_features,
#         "classes": n_classes,
#         "target_column": target_col,
#         "recommended_qubits": n_qubits,
#         "pca_dimension": pca_dimension,
#         "separator": separator,
#     }


# # ============================================================
# # UPLOAD DATASET
# # ============================================================

# @app.post("/api/upload")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         if not file.filename.lower().endswith(".csv"):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Seuls les fichiers CSV sont acceptés",
#             )

#         file_id = str(uuid.uuid4())
#         safe_filename = f"{file_id}_{file.filename}"
#         file_path = UPLOAD_DIR / safe_filename

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         dataset_info = build_dataset_info(file_path)

#         print(f"✅ Dataset uploaded: {file_id}")
#         print(f"   filename: {file.filename}")
#         print(f"   file_path: {file_path}")
#         print(f"   dataset_info: {dataset_info}")

#         return {
#             "success": True,
#             "file_id": file_id,
#             "filename": file.filename,
#             "file_path": str(file_path),
#             "dataset_info": dataset_info,
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ Upload error:", e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # QUEUE TRAINING
# # ============================================================

# @app.post("/api/train/{file_id}")
# async def start_training(file_id: str, request: Request):
#     try:
#         body = await request.json()

#         raw_config = body.get("config") or body
#         config = normalize_training_config(raw_config)
#         dataset_info = body.get("dataset_info") or coerce_json_object(raw_config).get("dataset_info") or {}

#         filename = body.get("filename")
#         file_path = body.get("file_path")

#         if not file_path:
#             matches = list(UPLOAD_DIR.glob(f"{file_id}_*.csv"))
#             if matches:
#                 file_path = str(matches[0])
#                 filename = filename or matches[0].name

#         existing_job = supabase_select_one_by_file_id(file_id)

#         if existing_job:
#             file_path = file_path or existing_job.get("file_path")
#             filename = filename or existing_job.get("filename")

#         if not file_path:
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "file_path introuvable. Le frontend doit envoyer file_path "
#                     "ou le backend doit trouver le CSV dans backend/uploads."
#                 ),
#             )

#         if not dataset_info:
#             dataset_info = build_dataset_info(Path(file_path))

#         if not existing_job:
#             raise HTTPException(
#                 status_code=404,
#                 detail=(
#                     "Job absent dans Supabase training_jobs. "
#                     "Le frontend doit créer la ligne avec user_id/user_email avant /api/train."
#                 ),
#             )

#         update_payload = {
#             "status": "queued",
#             "config": config,
#             "dataset_info": dataset_info,
#             "file_path": file_path,
#             "filename": filename,
#             "started_at": None,
#             "completed_at": None,
#             "error_message": None,
#         }

#         supabase_update_by_file_id(file_id, update_payload)

#         print(f"✅ Supabase job queued: {file_id}")
#         print(f"   raw_config: {raw_config}")
#         print(f"   config: {config}")
#         print(f"   dataset_info: {dataset_info}")
#         print(f"   file_path: {file_path}")

#         return {
#             "success": True,
#             "message": "Training job queued",
#             "file_id": file_id,
#             "job_id": file_id,
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ start_training error:", e)
#         traceback.print_exc()

#         try:
#             supabase_update_by_file_id(
#                 file_id,
#                 {
#                     "status": "failed",
#                     "error_message": str(e),
#                     "completed_at": now_iso(),
#                 },
#             )
#         except Exception:
#             pass

#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # NEXT JOB FOR COLAB
# # ============================================================

# @app.get("/api/next-job")
# async def get_next_job():
#     try:
#         print("\n" + "=" * 80, flush=True)
#         print("🔍 Colab requested next job", flush=True)
#         print("SUPABASE_URL:", SUPABASE_URL, flush=True)
#         print("SERVICE ROLE EXISTS:", bool(SUPABASE_SERVICE_ROLE_KEY), flush=True)
#         print("TABLE:", SUPABASE_TABLE, flush=True)

#         url = supabase_rest_url(SUPABASE_TABLE)

#         debug_params = {
#             "select": "file_id,user_email,status,created_at,started_at,completed_at",
#             "order": "created_at.desc",
#             "limit": "10",
#         }

#         debug_response = requests.get(
#             url,
#             headers=supabase_headers(),
#             params=debug_params,
#             timeout=30,
#         )

#         print("DEBUG all jobs status:", debug_response.status_code, flush=True)
#         print("DEBUG all jobs text:", debug_response.text[:2000], flush=True)

#         if debug_response.status_code >= 400:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Supabase debug error: {debug_response.status_code} - {debug_response.text}",
#             )

#         queued_params = {
#             "select": "*",
#             "status": "eq.queued",
#             "order": "created_at.asc",
#             "limit": "1",
#         }

#         response = requests.get(
#             url,
#             headers=supabase_headers(),
#             params=queued_params,
#             timeout=30,
#         )

#         print("DEBUG queued status:", response.status_code, flush=True)
#         print("DEBUG queued text:", response.text[:2000], flush=True)

#         if response.status_code >= 400:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Supabase queued error: {response.status_code} - {response.text}",
#             )

#         jobs = response.json()

#         if not jobs:
#             print("ℹ️ Aucun job queued trouvé par le backend", flush=True)
#             print("=" * 80 + "\n", flush=True)

#             return {
#                 "status": "no_job",
#                 "message": "Aucun job en attente",
#             }

#         job = jobs[0]
#         file_id = job.get("file_id")

#         if not file_id:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Job queued trouvé mais file_id est vide.",
#             )

#         print(f"✅ Job selected for Colab: {file_id}", flush=True)

#         raw_config = job.get("config")
#         normalized_config = normalize_training_config(raw_config)
#         manual_overrides = normalized_config["manual_overrides"]

#         print(
#             "Raw config from Supabase:",
#             json.dumps(raw_config or {}, ensure_ascii=False, default=str),
#             flush=True,
#         )
#         print(
#             "Normalized config sent to Colab:",
#             json.dumps(normalized_config, ensure_ascii=False, default=str),
#             flush=True,
#         )
#         print(f"rnn_epochs: {manual_overrides.get('rnn_epochs')}", flush=True)
#         print(f"qrnn_epochs: {manual_overrides.get('qrnn_epochs')}", flush=True)

#         update_response = requests.patch(
#             url,
#             headers=supabase_headers(prefer="return=representation"),
#             params={
#                 "file_id": f"eq.{file_id}",
#                 "status": "eq.queued",
#             },
#             json={
#                 "status": "processing",
#                 "config": normalized_config,
#                 "started_at": now_iso(),
#                 "updated_at": now_iso(),
#             },
#             timeout=30,
#         )

#         print("DEBUG update processing status:", update_response.status_code, flush=True)
#         print("DEBUG update processing text:", update_response.text[:1000], flush=True)

#         if update_response.status_code >= 400:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Supabase update error: {update_response.status_code} - {update_response.text}",
#             )

#         if not update_response.json():
#             print("ℹ️ Job déjà pris par un autre worker", flush=True)
#             print("=" * 80 + "\n", flush=True)
#             return {
#                 "status": "no_job",
#                 "message": "Aucun job en attente",
#             }

#         print(f"✅ Sending file_id to Colab: {file_id}", flush=True)
#         print("=" * 80 + "\n", flush=True)

#         return {
#             "file_id": file_id,
#             "job_id": file_id,
#             "config": normalized_config,
#             "dataset_info": job.get("dataset_info") or {},
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ /api/next-job error:", e, flush=True)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # DATASET FOR COLAB
# # ============================================================

# @app.get("/api/dataset/{file_id}")
# async def download_dataset(file_id: str):
#     try:
#         print(f"📥 Dataset requested for file_id: {file_id}")

#         job = supabase_select_one_by_file_id(file_id)

#         if not job:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Job non trouvé dans Supabase",
#             )

#         file_path = job.get("file_path")

#         if not file_path:
#             matches = list(UPLOAD_DIR.glob(f"{file_id}_*.csv"))
#             if matches:
#                 file_path = str(matches[0])

#         if not file_path:
#             raise HTTPException(
#                 status_code=404,
#                 detail=(
#                     "file_path manquant dans training_jobs et fichier introuvable dans uploads."
#                 ),
#             )

#         path = Path(file_path)

#         if not path.exists():
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Fichier dataset introuvable: {path}",
#             )

#         filename = job.get("filename") or path.name

#         return FileResponse(
#             path,
#             media_type="text/csv",
#             filename=filename,
#         )

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ download_dataset error:", e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # METRICS / REPORT HELPERS
# # ============================================================

# def extract_accuracy(results: dict):
#     try:
#         if results.get("comparison", {}).get("qrnn_accuracy") is not None:
#             return results["comparison"]["qrnn_accuracy"]

#         if results.get("comparison", {}).get("rnn_accuracy") is not None:
#             return results["comparison"]["rnn_accuracy"]

#         if results.get("rnn", {}).get("accuracy") is not None:
#             return results["rnn"]["accuracy"]

#         qrnn = results.get("qrnn") or {}

#         for key in ["clean", "noisy", "mitigated"]:
#             if isinstance(qrnn.get(key), dict) and qrnn[key].get("accuracy") is not None:
#                 return qrnn[key]["accuracy"]

#     except Exception:
#         pass

#     return "N/A"


# def extract_model_name(results: dict):
#     try:
#         if results.get("comparison", {}).get("better_model"):
#             return str(results["comparison"]["better_model"]).upper()

#         if "rnn" in results and "qrnn" in results:
#             return "RNN / QNN"

#         if "rnn" in results:
#             return "RNN / MLP"

#         if "qrnn" in results:
#             return "QNN"

#     except Exception:
#         pass

#     return "Training Model"


# def generate_pdf_report(file_id: str, results: dict, output_path: Path):
#     try:
#         from reportlab.lib import colors
#         from reportlab.lib.pagesizes import A4
#         from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
#         from reportlab.lib.units import inch
#         from reportlab.platypus import (
#             Image,
#             PageBreak,
#             Paragraph,
#             SimpleDocTemplate,
#             Spacer,
#             Table,
#             TableStyle,
#         )
#     except Exception as e:
#         raise RuntimeError("reportlab manquant. Installe: pip install reportlab") from e

#     output_path.parent.mkdir(parents=True, exist_ok=True)

#     dark = colors.HexColor("#101828")
#     muted = colors.HexColor("#667085")
#     panel = colors.HexColor("#F8FAFC")
#     border = colors.HexColor("#D0D5DD")

#     styles = getSampleStyleSheet()
#     styles.add(
#         ParagraphStyle(
#             name="ReportTitle",
#             parent=styles["Title"],
#             fontName="Helvetica-Bold",
#             fontSize=24,
#             leading=28,
#             textColor=dark,
#             spaceAfter=4,
#         )
#     )
#     styles.add(
#         ParagraphStyle(
#             name="SectionTitle",
#             parent=styles["Heading2"],
#             fontName="Helvetica-Bold",
#             fontSize=13,
#             leading=16,
#             textColor=dark,
#             spaceBefore=14,
#             spaceAfter=7,
#         )
#     )
#     styles.add(
#         ParagraphStyle(
#             name="SmallMuted",
#             parent=styles["BodyText"],
#             fontSize=8,
#             leading=10,
#             textColor=muted,
#         )
#     )

#     def fmt_percent(value):
#         return f"{value * 100:.2f}%" if isinstance(value, (int, float)) else "-"

#     def fmt_number(value):
#         if isinstance(value, bool):
#             return str(value)
#         if isinstance(value, int):
#             return str(value)
#         if isinstance(value, float):
#             return f"{value:.4f}"
#         return "-"

#     def fmt_value(key, value):
#         if value is None:
#             return "-"
#         if key in {
#             "accuracy",
#             "precision",
#             "recall",
#             "f1_score",
#             "f1-score",
#             "train_accuracy",
#             "val_accuracy",
#             "rnn_accuracy",
#             "qrnn_accuracy",
#             "improvement",
#         }:
#             return fmt_percent(value)
#         if isinstance(value, list):
#             return ", ".join(str(item) for item in value)
#         if isinstance(value, dict):
#             return json.dumps(value, ensure_ascii=False)
#         if isinstance(value, float):
#             return f"{value:.4f}"
#         return str(value)

#     def make_table(data, col_widths=None, header=True, font_size=8):
#         table = Table(data, colWidths=col_widths, repeatRows=1 if header else 0, hAlign="LEFT")
#         style = [
#             ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
#             ("FONTSIZE", (0, 0), (-1, -1), font_size),
#             ("LEADING", (0, 0), (-1, -1), font_size + 2),
#             ("GRID", (0, 0), (-1, -1), 0.35, border),
#             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#             ("LEFTPADDING", (0, 0), (-1, -1), 6),
#             ("RIGHTPADDING", (0, 0), (-1, -1), 6),
#             ("TOPPADDING", (0, 0), (-1, -1), 5),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
#         ]
#         if header:
#             style.extend(
#                 [
#                     ("BACKGROUND", (0, 0), (-1, 0), dark),
#                     ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#                     ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#                 ]
#             )
#         for row_index in range(1 if header else 0, len(data)):
#             if row_index % 2 == 0:
#                 style.append(("BACKGROUND", (0, row_index), (-1, row_index), panel))
#         table.setStyle(TableStyle(style))
#         return table

#     def section(title):
#         return Paragraph(title, styles["SectionTitle"])

#     def flatten_config(prefix, value, rows):
#         if isinstance(value, dict):
#             for nested_key, nested_value in value.items():
#                 flatten_config(f"{prefix}.{nested_key}" if prefix else nested_key, nested_value, rows)
#             return
#         rows.append([prefix, fmt_value(prefix, value)])

#     def model_blocks():
#         blocks = []
#         if isinstance(results.get("rnn"), dict):
#             blocks.append(("Classical RNN", results["rnn"]))

#         qrnn = results.get("qrnn")
#         if isinstance(qrnn, dict):
#             added_variant = False
#             variant_titles = {
#                 "clean": "QNN Clean",
#                 "noisy": "QNN Noisy",
#                 "mitigated": "QNN Mitigated",
#             }
#             for variant, title in variant_titles.items():
#                 if isinstance(qrnn.get(variant), dict):
#                     blocks.append((title, qrnn[variant]))
#                     added_variant = True
#             if not added_variant and "accuracy" in qrnn:
#                 blocks.append(("QNN", qrnn))
#         return blocks

#     def metric_rows(block):
#         rows = [["Metric", "Value"]]
#         metric_keys = [
#             "accuracy",
#             "precision",
#             "recall",
#             "f1_score",
#             "loss",
#             "train_loss",
#             "val_loss",
#             "train_accuracy",
#             "val_accuracy",
#             "train_size",
#             "val_size",
#             "test_size",
#         ]
#         for key in metric_keys:
#             if key in block:
#                 rows.append([key.replace("_", " ").title(), fmt_value(key, block.get(key))])
#             if key == "loss":
#                 training_time = get_training_time_formatted(block)
#                 if training_time != "-":
#                     rows.append(["Training Time", training_time])
#         return rows

#     def confusion_matrix_table(block):
#         matrix = block.get("confusion_matrix")
#         if not isinstance(matrix, list) or not matrix:
#             return None
#         max_columns = max((len(row) for row in matrix if isinstance(row, list)), default=0)
#         if max_columns == 0:
#             return None
#         class_names = block.get("class_names") if isinstance(block.get("class_names"), list) else None
#         labels = [str(item) for item in class_names] if class_names else [str(i) for i in range(max(len(matrix), max_columns))]
#         data = [["Actual / Predicted", *[f"Class {label}" for label in labels[:max_columns]]]]
#         for index, row in enumerate(matrix):
#             if isinstance(row, list):
#                 padded = [*row, *[""] * (max_columns - len(row))]
#                 label = labels[index] if index < len(labels) else str(index)
#                 data.append([f"Class {label}", *padded])
#         first_width = 1.25 * inch
#         value_width = min(0.8 * inch, max(0.42 * inch, (6.5 * inch - first_width) / max_columns))
#         return make_table(
#             data,
#             [first_width, *([value_width] * max_columns)],
#             header=True,
#             font_size=7 if max_columns > 4 else 8,
#         )

#     def classification_report_table(block):
#         report = block.get("classification_report")
#         if not isinstance(report, dict):
#             return None
#         rows = [["Class", "Precision", "Recall", "F1 Score", "Support"]]

#         def is_report_row(item):
#             _, metrics = item
#             return isinstance(metrics, dict) and any(
#                 key in metrics for key in ["precision", "recall", "f1-score", "support"]
#             )

#         def sort_key(item):
#             label, _ = item
#             if label == "macro avg":
#                 return (1, 0, label)
#             if label == "weighted avg":
#                 return (1, 1, label)
#             try:
#                 return (0, int(label), label)
#             except (TypeError, ValueError):
#                 return (0, 999999, str(label))

#         for label, metrics in sorted([item for item in report.items() if is_report_row(item)], key=sort_key):
#             rows.append(
#                 [
#                     str(label),
#                     fmt_percent(metrics.get("precision")),
#                     fmt_percent(metrics.get("recall")),
#                     fmt_percent(metrics.get("f1-score")),
#                     fmt_number(metrics.get("support")),
#                 ]
#             )
#         if isinstance(report.get("accuracy"), (int, float)):
#             rows.append(["Accuracy", "", "", fmt_percent(report["accuracy"]), ""])
#         return make_table(rows, [0.9 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 0.9 * inch], font_size=7)

#     def history_rows(block):
#         history = block.get("history")
#         if not isinstance(history, dict):
#             return []
#         max_len = max((len(values) for values in history.values() if isinstance(values, list)), default=0)
#         if max_len == 0:
#             return []
#         train_loss = history.get("train_loss") or history.get("loss") or []
#         val_loss = history.get("val_loss") or []
#         train_acc = history.get("train_acc") or history.get("train_accuracy") or history.get("accuracy") or []
#         val_acc = history.get("val_acc") or history.get("val_accuracy") or []
#         rows = [["Epoch", "Train Loss", "Val Loss", "Train Acc", "Val Acc"]]
#         for index in range(max_len):
#             rows.append(
#                 [
#                     str(index + 1),
#                     fmt_number(train_loss[index] if index < len(train_loss) else None),
#                     fmt_number(val_loss[index] if index < len(val_loss) else None),
#                     fmt_percent(train_acc[index] if index < len(train_acc) else None),
#                     fmt_percent(val_acc[index] if index < len(val_acc) else None),
#                 ]
#             )
#         return rows

#     def make_curve_image(blocks, metric):
#         try:
#             import matplotlib

#             matplotlib.use("Agg")
#             import matplotlib.pyplot as plt
#         except Exception:
#             return None

#         fig, ax = plt.subplots(figsize=(4.9, 2.2), dpi=150)
#         plotted = False
#         palette = ["#7C3AED", "#06B6D4", "#14B8A6", "#F97316"]
#         for index, (title, block) in enumerate(blocks):
#             history = block.get("history")
#             if not isinstance(history, dict):
#                 continue
#             if metric == "accuracy":
#                 series = history.get("val_acc") or history.get("val_accuracy") or history.get("accuracy") or history.get("train_acc")
#                 ylabel = "Accuracy"
#             else:
#                 series = history.get("val_loss") or history.get("loss") or history.get("train_loss")
#                 ylabel = "Loss"
#             if isinstance(series, list) and series:
#                 ax.plot(
#                     range(1, len(series) + 1),
#                     series,
#                     marker="o",
#                     markersize=2,
#                     linewidth=1.6,
#                     label=title,
#                     color=palette[index % len(palette)],
#                 )
#                 plotted = True
#         if not plotted:
#             plt.close(fig)
#             return None
#         ax.set_title(f"{ylabel} Curves", fontsize=8)
#         ax.set_xlabel("Epoch", fontsize=7)
#         ax.set_ylabel(ylabel, fontsize=7)
#         ax.grid(True, alpha=0.25)
#         ax.legend(fontsize=5)
#         ax.tick_params(labelsize=6)
#         fig.tight_layout()
#         image_path = output_path.parent / f"{file_id}_{metric}_curve.png"
#         fig.savefig(image_path, bbox_inches="tight")
#         plt.close(fig)
#         return image_path

#     def page_canvas(canvas_obj, doc):
#         canvas_obj.saveState()
#         canvas_obj.setFillColor(dark)
#         canvas_obj.rect(0, A4[1] - 36, A4[0], 36, stroke=0, fill=1)
#         canvas_obj.setFillColor(colors.white)
#         canvas_obj.setFont("Helvetica-Bold", 8)
#         canvas_obj.drawString(36, A4[1] - 22, "NeuroSpace Evaluation Report")
#         canvas_obj.setFillColor(muted)
#         canvas_obj.setFont("Helvetica", 7)
#         canvas_obj.drawRightString(A4[0] - 36, 22, f"Page {doc.page}")
#         canvas_obj.restoreState()

#     story = []
#     logo_candidates = [
#         BASE_DIR.parent / "frontend" / "public" / "assets" / "images" / "app_logo1.png",
#         BASE_DIR.parent / "frontend" / "public" / "app_logo1.png",
#     ]
#     logo_path = next((path for path in logo_candidates if path.exists()), None)
#     logo = Image(str(logo_path), width=0.65 * inch, height=0.65 * inch) if logo_path else Paragraph("NS", styles["ReportTitle"])

#     header = Table(
#         [
#             [
#                 logo,
#                 [
#                     Paragraph("NeuroSpace", styles["ReportTitle"]),
#                     Paragraph("Complete evaluation export", styles["SmallMuted"]),
#                 ],
#             ]
#         ],
#         colWidths=[1.0 * inch, 5.5 * inch],
#     )
#     header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
#     story.append(Spacer(1, 0.42 * inch))
#     story.append(header)
#     story.append(Spacer(1, 0.18 * inch))
#     story.append(
#         make_table(
#             [
#                 ["Job ID", file_id],
#                 ["Status", str(results.get("status", "completed"))],
#                 ["Result timestamp", str(results.get("timestamp") or "-")],
#                 ["PDF generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             ],
#             [1.35 * inch, 5.15 * inch],
#             header=False,
#             font_size=8,
#         )
#     )

#     config_rows = [["Parameter", "Value"]]
#     flatten_config("", results.get("config_used") or {}, config_rows)
#     if len(config_rows) > 1:
#         story.append(section("Pipeline Configuration"))
#         story.append(make_table(config_rows, [2.2 * inch, 4.3 * inch]))

#     comparison = results.get("comparison")
#     if isinstance(comparison, dict):
#         story.append(section("Best Model"))
#         story.append(
#             make_table(
#                 [
#                     ["Winner", "RNN Accuracy", "QNN Accuracy", "Improvement"],
#                     [
#                         str(comparison.get("better_model", "-")).upper(),
#                         fmt_percent(comparison.get("rnn_accuracy")),
#                         fmt_percent(comparison.get("qrnn_accuracy")),
#                         fmt_percent(comparison.get("improvement")),
#                     ],
#                 ],
#                 [1.4 * inch, 1.55 * inch, 1.55 * inch, 1.55 * inch],
#             )
#         )

#     blocks = model_blocks()
#     if blocks:
#         story.append(section("Evaluation Summary"))
#         summary_rows = [["Model", "Accuracy", "Precision", "Recall", "F1 Score", "Loss", "Training Time"]]
#         for title, block in blocks:
#             summary_rows.append(
#                 [
#                     title,
#                     fmt_percent(block.get("accuracy")),
#                     fmt_percent(block.get("precision")),
#                     fmt_percent(block.get("recall")),
#                     fmt_percent(block.get("f1_score")),
#                     fmt_number(block.get("loss")),
#                     get_training_time_formatted(block),
#                 ]
#             )
#         story.append(
#             make_table(
#                 summary_rows,
#                 [
#                     1.35 * inch,
#                     0.85 * inch,
#                     0.85 * inch,
#                     0.85 * inch,
#                     0.9 * inch,
#                     0.7 * inch,
#                     1.0 * inch,
#                 ],
#             )
#         )

#     accuracy_curve = make_curve_image(blocks, "accuracy")
#     loss_curve = make_curve_image(blocks, "loss")
#     if accuracy_curve or loss_curve:
#         story.append(section("Learning Curves"))
#         story.append(PageBreak())
#         curve_cells = []
#         if accuracy_curve:
#             curve_cells.append(Image(str(accuracy_curve), width=3.1 * inch, height=1.55 * inch))
#         if loss_curve:
#             curve_cells.append(Image(str(loss_curve), width=3.1 * inch, height=1.55 * inch))
#         story.append(Spacer(1, 0.45 * inch))
#         story.append(Table([curve_cells], colWidths=[3.2 * inch] * len(curve_cells), hAlign="CENTER"))

#     for title, block in blocks:
#         story.append(PageBreak())
#         story.append(section(title))
#         story.append(make_table(metric_rows(block), [2.0 * inch, 4.0 * inch], font_size=8))

#         cm_table = confusion_matrix_table(block)
#         if cm_table:
#             story.append(section(f"{title} Confusion Matrix"))
#             story.append(cm_table)

#         report_table = classification_report_table(block)
#         if report_table:
#             story.append(section(f"{title} Classification Report"))
#             story.append(report_table)

#         rows = history_rows(block)
#         if rows:
#             story.append(section(f"{title} Epoch History"))
#             story.append(make_table(rows, [0.65 * inch, 1.15 * inch, 1.15 * inch, 1.15 * inch, 1.15 * inch], font_size=7))

#     doc = SimpleDocTemplate(
#         str(output_path),
#         pagesize=A4,
#         rightMargin=36,
#         leftMargin=36,
#         topMargin=54,
#         bottomMargin=36,
#         title=f"NeuroSpace Evaluation Report - {file_id}",
#     )
#     doc.build(story, onFirstPage=page_canvas, onLaterPages=page_canvas)


# def send_report_email(
#     to_email: str,
#     to_name: str | None,
#     file_id: str,
#     pdf_path: Path,
#     json_path: Path | None,
#     results: dict,
# ):
#     if not to_email:
#         return {
#             "success": False,
#             "error": "Recipient email missing",
#         }

#     if not EMAIL_FROM or not BREVO_SMTP_USER or not BREVO_SMTP_PASSWORD:
#         return {
#             "success": False,
#             "error": "Brevo SMTP env missing. Email skipped.",
#         }

#     if not pdf_path.exists():
#         return {
#             "success": False,
#             "error": f"PDF not found: {pdf_path}",
#         }

#     try:
#         subject = "Your NeuroSpace Training Report is Ready"
#         created_at = results.get("timestamp") or now_iso()

#         body = f"""Hello {to_name or "User"},

# Your training and classification process has been completed successfully.

# The generated PDF report is now ready and contains the full classification results.

# Summary:
# - Generated at: {created_at}

# Thank you for using NeuroSpace.

# Best regards,
# NeuroSpace Team
# """

#         msg = EmailMessage()
#         msg["From"] = EMAIL_FROM
#         msg["To"] = to_email
#         msg["Subject"] = subject
#         msg.set_content(body)

#         with open(pdf_path, "rb") as f:
#             msg.add_attachment(
#                 f.read(),
#                 maintype="application",
#                 subtype="pdf",
#                 filename=f"neurospace-report-{file_id}.pdf",
#             )

#         if json_path and json_path.exists():
#             with open(json_path, "rb") as f:
#                 msg.add_attachment(
#                     f.read(),
#                     maintype="application",
#                     subtype="json",
#                     filename=f"results-{file_id}.json",
#                 )

#         with smtplib.SMTP(BREVO_SMTP_HOST, BREVO_SMTP_PORT) as smtp:
#             smtp.starttls()
#             smtp.login(BREVO_SMTP_USER, BREVO_SMTP_PASSWORD)
#             smtp.send_message(msg)

#         print(f"📧 Email sent to {to_email}")

#         return {
#             "success": True,
#             "error": None,
#         }

#     except Exception as e:
#         print("❌ Brevo email error:", e)
#         traceback.print_exc()

#         return {
#             "success": False,
#             "error": str(e),
#         }


# # ============================================================
# # COMPLETE JOB FROM COLAB
# # ============================================================

# @app.post("/api/job/{file_id}/complete")
# async def complete_job(file_id: str, request: Request):
#     try:
#         print(f"✅ Complete job received for file_id: {file_id}")

#         results = await request.json()
#         results = make_json_serializable(results)
#         results = ensure_training_times(results)

#         job = supabase_select_one_by_file_id(file_id)

#         if not job:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Job non trouvé dans Supabase",
#             )

#         user_email = job.get("user_email")
#         user_name = job.get("user_name")

#         if not user_email:
#             raise HTTPException(
#                 status_code=400,
#                 detail="user_email manquant dans training_jobs",
#             )

#         result_dir = RESULTS_DIR / file_id
#         result_dir.mkdir(parents=True, exist_ok=True)

#         json_path = result_dir / "results.json"
#         pdf_path = result_dir / "report.pdf"

#         with open(json_path, "w", encoding="utf-8") as f:
#             json.dump(results, f, indent=2, ensure_ascii=False)

#         print(f"💾 Results JSON saved: {json_path}")

#         generate_pdf_report(file_id, results, pdf_path)

#         print(f"📄 PDF generated: {pdf_path}")

#         supabase_update_by_file_id(
#             file_id,
#             {
#                 "status": "completed",
#                 "results": results,
#                 "json_path": str(json_path),
#                 "pdf_path": str(pdf_path),
#                 "completed_at": now_iso(),
#             },
#         )

#         print("📧 Brevo email sending started")

#         email_result = send_report_email(
#             to_email=user_email,
#             to_name=user_name,
#             file_id=file_id,
#             pdf_path=pdf_path,
#             json_path=json_path,
#             results=results,
#         )

#         supabase_update_by_file_id(
#             file_id,
#             {
#                 "email_sent": bool(email_result.get("success")),
#                 "email_sent_to": user_email,
#                 "email_sent_at": now_iso() if email_result.get("success") else None,
#                 "email_error": None if email_result.get("success") else email_result.get("error"),
#             },
#         )

#         if email_result.get("success"):
#             print("✅ Brevo email sent successfully")
#         else:
#             print(f"⚠️ Brevo email failed/skipped: {email_result.get('error')}")

#         return {
#             "success": True,
#             "file_id": file_id,
#             "message": "Job completed",
#             "email_sent": bool(email_result.get("success")),
#             "email_error": None if email_result.get("success") else email_result.get("error"),
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ complete_job error:", e)
#         traceback.print_exc()

#         try:
#             supabase_update_by_file_id(
#                 file_id,
#                 {
#                     "status": "failed",
#                     "error_message": str(e),
#                     "completed_at": now_iso(),
#                 },
#             )
#         except Exception:
#             pass

#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # FAIL / FAILED JOB
# # ============================================================

# async def mark_job_failed(file_id: str, payload: dict):
#     error_message = (
#         payload.get("error")
#         or payload.get("message")
#         or payload.get("detail")
#         or "Erreur inconnue"
#     )

#     print(f"❌ Job failed: {file_id} - {error_message}")

#     job = supabase_select_one_by_file_id(file_id)

#     if not job:
#         raise HTTPException(
#             status_code=404,
#             detail="Job non trouvé dans Supabase",
#         )

#     supabase_update_by_file_id(
#         file_id,
#         {
#             "status": "failed",
#             "error_message": str(error_message),
#             "completed_at": now_iso(),
#         },
#     )

#     return {
#         "success": True,
#         "message": "Job marked as failed",
#         "file_id": file_id,
#     }


# @app.post("/api/job/{file_id}/failed")
# async def failed_job(file_id: str, request: Request):
#     payload = await request.json()
#     return await mark_job_failed(file_id, payload)


# @app.post("/api/job/{file_id}/fail")
# async def fail_job(file_id: str, request: Request):
#     payload = await request.json()
#     return await mark_job_failed(file_id, payload)


# # ============================================================
# # STATUS + RESULTS
# # ============================================================

# @app.get("/api/job/{file_id}/status")
# async def get_job_status(file_id: str):
#     try:
#         job = supabase_select_one_by_file_id(file_id)

#         if not job:
#             raise HTTPException(status_code=404, detail="Job non trouvé")

#         return {
#             "job_id": file_id,
#             "file_id": file_id,
#             "status": job.get("status"),
#             "message": job.get("error_message") if job.get("status") == "failed" else None,
#             "error": job.get("error_message"),
#             "email_sent": job.get("email_sent"),
#             "email_error": job.get("email_error"),
#             "created_at": job.get("created_at"),
#             "started_at": job.get("started_at"),
#             "completed_at": job.get("completed_at"),
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ get_job_status error:", e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/results/{file_id}")
# async def get_results(file_id: str):
#     try:
#         job = supabase_select_one_by_file_id(file_id)

#         if not job:
#             raise HTTPException(status_code=404, detail="Job non trouvé")

#         if job.get("status") != "completed":
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Résultats pas encore prêts: {job.get('status')}",
#             )

#         results = job.get("results")

#         if results:
#             return results

#         json_path = job.get("json_path")

#         if json_path and Path(json_path).exists():
#             with open(json_path, "r", encoding="utf-8") as f:
#                 return json.load(f)

#         raise HTTPException(status_code=404, detail="Résultats introuvables")

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ get_results error:", e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/report/{file_id}/pdf")
# @app.get("/api/report/{file_id}/download")
# async def download_report(file_id: str):
#     try:
#         job = supabase_select_one_by_file_id(file_id)

#         if not job:
#             raise HTTPException(status_code=404, detail="Job non trouvé")

#         pdf_path = job.get("pdf_path") or str(RESULTS_DIR / file_id / "report.pdf")
#         path = Path(pdf_path)

#         if not path.exists():
#             raise HTTPException(status_code=404, detail="PDF introuvable")

#         return FileResponse(
#             path,
#             media_type="application/pdf",
#             filename=f"neurospace-report-{file_id}.pdf",
#         )

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ download_report error:", e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # DEBUG
# # ============================================================

# @app.get("/api/debug/jobs")
# async def debug_jobs():
#     try:
#         url = supabase_rest_url(SUPABASE_TABLE)

#         params = {
#             "select": "file_id,user_email,status,created_at,started_at,completed_at,file_path,filename",
#             "order": "created_at.desc",
#             "limit": "10",
#         }

#         response = requests.get(
#             url,
#             headers=supabase_headers(),
#             params=params,
#             timeout=30,
#         )

#         if response.status_code >= 400:
#             raise HTTPException(status_code=500, detail=response.text)

#         return {
#             "success": True,
#             "supabase_url": SUPABASE_URL,
#             "service_role_exists": bool(SUPABASE_SERVICE_ROLE_KEY),
#             "jobs": response.json(),
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ debug_jobs error:", e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# # ============================================================
# # MAIN
# # ============================================================

# if __name__ == "__main__":
#     import uvicorn

#     print("==============================================")
#     print("🚀 NeuroSpace Backend starting")
#     print("ENV_PATH:", ENV_PATH)
#     print("ENV_PATH exists:", ENV_PATH.exists())
#     print("SUPABASE_URL exists:", bool(SUPABASE_URL))
#     print("SUPABASE_SERVICE_ROLE_KEY exists:", bool(SUPABASE_SERVICE_ROLE_KEY))
#     print("BREVO_SMTP_USER exists:", bool(BREVO_SMTP_USER))
#     print("BREVO_SMTP_PASSWORD exists:", bool(BREVO_SMTP_PASSWORD))
#     print("EMAIL_FROM exists:", bool(EMAIL_FROM))
#     print("UPLOAD_DIR:", UPLOAD_DIR)
#     print("RESULTS_DIR:", RESULTS_DIR)
#     print("==============================================")

#     uvicorn.run(app, host="0.0.0.0", port=7000)

import os
import json
import uuid
import shutil
import smtplib
import sys
import traceback
from pathlib import Path
from datetime import datetime, timezone
from email.message import EmailMessage

import requests
import pandas as pd
import numpy as np

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ============================================================
# LOAD .ENV FROM BACKEND FOLDER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

try:
    from dotenv import load_dotenv

    load_dotenv(ENV_PATH)
    print("✅ .env loaded from:", ENV_PATH)
except Exception as e:
    print("⚠️ dotenv not loaded:", e)


# ============================================================
# CONFIG
# ============================================================

UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SUPABASE_URL = (
    os.getenv("SUPABASE_URL")
    or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
)

SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

SUPABASE_TABLE = "training_jobs"
SUPABASE_REPORTS_BUCKET = os.getenv("SUPABASE_REPORTS_BUCKET", "reports")

BREVO_SMTP_HOST = os.getenv("BREVO_SMTP_HOST", "smtp-relay.brevo.com")
BREVO_SMTP_PORT = int(os.getenv("BREVO_SMTP_PORT", "587"))
BREVO_SMTP_USER = os.getenv("BREVO_SMTP_USER")
BREVO_SMTP_PASSWORD = os.getenv("BREVO_SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
APP_URL = os.getenv("NEXT_PUBLIC_APP_URL") or os.getenv("APP_URL") or "http://localhost:3000"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def require_supabase_env():
    if not SUPABASE_URL:
        raise RuntimeError(
            "SUPABASE_URL manquant. Mets SUPABASE_URL dans backend/.env"
        )

    if not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY manquant. Mets SUPABASE_SERVICE_ROLE_KEY dans backend/.env"
        )


def supabase_headers(prefer: str | None = None):
    require_supabase_env()

    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }

    if prefer:
        headers["Prefer"] = prefer

    return headers


def supabase_rest_url(table: str):
    require_supabase_env()
    return f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table}"


def supabase_select_one_by_file_id(file_id: str):
    url = supabase_rest_url(SUPABASE_TABLE)

    params = {
        "file_id": f"eq.{file_id}",
        "select": "*",
        "limit": "1",
    }

    response = requests.get(
        url,
        headers=supabase_headers(),
        params=params,
        timeout=30,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Supabase select error: {response.status_code} - {response.text}"
        )

    rows = response.json()

    if not rows:
        return None

    return rows[0]


def supabase_update_by_file_id(file_id: str, data: dict):
    url = supabase_rest_url(SUPABASE_TABLE)

    params = {
        "file_id": f"eq.{file_id}",
    }

    payload = {
        **data,
        "updated_at": now_iso(),
    }

    response = requests.patch(
        url,
        headers=supabase_headers(prefer="return=representation"),
        params=params,
        json=payload,
        timeout=30,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Supabase update error: {response.status_code} - {response.text}"
        )

    return response.json()




def supabase_storage_upload_file(local_path: Path, storage_path: str, content_type: str):
    require_supabase_env()

    if not local_path.exists():
        raise RuntimeError(f"Fichier introuvable pour upload Supabase Storage: {local_path}")

    url = (
        f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/"
        f"{SUPABASE_REPORTS_BUCKET}/{storage_path}"
    )

    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": content_type,
        "x-upsert": "true",
    }

    with open(local_path, "rb") as f:
        response = requests.post(
            url,
            headers=headers,
            data=f.read(),
            timeout=60,
        )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Supabase Storage upload error: {response.status_code} - {response.text}"
        )

    return f"{SUPABASE_REPORTS_BUCKET}/{storage_path}"


def supabase_storage_upload_pdf(file_id: str, pdf_path: Path):
    storage_path = f"{file_id}/report.pdf"
    return supabase_storage_upload_file(
        local_path=pdf_path,
        storage_path=storage_path,
        content_type="application/pdf",
    )


def supabase_storage_upload_json(file_id: str, json_path: Path):
    storage_path = f"{file_id}/results.json"
    return supabase_storage_upload_file(
        local_path=json_path,
        storage_path=storage_path,
        content_type="application/json",
    )


def supabase_storage_download_file(storage_key: str):
    require_supabase_env()

    if not storage_key or "/" not in storage_key:
        raise RuntimeError(f"storage_key invalide: {storage_key}")

    bucket, object_path = storage_key.split("/", 1)

    url = (
        f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/"
        f"{bucket}/{object_path}"
    )

    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Supabase Storage download error: {response.status_code} - {response.text}"
        )

    return response.content


def is_supabase_storage_key(value: str | None):
    if not isinstance(value, str) or not value.strip():
        return False

    return value.startswith(f"{SUPABASE_REPORTS_BUCKET}/")


def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {str(k): make_json_serializable(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]

    if isinstance(obj, tuple):
        return [make_json_serializable(v) for v in obj]

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating,)):
        return float(obj)

    if isinstance(obj, (np.bool_)):
        return bool(obj)

    return obj


def format_training_time_seconds(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        return None

    if value < 60:
        return f"{value:.2f}s"

    total_seconds = float(value)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60

    if hours:
        return f"{hours}h {minutes}m {seconds:.2f}s"
    return f"{minutes}m {seconds:.2f}s"


def get_training_time_formatted(block):
    if not isinstance(block, dict):
        return "-"

    formatted = block.get("training_time_formatted")
    if isinstance(formatted, str) and formatted.strip():
        return formatted

    formatted = format_training_time_seconds(block.get("training_time_seconds"))
    return formatted or "-"


def ensure_training_times(results):
    if not isinstance(results, dict):
        return results

    def normalize_block(block):
        if not isinstance(block, dict):
            return
        if isinstance(block.get("training_time_formatted"), str) and block["training_time_formatted"].strip():
            return
        formatted = format_training_time_seconds(block.get("training_time_seconds"))
        if formatted:
            block["training_time_formatted"] = formatted

    def training_time_payload(block):
        if not isinstance(block, dict):
            return None

        seconds = block.get("training_time_seconds")
        formatted = get_training_time_formatted(block)

        if formatted == "-" and not isinstance(seconds, (int, float)):
            return None

        payload = {"training_time_formatted": formatted}
        if isinstance(seconds, (int, float)) and not isinstance(seconds, bool):
            payload["training_time_seconds"] = seconds
        return payload

    normalize_block(results.get("rnn"))

    qrnn = results.get("qrnn")
    if isinstance(qrnn, dict):
        has_variant = False
        for variant in ["clean", "noisy", "mitigated"]:
            if isinstance(qrnn.get(variant), dict):
                normalize_block(qrnn[variant])
                has_variant = True
        if not has_variant:
            normalize_block(qrnn)

    training_times = {}
    rnn_time = training_time_payload(results.get("rnn"))
    if rnn_time:
        training_times["rnn"] = rnn_time

    qrnn_main_time = None
    if isinstance(qrnn, dict):
        for variant in ["clean", "noisy", "mitigated"]:
            variant_time = training_time_payload(qrnn.get(variant))
            if variant_time:
                training_times[f"qrnn_{variant}"] = variant_time
                if variant in ["mitigated", "noisy", "clean"]:
                    qrnn_main_time = variant_time
        if not training_times.get("qrnn_clean") and not training_times.get("qrnn_noisy") and not training_times.get("qrnn_mitigated"):
            qrnn_main_time = training_time_payload(qrnn)
            if qrnn_main_time:
                training_times["qrnn"] = qrnn_main_time

    if training_times:
        results["training_times"] = training_times

    comparison = results.get("comparison")
    if isinstance(comparison, dict):
        if rnn_time:
            comparison["rnn_training_time_formatted"] = rnn_time["training_time_formatted"]
            if "training_time_seconds" in rnn_time:
                comparison["rnn_training_time_seconds"] = rnn_time["training_time_seconds"]

        for key, prefix in [
            ("qrnn_clean", "qrnn_clean"),
            ("qrnn_noisy", "qrnn_noisy"),
            ("qrnn_mitigated", "qrnn_mitigated"),
        ]:
            model_time = training_times.get(key)
            if model_time:
                comparison[f"{prefix}_training_time_formatted"] = model_time["training_time_formatted"]
                if "training_time_seconds" in model_time:
                    comparison[f"{prefix}_training_time_seconds"] = model_time["training_time_seconds"]

        if qrnn_main_time:
            comparison["qrnn_training_time_formatted"] = qrnn_main_time["training_time_formatted"]
            if "training_time_seconds" in qrnn_main_time:
                comparison["qrnn_training_time_seconds"] = qrnn_main_time["training_time_seconds"]

    return results


def coerce_json_object(value):
    if isinstance(value, dict):
        return value

    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    return {}


def coerce_int(value, default):
    if isinstance(value, bool):
        return default

    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def coerce_float(value, default):
    if isinstance(value, bool):
        return default

    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def coerce_bool(value, default=False):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        lower_value = value.strip().lower()
        if lower_value in {"true", "1", "yes", "on"}:
            return True
        if lower_value in {"false", "0", "no", "off"}:
            return False

    return default


def normalize_training_config(raw_config):
    """
    Retourne toujours une config compatible worker Colab.
    Accepte les formats:
    - {user_preferences, manual_overrides}
    - config plate: {model_types, rnn_epochs, ...}
    - {config: {...}}
    - null / {}
    """
    config = coerce_json_object(raw_config)

    if isinstance(config.get("config"), dict):
        nested_config = coerce_json_object(config.get("config"))
        if "user_preferences" not in config and "manual_overrides" not in config:
            config = nested_config

    user_preferences = coerce_json_object(config.get("user_preferences"))
    manual_overrides = coerce_json_object(config.get("manual_overrides"))

    comparison_mode = (
        user_preferences.get("comparison_mode")
        or config.get("comparison_mode")
        or "pca"
    )
    feature_selector = (
        user_preferences.get("feature_selector")
        or config.get("feature_selector")
        or comparison_mode
    )
    batch_size = coerce_int(
        manual_overrides.get("batch_size", config.get("batch_size")),
        32,
    )

    normalized_user_preferences = {
        "model_types": (
            user_preferences.get("model_types")
            or config.get("model_types")
            or ["rnn", "qrnn"]
        ),
        "comparison_mode": comparison_mode,
        "feature_selector": feature_selector,
        "qrnn_backend": (
            user_preferences.get("qrnn_backend")
            or config.get("qrnn_backend")
            or "pennylane"
        ),
        "noise_enabled": coerce_bool(
            user_preferences.get("noise_enabled", config.get("noise_enabled")),
            False,
        ),
        "noise_level": coerce_float(
            user_preferences.get("noise_level", config.get("noise_level")),
            0.0,
        ),
        "mitigation_enabled": coerce_bool(
            user_preferences.get("mitigation_enabled", config.get("mitigation_enabled")),
            False,
        ),
        "mitigation_runs": coerce_int(
            user_preferences.get("mitigation_runs", config.get("mitigation_runs")),
            1,
        ),
    }

    if not isinstance(normalized_user_preferences["model_types"], list):
        normalized_user_preferences["model_types"] = ["rnn", "qrnn"]

    normalized_manual_overrides = {
        "rnn_epochs": coerce_int(
            manual_overrides.get("rnn_epochs", config.get("rnn_epochs")),
            30,
        ),
        "qrnn_epochs": coerce_int(
            manual_overrides.get("qrnn_epochs", config.get("qrnn_epochs")),
            20,
        ),
        "batch_size": batch_size,
        "rnn_batch_size": coerce_int(
            manual_overrides.get("rnn_batch_size", config.get("rnn_batch_size")),
            batch_size,
        ),
        "qrnn_batch_size": coerce_int(
            manual_overrides.get("qrnn_batch_size", config.get("qrnn_batch_size")),
            batch_size,
        ),
    }

    return {
        "user_preferences": normalized_user_preferences,
        "manual_overrides": normalized_manual_overrides,
    }


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(title="NeuroSpace Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


@app.get("/")
async def root():
    return {
        "message": "NeuroSpace Backend API",
        "status": "operational",
        "env_path": str(ENV_PATH),
        "supabase_url_exists": bool(SUPABASE_URL),
        "service_role_exists": bool(SUPABASE_SERVICE_ROLE_KEY),
        "upload_dir": str(UPLOAD_DIR),
        "results_dir": str(RESULTS_DIR),
    }


# ============================================================
# DATASET HELPERS
# ============================================================

def detect_separator(file_path: Path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        first_line = f.readline().strip()

    if ";" in first_line:
        return ";"

    return ","


def is_feature_column(column_name: str) -> bool:
    column_lower = column_name.lower().strip()

    ignore_words = [
        "id",
        "identifier",
        "index",
        "unnamed",
        "row",
        "rowid",
        "class",
        "target",
        "output",
        "label",
        "prediction",
        "result",
        "y",
        "response",
        "dependent",
        "outcome",
        "date",
        "time",
        "timestamp",
        "created_at",
        "updated_at",
    ]

    for word in ignore_words:
        if (
            word == column_lower
            or column_lower.startswith(word + "_")
            or column_lower.endswith("_" + word)
            or f"_{word}_" in column_lower
        ):
            return False

    return True


def build_dataset_info(file_path: Path):
    separator = detect_separator(file_path)
    df = pd.read_csv(file_path, sep=separator)

    if df.isnull().any().any():
        missing = df.columns[df.isnull().any()].tolist()
        raise ValueError(f"Valeurs manquantes dans: {missing}")

    all_columns = list(df.columns)

    target_col = None
    target_keywords = [
        "class",
        "target",
        "output",
        "label",
        "y",
        "result",
        "outcome",
    ]

    for col in all_columns:
        col_lower = col.lower().strip()

        for keyword in target_keywords:
            if (
                keyword == col_lower
                or col_lower.endswith("_" + keyword)
                or col_lower.startswith(keyword + "_")
            ):
                target_col = col
                break

        if target_col:
            break

    if not target_col:
        target_col = all_columns[-1]

    feature_cols = []

    for col in all_columns:
        if col == target_col:
            continue

        if is_feature_column(col):
            feature_cols.append(col)

    n_samples = int(len(df))
    n_features = int(len(feature_cols))
    n_classes = int(df[target_col].nunique())

    if n_features > 0:
        n_qubits = int(np.floor(np.log2(n_features)))
        n_qubits = max(n_qubits, 1)
    else:
        n_qubits = 1

    pca_dimension = int(2**n_qubits)

    return {
        "samples": n_samples,
        "features": n_features,
        "classes": n_classes,
        "target_column": target_col,
        "recommended_qubits": n_qubits,
        "pca_dimension": pca_dimension,
        "separator": separator,
    }


# ============================================================
# UPLOAD DATASET
# ============================================================

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="Seuls les fichiers CSV sont acceptés",
            )

        file_id = str(uuid.uuid4())
        safe_filename = f"{file_id}_{file.filename}"
        file_path = UPLOAD_DIR / safe_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        dataset_info = build_dataset_info(file_path)

        print(f"✅ Dataset uploaded: {file_id}")
        print(f"   filename: {file.filename}")
        print(f"   file_path: {file_path}")
        print(f"   dataset_info: {dataset_info}")

        return {
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "file_path": str(file_path),
            "dataset_info": dataset_info,
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ Upload error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# QUEUE TRAINING
# ============================================================

@app.post("/api/train/{file_id}")
async def start_training(file_id: str, request: Request):
    try:
        body = await request.json()

        raw_config = body.get("config") or body
        config = normalize_training_config(raw_config)
        dataset_info = body.get("dataset_info") or coerce_json_object(raw_config).get("dataset_info") or {}

        filename = body.get("filename")
        file_path = body.get("file_path")

        if not file_path:
            matches = list(UPLOAD_DIR.glob(f"{file_id}_*.csv"))
            if matches:
                file_path = str(matches[0])
                filename = filename or matches[0].name

        existing_job = supabase_select_one_by_file_id(file_id)

        if existing_job:
            file_path = file_path or existing_job.get("file_path")
            filename = filename or existing_job.get("filename")

        if not file_path:
            raise HTTPException(
                status_code=400,
                detail=(
                    "file_path introuvable. Le frontend doit envoyer file_path "
                    "ou le backend doit trouver le CSV dans backend/uploads."
                ),
            )

        if not dataset_info:
            dataset_info = build_dataset_info(Path(file_path))

        if not existing_job:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Job absent dans Supabase training_jobs. "
                    "Le frontend doit créer la ligne avec user_id/user_email avant /api/train."
                ),
            )

        update_payload = {
            "status": "queued",
            "config": config,
            "dataset_info": dataset_info,
            "file_path": file_path,
            "filename": filename,
            "started_at": None,
            "completed_at": None,
            "error_message": None,
        }

        supabase_update_by_file_id(file_id, update_payload)

        print(f"✅ Supabase job queued: {file_id}")
        print(f"   raw_config: {raw_config}")
        print(f"   config: {config}")
        print(f"   dataset_info: {dataset_info}")
        print(f"   file_path: {file_path}")

        return {
            "success": True,
            "message": "Training job queued",
            "file_id": file_id,
            "job_id": file_id,
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ start_training error:", e)
        traceback.print_exc()

        try:
            supabase_update_by_file_id(
                file_id,
                {
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": now_iso(),
                },
            )
        except Exception:
            pass

        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# NEXT JOB FOR COLAB
# ============================================================

@app.get("/api/next-job")
async def get_next_job():
    try:
        print("\n" + "=" * 80, flush=True)
        print("🔍 Colab requested next job", flush=True)
        print("SUPABASE_URL:", SUPABASE_URL, flush=True)
        print("SERVICE ROLE EXISTS:", bool(SUPABASE_SERVICE_ROLE_KEY), flush=True)
        print("TABLE:", SUPABASE_TABLE, flush=True)

        url = supabase_rest_url(SUPABASE_TABLE)

        debug_params = {
            "select": "file_id,user_email,status,created_at,started_at,completed_at",
            "order": "created_at.desc",
            "limit": "10",
        }

        debug_response = requests.get(
            url,
            headers=supabase_headers(),
            params=debug_params,
            timeout=30,
        )

        print("DEBUG all jobs status:", debug_response.status_code, flush=True)
        print("DEBUG all jobs text:", debug_response.text[:2000], flush=True)

        if debug_response.status_code >= 400:
            raise HTTPException(
                status_code=500,
                detail=f"Supabase debug error: {debug_response.status_code} - {debug_response.text}",
            )

        queued_params = {
            "select": "*",
            "status": "eq.queued",
            "order": "created_at.asc",
            "limit": "1",
        }

        response = requests.get(
            url,
            headers=supabase_headers(),
            params=queued_params,
            timeout=30,
        )

        print("DEBUG queued status:", response.status_code, flush=True)
        print("DEBUG queued text:", response.text[:2000], flush=True)

        if response.status_code >= 400:
            raise HTTPException(
                status_code=500,
                detail=f"Supabase queued error: {response.status_code} - {response.text}",
            )

        jobs = response.json()

        if not jobs:
            print("ℹ️ Aucun job queued trouvé par le backend", flush=True)
            print("=" * 80 + "\n", flush=True)

            return {
                "status": "no_job",
                "message": "Aucun job en attente",
            }

        job = jobs[0]
        file_id = job.get("file_id")

        if not file_id:
            raise HTTPException(
                status_code=500,
                detail="Job queued trouvé mais file_id est vide.",
            )

        print(f"✅ Job selected for Colab: {file_id}", flush=True)

        raw_config = job.get("config")
        normalized_config = normalize_training_config(raw_config)
        manual_overrides = normalized_config["manual_overrides"]

        print(
            "Raw config from Supabase:",
            json.dumps(raw_config or {}, ensure_ascii=False, default=str),
            flush=True,
        )
        print(
            "Normalized config sent to Colab:",
            json.dumps(normalized_config, ensure_ascii=False, default=str),
            flush=True,
        )
        print(f"rnn_epochs: {manual_overrides.get('rnn_epochs')}", flush=True)
        print(f"qrnn_epochs: {manual_overrides.get('qrnn_epochs')}", flush=True)

        update_response = requests.patch(
            url,
            headers=supabase_headers(prefer="return=representation"),
            params={
                "file_id": f"eq.{file_id}",
                "status": "eq.queued",
            },
            json={
                "status": "processing",
                "config": normalized_config,
                "started_at": now_iso(),
                "updated_at": now_iso(),
            },
            timeout=30,
        )

        print("DEBUG update processing status:", update_response.status_code, flush=True)
        print("DEBUG update processing text:", update_response.text[:1000], flush=True)

        if update_response.status_code >= 400:
            raise HTTPException(
                status_code=500,
                detail=f"Supabase update error: {update_response.status_code} - {update_response.text}",
            )

        if not update_response.json():
            print("ℹ️ Job déjà pris par un autre worker", flush=True)
            print("=" * 80 + "\n", flush=True)
            return {
                "status": "no_job",
                "message": "Aucun job en attente",
            }

        print(f"✅ Sending file_id to Colab: {file_id}", flush=True)
        print("=" * 80 + "\n", flush=True)

        return {
            "file_id": file_id,
            "job_id": file_id,
            "config": normalized_config,
            "dataset_info": job.get("dataset_info") or {},
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ /api/next-job error:", e, flush=True)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# DATASET FOR COLAB
# ============================================================

@app.get("/api/dataset/{file_id}")
async def download_dataset(file_id: str):
    try:
        print(f"📥 Dataset requested for file_id: {file_id}")

        job = supabase_select_one_by_file_id(file_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job non trouvé dans Supabase",
            )

        file_path = job.get("file_path")

        if not file_path:
            matches = list(UPLOAD_DIR.glob(f"{file_id}_*.csv"))
            if matches:
                file_path = str(matches[0])

        if not file_path:
            raise HTTPException(
                status_code=404,
                detail=(
                    "file_path manquant dans training_jobs et fichier introuvable dans uploads."
                ),
            )

        path = Path(file_path)

        if not path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Fichier dataset introuvable: {path}",
            )

        filename = job.get("filename") or path.name

        return FileResponse(
            path,
            media_type="text/csv",
            filename=filename,
        )

    except HTTPException:
        raise

    except Exception as e:
        print("❌ download_dataset error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# METRICS / REPORT HELPERS
# ============================================================

def extract_accuracy(results: dict):
    try:
        if results.get("comparison", {}).get("qrnn_accuracy") is not None:
            return results["comparison"]["qrnn_accuracy"]

        if results.get("comparison", {}).get("rnn_accuracy") is not None:
            return results["comparison"]["rnn_accuracy"]

        if results.get("rnn", {}).get("accuracy") is not None:
            return results["rnn"]["accuracy"]

        qrnn = results.get("qrnn") or {}

        for key in ["clean", "noisy", "mitigated"]:
            if isinstance(qrnn.get(key), dict) and qrnn[key].get("accuracy") is not None:
                return qrnn[key]["accuracy"]

    except Exception:
        pass

    return "N/A"


def extract_model_name(results: dict):
    try:
        if results.get("comparison", {}).get("better_model"):
            return str(results["comparison"]["better_model"]).upper()

        if "rnn" in results and "qrnn" in results:
            return "RNN / QNN"

        if "rnn" in results:
            return "RNN / MLP"

        if "qrnn" in results:
            return "QNN"

    except Exception:
        pass

    return "Training Model"


def generate_pdf_report(file_id: str, results: dict, output_path: Path):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            Image,
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except Exception as e:
        raise RuntimeError("reportlab manquant. Installe: pip install reportlab") from e

    output_path.parent.mkdir(parents=True, exist_ok=True)

    dark = colors.HexColor("#101828")
    muted = colors.HexColor("#667085")
    panel = colors.HexColor("#F8FAFC")
    border = colors.HexColor("#D0D5DD")

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=dark,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=dark,
            spaceBefore=14,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallMuted",
            parent=styles["BodyText"],
            fontSize=8,
            leading=10,
            textColor=muted,
        )
    )

    def fmt_percent(value):
        return f"{value * 100:.2f}%" if isinstance(value, (int, float)) else "-"

    def fmt_number(value):
        if isinstance(value, bool):
            return str(value)
        if isinstance(value, int):
            return str(value)
        if isinstance(value, float):
            return f"{value:.4f}"
        return "-"

    def fmt_value(key, value):
        if value is None:
            return "-"
        if key in {
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "f1-score",
            "train_accuracy",
            "val_accuracy",
            "rnn_accuracy",
            "qrnn_accuracy",
            "improvement",
        }:
            return fmt_percent(value)
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        if isinstance(value, float):
            return f"{value:.4f}"
        return str(value)

    def make_table(data, col_widths=None, header=True, font_size=8):
        table = Table(data, colWidths=col_widths, repeatRows=1 if header else 0, hAlign="LEFT")
        style = [
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), font_size),
            ("LEADING", (0, 0), (-1, -1), font_size + 2),
            ("GRID", (0, 0), (-1, -1), 0.35, border),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
        if header:
            style.extend(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), dark),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        for row_index in range(1 if header else 0, len(data)):
            if row_index % 2 == 0:
                style.append(("BACKGROUND", (0, row_index), (-1, row_index), panel))
        table.setStyle(TableStyle(style))
        return table

    def section(title):
        return Paragraph(title, styles["SectionTitle"])

    def flatten_config(prefix, value, rows):
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                flatten_config(f"{prefix}.{nested_key}" if prefix else nested_key, nested_value, rows)
            return
        rows.append([prefix, fmt_value(prefix, value)])

    def model_blocks():
        blocks = []
        if isinstance(results.get("rnn"), dict):
            blocks.append(("Classical RNN", results["rnn"]))

        qrnn = results.get("qrnn")
        if isinstance(qrnn, dict):
            added_variant = False
            variant_titles = {
                "clean": "QNN Clean",
                "noisy": "QNN Noisy",
                "mitigated": "QNN Mitigated",
            }
            for variant, title in variant_titles.items():
                if isinstance(qrnn.get(variant), dict):
                    blocks.append((title, qrnn[variant]))
                    added_variant = True
            if not added_variant and "accuracy" in qrnn:
                blocks.append(("QNN", qrnn))
        return blocks

    def metric_rows(block):
        rows = [["Metric", "Value"]]
        metric_keys = [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "loss",
            "train_loss",
            "val_loss",
            "train_accuracy",
            "val_accuracy",
            "train_size",
            "val_size",
            "test_size",
        ]
        for key in metric_keys:
            if key in block:
                rows.append([key.replace("_", " ").title(), fmt_value(key, block.get(key))])
            if key == "loss":
                training_time = get_training_time_formatted(block)
                if training_time != "-":
                    rows.append(["Training Time", training_time])
        return rows

    def confusion_matrix_table(block):
        matrix = block.get("confusion_matrix")
        if not isinstance(matrix, list) or not matrix:
            return None
        max_columns = max((len(row) for row in matrix if isinstance(row, list)), default=0)
        if max_columns == 0:
            return None
        class_names = block.get("class_names") if isinstance(block.get("class_names"), list) else None
        labels = [str(item) for item in class_names] if class_names else [str(i) for i in range(max(len(matrix), max_columns))]
        data = [["Actual / Predicted", *[f"Class {label}" for label in labels[:max_columns]]]]
        for index, row in enumerate(matrix):
            if isinstance(row, list):
                padded = [*row, *[""] * (max_columns - len(row))]
                label = labels[index] if index < len(labels) else str(index)
                data.append([f"Class {label}", *padded])
        first_width = 1.25 * inch
        value_width = min(0.8 * inch, max(0.42 * inch, (6.5 * inch - first_width) / max_columns))
        return make_table(
            data,
            [first_width, *([value_width] * max_columns)],
            header=True,
            font_size=7 if max_columns > 4 else 8,
        )

    def classification_report_table(block):
        report = block.get("classification_report")
        if not isinstance(report, dict):
            return None
        rows = [["Class", "Precision", "Recall", "F1 Score", "Support"]]

        def is_report_row(item):
            _, metrics = item
            return isinstance(metrics, dict) and any(
                key in metrics for key in ["precision", "recall", "f1-score", "support"]
            )

        def sort_key(item):
            label, _ = item
            if label == "macro avg":
                return (1, 0, label)
            if label == "weighted avg":
                return (1, 1, label)
            try:
                return (0, int(label), label)
            except (TypeError, ValueError):
                return (0, 999999, str(label))

        for label, metrics in sorted([item for item in report.items() if is_report_row(item)], key=sort_key):
            rows.append(
                [
                    str(label),
                    fmt_percent(metrics.get("precision")),
                    fmt_percent(metrics.get("recall")),
                    fmt_percent(metrics.get("f1-score")),
                    fmt_number(metrics.get("support")),
                ]
            )
        if isinstance(report.get("accuracy"), (int, float)):
            rows.append(["Accuracy", "", "", fmt_percent(report["accuracy"]), ""])
        return make_table(rows, [0.9 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 0.9 * inch], font_size=7)

    def history_rows(block):
        history = block.get("history")
        if not isinstance(history, dict):
            return []
        max_len = max((len(values) for values in history.values() if isinstance(values, list)), default=0)
        if max_len == 0:
            return []
        train_loss = history.get("train_loss") or history.get("loss") or []
        val_loss = history.get("val_loss") or []
        train_acc = history.get("train_acc") or history.get("train_accuracy") or history.get("accuracy") or []
        val_acc = history.get("val_acc") or history.get("val_accuracy") or []
        rows = [["Epoch", "Train Loss", "Val Loss", "Train Acc", "Val Acc"]]
        for index in range(max_len):
            rows.append(
                [
                    str(index + 1),
                    fmt_number(train_loss[index] if index < len(train_loss) else None),
                    fmt_number(val_loss[index] if index < len(val_loss) else None),
                    fmt_percent(train_acc[index] if index < len(train_acc) else None),
                    fmt_percent(val_acc[index] if index < len(val_acc) else None),
                ]
            )
        return rows

    def make_curve_image(blocks, metric):
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception:
            return None

        fig, ax = plt.subplots(figsize=(4.9, 2.2), dpi=150)
        plotted = False
        palette = ["#7C3AED", "#06B6D4", "#14B8A6", "#F97316"]
        for index, (title, block) in enumerate(blocks):
            history = block.get("history")
            if not isinstance(history, dict):
                continue
            if metric == "accuracy":
                series = history.get("val_acc") or history.get("val_accuracy") or history.get("accuracy") or history.get("train_acc")
                ylabel = "Accuracy"
            else:
                series = history.get("val_loss") or history.get("loss") or history.get("train_loss")
                ylabel = "Loss"
            if isinstance(series, list) and series:
                ax.plot(
                    range(1, len(series) + 1),
                    series,
                    marker="o",
                    markersize=2,
                    linewidth=1.6,
                    label=title,
                    color=palette[index % len(palette)],
                )
                plotted = True
        if not plotted:
            plt.close(fig)
            return None
        ax.set_title(f"{ylabel} Curves", fontsize=8)
        ax.set_xlabel("Epoch", fontsize=7)
        ax.set_ylabel(ylabel, fontsize=7)
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=5)
        ax.tick_params(labelsize=6)
        fig.tight_layout()
        image_path = output_path.parent / f"{file_id}_{metric}_curve.png"
        fig.savefig(image_path, bbox_inches="tight")
        plt.close(fig)
        return image_path

    def page_canvas(canvas_obj, doc):
        canvas_obj.saveState()
        canvas_obj.setFillColor(dark)
        canvas_obj.rect(0, A4[1] - 36, A4[0], 36, stroke=0, fill=1)
        canvas_obj.setFillColor(colors.white)
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(36, A4[1] - 22, "NeuroSpace Evaluation Report")
        canvas_obj.setFillColor(muted)
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.drawRightString(A4[0] - 36, 22, f"Page {doc.page}")
        canvas_obj.restoreState()

    story = []
    logo_candidates = [
        BASE_DIR.parent / "frontend" / "public" / "assets" / "images" / "app_logo1.png",
        BASE_DIR.parent / "frontend" / "public" / "app_logo1.png",
    ]
    logo_path = next((path for path in logo_candidates if path.exists()), None)
    logo = Image(str(logo_path), width=0.65 * inch, height=0.65 * inch) if logo_path else Paragraph("NS", styles["ReportTitle"])

    header = Table(
        [
            [
                logo,
                [
                    Paragraph("NeuroSpace", styles["ReportTitle"]),
                    Paragraph("Complete evaluation export", styles["SmallMuted"]),
                ],
            ]
        ],
        colWidths=[1.0 * inch, 5.5 * inch],
    )
    header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(Spacer(1, 0.42 * inch))
    story.append(header)
    story.append(Spacer(1, 0.18 * inch))
    story.append(
        make_table(
            [
                ["Job ID", file_id],
                ["Status", str(results.get("status", "completed"))],
                ["Result timestamp", str(results.get("timestamp") or "-")],
                ["PDF generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ],
            [1.35 * inch, 5.15 * inch],
            header=False,
            font_size=8,
        )
    )

    config_rows = [["Parameter", "Value"]]
    flatten_config("", results.get("config_used") or {}, config_rows)
    if len(config_rows) > 1:
        story.append(section("Pipeline Configuration"))
        story.append(make_table(config_rows, [2.2 * inch, 4.3 * inch]))

    comparison = results.get("comparison")
    if isinstance(comparison, dict):
        story.append(section("Best Model"))
        story.append(
            make_table(
                [
                    ["Winner", "RNN Accuracy", "QNN Accuracy", "Improvement"],
                    [
                        str(comparison.get("better_model", "-")).upper(),
                        fmt_percent(comparison.get("rnn_accuracy")),
                        fmt_percent(comparison.get("qrnn_accuracy")),
                        fmt_percent(comparison.get("improvement")),
                    ],
                ],
                [1.4 * inch, 1.55 * inch, 1.55 * inch, 1.55 * inch],
            )
        )

    blocks = model_blocks()
    if blocks:
        story.append(section("Evaluation Summary"))
        summary_rows = [["Model", "Accuracy", "Precision", "Recall", "F1 Score", "Loss", "Training Time"]]
        for title, block in blocks:
            summary_rows.append(
                [
                    title,
                    fmt_percent(block.get("accuracy")),
                    fmt_percent(block.get("precision")),
                    fmt_percent(block.get("recall")),
                    fmt_percent(block.get("f1_score")),
                    fmt_number(block.get("loss")),
                    get_training_time_formatted(block),
                ]
            )
        story.append(
            make_table(
                summary_rows,
                [
                    1.35 * inch,
                    0.85 * inch,
                    0.85 * inch,
                    0.85 * inch,
                    0.9 * inch,
                    0.7 * inch,
                    1.0 * inch,
                ],
            )
        )

    accuracy_curve = make_curve_image(blocks, "accuracy")
    loss_curve = make_curve_image(blocks, "loss")
    if accuracy_curve or loss_curve:
        story.append(section("Learning Curves"))
        story.append(PageBreak())
        curve_cells = []
        if accuracy_curve:
            curve_cells.append(Image(str(accuracy_curve), width=3.1 * inch, height=1.55 * inch))
        if loss_curve:
            curve_cells.append(Image(str(loss_curve), width=3.1 * inch, height=1.55 * inch))
        story.append(Spacer(1, 0.45 * inch))
        story.append(Table([curve_cells], colWidths=[3.2 * inch] * len(curve_cells), hAlign="CENTER"))

    for title, block in blocks:
        story.append(PageBreak())
        story.append(section(title))
        story.append(make_table(metric_rows(block), [2.0 * inch, 4.0 * inch], font_size=8))

        cm_table = confusion_matrix_table(block)
        if cm_table:
            story.append(section(f"{title} Confusion Matrix"))
            story.append(cm_table)

        report_table = classification_report_table(block)
        if report_table:
            story.append(section(f"{title} Classification Report"))
            story.append(report_table)

        rows = history_rows(block)
        if rows:
            story.append(section(f"{title} Epoch History"))
            story.append(make_table(rows, [0.65 * inch, 1.15 * inch, 1.15 * inch, 1.15 * inch, 1.15 * inch], font_size=7))

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=54,
        bottomMargin=36,
        title=f"NeuroSpace Evaluation Report - {file_id}",
    )
    doc.build(story, onFirstPage=page_canvas, onLaterPages=page_canvas)


def send_report_email(
    to_email: str,
    to_name: str | None,
    file_id: str,
    pdf_path: Path,
    json_path: Path | None,
    results: dict,
):
    if not to_email:
        return {
            "success": False,
            "error": "Recipient email missing",
        }

    if not EMAIL_FROM or not BREVO_SMTP_USER or not BREVO_SMTP_PASSWORD:
        return {
            "success": False,
            "error": "Brevo SMTP env missing. Email skipped.",
        }

    if not pdf_path.exists():
        return {
            "success": False,
            "error": f"PDF not found: {pdf_path}",
        }

    try:
        subject = "Your NeuroSpace Training Report is Ready"
        created_at = results.get("timestamp") or now_iso()

        body = f"""Hello {to_name or "User"},

Your training and classification process has been completed successfully.

The generated PDF report is now ready and contains the full classification results.

Summary:
- Generated at: {created_at}

Thank you for using NeuroSpace.

Best regards,
NeuroSpace Team
"""

        msg = EmailMessage()
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with open(pdf_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=f"neurospace-report-{file_id}.pdf",
            )

        if json_path and json_path.exists():
            with open(json_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="json",
                    filename=f"results-{file_id}.json",
                )

        with smtplib.SMTP(BREVO_SMTP_HOST, BREVO_SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(BREVO_SMTP_USER, BREVO_SMTP_PASSWORD)
            smtp.send_message(msg)

        print(f"📧 Email sent to {to_email}")

        return {
            "success": True,
            "error": None,
        }

    except Exception as e:
        print("❌ Brevo email error:", e)
        traceback.print_exc()

        return {
            "success": False,
            "error": str(e),
        }


# ============================================================
# COMPLETE JOB FROM COLAB
# ============================================================

@app.post("/api/job/{file_id}/complete")
async def complete_job(file_id: str, request: Request):
    try:
        print(f"✅ Complete job received for file_id: {file_id}")

        results = await request.json()
        results = make_json_serializable(results)
        results = ensure_training_times(results)

        job = supabase_select_one_by_file_id(file_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job non trouvé dans Supabase",
            )

        user_email = job.get("user_email")
        user_name = job.get("user_name")

        if not user_email:
            raise HTTPException(
                status_code=400,
                detail="user_email manquant dans training_jobs",
            )

        result_dir = RESULTS_DIR / file_id
        result_dir.mkdir(parents=True, exist_ok=True)

        json_path = result_dir / "results.json"
        pdf_path = result_dir / "report.pdf"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"💾 Results JSON saved: {json_path}")

        generate_pdf_report(file_id, results, pdf_path)

        print(f"📄 PDF generated: {pdf_path}")

        pdf_storage_key = supabase_storage_upload_pdf(file_id, pdf_path)
        json_storage_key = supabase_storage_upload_json(file_id, json_path)

        print(f"☁️ PDF uploaded to Supabase Storage: {pdf_storage_key}")
        print(f"☁️ JSON uploaded to Supabase Storage: {json_storage_key}")

        supabase_update_by_file_id(
            file_id,
            {
                "status": "completed",
                "results": results,
                "json_path": json_storage_key,
                "pdf_path": pdf_storage_key,
                "completed_at": now_iso(),
            },
        )

        print("📧 Brevo email sending started")

        email_result = send_report_email(
            to_email=user_email,
            to_name=user_name,
            file_id=file_id,
            pdf_path=pdf_path,
            json_path=json_path,
            results=results,
        )

        supabase_update_by_file_id(
            file_id,
            {
                "email_sent": bool(email_result.get("success")),
                "email_sent_to": user_email,
                "email_sent_at": now_iso() if email_result.get("success") else None,
                "email_error": None if email_result.get("success") else email_result.get("error"),
            },
        )

        if email_result.get("success"):
            print("✅ Brevo email sent successfully")
        else:
            print(f"⚠️ Brevo email failed/skipped: {email_result.get('error')}")

        return {
            "success": True,
            "file_id": file_id,
            "message": "Job completed",
            "email_sent": bool(email_result.get("success")),
            "email_error": None if email_result.get("success") else email_result.get("error"),
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ complete_job error:", e)
        traceback.print_exc()

        try:
            supabase_update_by_file_id(
                file_id,
                {
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": now_iso(),
                },
            )
        except Exception:
            pass

        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# FAIL / FAILED JOB
# ============================================================

async def mark_job_failed(file_id: str, payload: dict):
    error_message = (
        payload.get("error")
        or payload.get("message")
        or payload.get("detail")
        or "Erreur inconnue"
    )

    print(f"❌ Job failed: {file_id} - {error_message}")

    job = supabase_select_one_by_file_id(file_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job non trouvé dans Supabase",
        )

    supabase_update_by_file_id(
        file_id,
        {
            "status": "failed",
            "error_message": str(error_message),
            "completed_at": now_iso(),
        },
    )

    return {
        "success": True,
        "message": "Job marked as failed",
        "file_id": file_id,
    }


@app.post("/api/job/{file_id}/failed")
async def failed_job(file_id: str, request: Request):
    payload = await request.json()
    return await mark_job_failed(file_id, payload)


@app.post("/api/job/{file_id}/fail")
async def fail_job(file_id: str, request: Request):
    payload = await request.json()
    return await mark_job_failed(file_id, payload)


# ============================================================
# STATUS + RESULTS
# ============================================================

@app.get("/api/job/{file_id}/status")
async def get_job_status(file_id: str):
    try:
        job = supabase_select_one_by_file_id(file_id)

        if not job:
            raise HTTPException(status_code=404, detail="Job non trouvé")

        return {
            "job_id": file_id,
            "file_id": file_id,
            "status": job.get("status"),
            "message": job.get("error_message") if job.get("status") == "failed" else None,
            "error": job.get("error_message"),
            "email_sent": job.get("email_sent"),
            "email_error": job.get("email_error"),
            "created_at": job.get("created_at"),
            "started_at": job.get("started_at"),
            "completed_at": job.get("completed_at"),
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ get_job_status error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/results/{file_id}")
async def get_results(file_id: str):
    try:
        job = supabase_select_one_by_file_id(file_id)

        if not job:
            raise HTTPException(status_code=404, detail="Job non trouvé")

        if job.get("status") != "completed":
            raise HTTPException(
                status_code=400,
                detail=f"Résultats pas encore prêts: {job.get('status')}",
            )

        results = job.get("results")

        if results:
            return results

        json_path = job.get("json_path")

        if json_path and Path(json_path).exists():
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)

        raise HTTPException(status_code=404, detail="Résultats introuvables")

    except HTTPException:
        raise

    except Exception as e:
        print("❌ get_results error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/report/{file_id}/pdf")
@app.get("/api/report/{file_id}/download")
async def download_report(file_id: str):
    try:
        job = supabase_select_one_by_file_id(file_id)

        if not job:
            raise HTTPException(status_code=404, detail="Job non trouvé")

        pdf_path = job.get("pdf_path")

        if not pdf_path:
            raise HTTPException(
                status_code=404,
                detail="PDF path manquant dans Supabase",
            )

        if is_supabase_storage_key(pdf_path):
            pdf_bytes = supabase_storage_download_file(pdf_path)

            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'attachment; filename="neurospace-report-{file_id}.pdf"'
                },
            )

        path = Path(pdf_path)

        if not path.exists():
            fallback_path = RESULTS_DIR / file_id / "report.pdf"

            if fallback_path.exists():
                path = fallback_path
            else:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        "PDF introuvable localement. "
                        "Le rapport doit être stocké dans Supabase Storage. "
                        "Relance un training pour générer et uploader le PDF."
                    ),
                )

        return FileResponse(
            path,
            media_type="application/pdf",
            filename=f"neurospace-report-{file_id}.pdf",
        )

    except HTTPException:
        raise

    except Exception as e:
        print("❌ download_report error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# DEBUG
# ============================================================

@app.get("/api/debug/jobs")
async def debug_jobs():
    try:
        url = supabase_rest_url(SUPABASE_TABLE)

        params = {
            "select": "file_id,user_email,status,created_at,started_at,completed_at,file_path,filename",
            "order": "created_at.desc",
            "limit": "10",
        }

        response = requests.get(
            url,
            headers=supabase_headers(),
            params=params,
            timeout=30,
        )

        if response.status_code >= 400:
            raise HTTPException(status_code=500, detail=response.text)

        return {
            "success": True,
            "supabase_url": SUPABASE_URL,
            "service_role_exists": bool(SUPABASE_SERVICE_ROLE_KEY),
            "jobs": response.json(),
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ debug_jobs error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("==============================================")
    print("🚀 NeuroSpace Backend starting")
    print("ENV_PATH:", ENV_PATH)
    print("ENV_PATH exists:", ENV_PATH.exists())
    print("SUPABASE_URL exists:", bool(SUPABASE_URL))
    print("SUPABASE_SERVICE_ROLE_KEY exists:", bool(SUPABASE_SERVICE_ROLE_KEY))
    print("BREVO_SMTP_USER exists:", bool(BREVO_SMTP_USER))
    print("BREVO_SMTP_PASSWORD exists:", bool(BREVO_SMTP_PASSWORD))
    print("EMAIL_FROM exists:", bool(EMAIL_FROM))
    print("UPLOAD_DIR:", UPLOAD_DIR)
    print("RESULTS_DIR:", RESULTS_DIR)
    print("==============================================")

    uvicorn.run(app, host="0.0.0.0", port=7000)
