from __future__ import annotations

import subprocess
import time
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
WEB_CONTAINER_NAME = "baruashub-web"


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
        start_time = time.time()

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

        duration = round(time.time() - start_time, 2)
        size_mb = round(backup_path.stat().st_size / (1024 * 1024), 2)

        return True, (
            f"Backup created:\n"
            f"{backup_path}\n"
            f"Size: {size_mb} MB\n"
            f"Time: {duration}s"
        )

    except Exception as error:
        return False, str(error)


def create_invite() -> tuple[bool, str]:
    try:
        command = [
            "docker",
            "exec",
            WEB_CONTAINER_NAME,
            "npx",
            "tsx",
            "scripts/create-invite.ts",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = (result.stdout or "") + (
            ("\n" + result.stderr) if result.stderr else ""
        )

        if result.returncode != 0:
            return False, output.strip() or "Invite generation failed."

        return True, output.strip() or "Invite created."

    except Exception as error:
        return False, str(error)


def list_notice_templates() -> tuple[bool, str]:
    try:
        command = [
            "docker",
            "exec",
            WEB_CONTAINER_NAME,
            "npx",
            "tsx",
            "scripts/list-notices.ts",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = (result.stdout or "") + (
            ("\n" + result.stderr) if result.stderr else ""
        )

        if result.returncode != 0:
            return False, output.strip() or "Failed to list notice templates."

        return True, output.strip() or "No notice templates found."

    except Exception as error:
        return False, str(error)


def send_notice(template_name: str, test_mode: bool = False) -> tuple[bool, str]:
    try:
        command = [
            "docker",
            "exec",
            WEB_CONTAINER_NAME,
            "npx",
            "tsx",
            "scripts/send-notice.ts",
            template_name,
        ]

        if test_mode:
            command.append("--test")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=600,
        )

        output = (result.stdout or "") + (
            ("\n" + result.stderr) if result.stderr else ""
        )

        if result.returncode != 0:
            return False, output.strip() or "Notice process failed."

        return True, output.strip() or "Notice process completed."

    except Exception as error:
        return False, str(error)
