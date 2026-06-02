# backend/ngrok_setup.py

import os
import subprocess
import time
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parent
NGROK_LOG = BASE_DIR / "ngrok.log"
NGROK_URL_FILE = BASE_DIR / "ngrok_url.txt"


def _run_command(command):
    return subprocess.run(
        command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _print_ngrok_log():
    if not NGROK_LOG.exists():
        print("Aucun fichier ngrok.log trouve.")
        return

    print("\nDernieres lignes de ngrok.log:")
    print("-" * 60)
    lines = NGROK_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines[-30:]:
        print(line)
    print("-" * 60)


def _check_local_backend(port):
    try:
        response = requests.get(f"http://127.0.0.1:{port}/", timeout=3)
        if response.status_code == 200:
            return True
        print(f"Backend local detecte sur {port}, mais status={response.status_code}")
        return True
    except Exception as exc:
        print(f"Attention: FastAPI ne repond pas sur http://127.0.0.1:{port}/")
        print(f"Detail: {exc}")
        return False


def setup_ngrok(port=7000):
    """
    Lance ngrok et recupere l'URL publique.
    """

    print("Configuration de ngrok...")

    ngrok_path = BASE_DIR / "ngrok.exe" if os.name == "nt" else Path("ngrok")

    if os.name == "nt" and not ngrok_path.exists():
        print("ngrok.exe non trouve dans le dossier backend")
        print("Telecharge-le ici: https://ngrok.com/download")
        return None

    try:
        version = _run_command([str(ngrok_path), "--version"])
        if version.returncode != 0:
            print("Impossible de lire la version de ngrok:")
            print(version.stderr.strip() or version.stdout.strip())
            return None
        print(f"Ngrok detecte: {version.stdout.strip()}")
    except Exception as exc:
        print(f"Impossible de lancer ngrok: {exc}")
        return None

    _check_local_backend(port)

    print("Arret des anciens tunnels ngrok...")
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/IM", "ngrok.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(["pkill", "ngrok"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2)

    if NGROK_LOG.exists():
        NGROK_LOG.unlink()

    print(f"Lancement de ngrok sur le port {port}...")

    with open(NGROK_LOG, "w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            [
                str(ngrok_path),
                "http",
                str(port),
                "--log",
                str(NGROK_LOG),
                "--log-format",
                "logfmt",
            ],
            cwd=BASE_DIR,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )

    print("Attente du demarrage de ngrok...")

    for i in range(30):
        time.sleep(1)

        if process.poll() is not None:
            print(f"ngrok s'est arrete immediatement avec le code {process.returncode}.")
            _print_ngrok_log()
            print("\nCa indique souvent un authtoken absent, une session ngrok deja active ailleurs,")
            print("ou une configuration locale ngrok differente sur ce PC.")
            return None

        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=2)
            tunnels = response.json().get("tunnels", [])

            public_url = next(
                (
                    tunnel.get("public_url")
                    for tunnel in tunnels
                    if tunnel.get("proto") == "https" and tunnel.get("public_url")
                ),
                None,
            )

            if not public_url and tunnels:
                public_url = tunnels[0].get("public_url")

            if public_url:
                NGROK_URL_FILE.write_text(public_url, encoding="utf-8")
                print(f"URL publique: {public_url}")
                print(f"API pour Colab: {public_url}/api")
                return public_url

        except Exception:
            pass

        print(f"   {i + 1}/30 secondes...")

    print("Impossible de recuperer l'URL publique depuis http://127.0.0.1:4040/api/tunnels")
    _print_ngrok_log()
    print("\nSi ngrok.log contient ERR_NGROK_108, ferme ngrok sur l'autre PC ou change de compte.")
    print("Si le log parle d'authtoken, execute: .\\ngrok.exe config add-authtoken TON_TOKEN")
    return None


def get_ngrok_url():
    """Recupere l'URL sauvegardee."""

    if NGROK_URL_FILE.exists():
        return NGROK_URL_FILE.read_text(encoding="utf-8").strip()

    return None


if __name__ == "__main__":
    url = setup_ngrok()

    if url:
        print("\nURL a utiliser dans Google Colab:")
        print(f"{url}/api")
        print("\nngrok est actif")
        print("Laisse ce terminal ouvert")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nArret de ngrok")
    else:
        print("\nEchec du lancement automatique")
        print("\nSolution manuelle:")
        print("1. Ouvre un nouveau terminal")
        print("2. cd backend")
        print("3. .\\ngrok.exe config add-authtoken TON_TOKEN")
        print("4. .\\ngrok.exe http 7000")
