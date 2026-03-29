from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


PROJECT_PATH = "/opt/baruashub/StudexHub"

DOCKER_CMD = [
    "docker",
    "compose",
    "--env-file",
    "infra/docker/.env.docker",
    "-f",
    "infra/docker/docker-compose.yml",
    "up",
    "-d",
    "--build",
]

BACKUP_DIR = Path("/opt/baruashub/StudexHub/storage/backups")
DB_CONTAINER_NAME = "baruashub-db"
DB_NAME = "baruashub"
DB_USER = "postgres"


def restart_studexhub() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            DOCKER_CMD,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            timeout=300,
        )

        output = (result.stdout or "") + (
            ("\n" + result.stderr) if result.stderr else ""
        )

        if result.returncode != 0:
            return False, output.strip()

        return True, output.strip() or "StudexHub restarted successfully."

    except Exception as error:
        return False, str(error)


def backup_studexhub() -> tuple[bool, str]:
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = BACKUP_DIR / f"studexhub_backup_{timestamp}.sql"

        command = [
            "docker",
            "exec",
            DB_CONTAINER_NAME,
            "pg_dump",
            "-U",
            DB_USER,
            "-d",
            DB_NAME,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            error_output = (result.stderr or result.stdout or "").strip()
            return False, error_output or "pg_dump failed."

        backup_path.write_text(result.stdout, encoding="utf-8")

        return True, f"Backup created: {backup_path}"

    except Exception as error:
        return False, str(error)
