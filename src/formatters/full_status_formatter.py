from __future__ import annotations


def format_full_status(host_block: str, services_block: str) -> str:
    return (
        "📊 Full System Status\n\n"
        "=== Host ===\n"
        f"{host_block}\n\n"
        "=== Services ===\n"
        f"{services_block}"
    )
