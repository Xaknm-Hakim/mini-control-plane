from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / "env" / ".env"
BOT_CONFIG_PATH = PROJECT_ROOT / "config" / "bot.yaml"


def load_env() -> dict[str, str | int]:
    load_dotenv(ENV_PATH)

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    admin_id = os.getenv("ADMIN_TELEGRAM_ID")

    if not token:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN in env/.env")

    if not admin_id:
        raise ValueError("Missing ADMIN_TELEGRAM_ID in env/.env")

    return {
        "token": token,
        "admin_id": int(admin_id),
    }


def load_bot_config() -> dict:
    if not BOT_CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config file: {BOT_CONFIG_PATH}")

    with BOT_CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
