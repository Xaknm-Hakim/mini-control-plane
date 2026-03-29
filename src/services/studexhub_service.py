from __future__ import annotations

import subprocess


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


def restart_studexhub() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            DOCKER_CMD,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            return False, result.stderr

        return True, result.stdout

    except Exception as e:
        return False, str(e)
