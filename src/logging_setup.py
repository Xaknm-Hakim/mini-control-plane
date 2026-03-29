from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(exist_ok=True)

BOT_LOG_PATH = LOG_DIR / "bot.log"
ACTION_LOG_PATH = LOG_DIR / "actions.log"


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(BOT_LOG_PATH),
            logging.StreamHandler(),
        ],
    )


def get_logger(name: str = "bot") -> logging.Logger:
    return logging.getLogger(name)


def log_action(user_id: int, username: str | None, action: str, status: str) -> None:
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "username": username,
        "action": action,
        "status": status,
    }

    with ACTION_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry) + "\n")
