from __future__ import annotations

import platform
import socket
from datetime import datetime

import psutil


def get_host_status() -> dict[str, str]:
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_delta = datetime.now() - boot_time

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    load_avg = "N/A"
    try:
        load1, load5, load15 = psutil.getloadavg()
        load_avg = f"{load1:.2f}, {load5:.2f}, {load15:.2f}"
    except (AttributeError, OSError):
        pass

    return {
        "hostname": socket.gethostname(),
        "system": platform.system(),
        "release": platform.release(),
        "cpu_percent": f"{psutil.cpu_percent(interval=1):.1f}%",
        "memory_percent": f"{memory.percent:.1f}%",
        "memory_used": f"{memory.used / (1024**3):.2f} GB",
        "memory_total": f"{memory.total / (1024**3):.2f} GB",
        "disk_percent": f"{disk.percent:.1f}%",
        "disk_used": f"{disk.used / (1024**3):.2f} GB",
        "disk_total": f"{disk.total / (1024**3):.2f} GB",
        "uptime": str(uptime_delta).split(".")[0],
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "load_avg": load_avg,
    }
