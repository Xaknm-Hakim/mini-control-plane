from __future__ import annotations


def format_host_status(data: dict[str, str]) -> str:
    return (
        "🖥️ Host Status\n"
        f"Hostname: {data['hostname']}\n"
        f"System: {data['system']} {data['release']}\n"
        f"Uptime: {data['uptime']}\n"
        f"Boot Time: {data['boot_time']}\n"
        f"CPU Usage: {data['cpu_percent']}\n"
        f"Load Avg: {data['load_avg']}\n"
        f"Memory: {data['memory_used']} / {data['memory_total']} ({data['memory_percent']})\n"
        f"Disk: {data['disk_used']} / {data['disk_total']} ({data['disk_percent']})"
    )
