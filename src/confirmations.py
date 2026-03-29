from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Confirmation:
    user_id: int
    action: str
    created_at: datetime
    expires_at: datetime


_confirmations: dict[int, Confirmation] = {}


def create_confirmation(user_id: int, action: str, timeout_seconds: int = 180) -> None:
    now = datetime.now()

    _confirmations[user_id] = Confirmation(
        user_id=user_id,
        action=action,
        created_at=now,
        expires_at=now + timedelta(seconds=timeout_seconds),
    )


def get_confirmation(user_id: int) -> Confirmation | None:
    confirmation = _confirmations.get(user_id)

    if confirmation is None:
        return None

    if datetime.now() > confirmation.expires_at:
        _confirmations.pop(user_id, None)
        return None

    return confirmation


def clear_confirmation(user_id: int) -> None:
    _confirmations.pop(user_id, None)
