from __future__ import annotations


def format_help() -> str:
    return (
        "🤖 mini-control-plane\n\n"
        "Global commands:\n"
        "/ping - Check if the bot is alive\n"
        "/help - Show this help message\n"
        "/host_status - Show host system status\n"
        "/system_services - Check cloudflared, nginx, docker, and running containers\n"
        "/full_status - Combined host + services system overview\n\n"
        "StudexHub commands:\n"
        "/studexhub_restart - Safely restart StudexHub with confirmation\n"
        "/studexhub_backup - Create a timestamped StudexHub database backup\n"
        "/studexhub_invite - Generate a new StudexHub invite code\n"
        "/studexhub_templates - List available notice templates\n"
        "/studexhub_notice <filename> test - Send notice to admin test target only\n"
        "/studexhub_notice <filename> - Send notice to all users\n"
    )
