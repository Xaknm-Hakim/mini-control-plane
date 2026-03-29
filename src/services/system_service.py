from __future__ import annotations

import subprocess


def check_systemd_service(service_name: str) -> str:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True,
        )

        status = result.stdout.strip()

        if status == "active":
            return f"✅ {service_name}: active"
        elif status == "inactive":
            return f"⚠️ {service_name}: inactive"
        else:
            return f"❌ {service_name}: {status}"

    except Exception as error:
        return f"❌ {service_name}: error ({error})"


def check_docker_containers() -> str:
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}: {{.Status}}"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return "❌ docker ps failed"

        output = result.stdout.strip()

        if not output:
            return "⚠️ No running containers"

        return "🐳 Containers:\n" + output

    except Exception as error:
        return f"❌ docker error: {error}"


def get_system_services_status() -> str:
    services = ["cloudflared", "nginx", "docker"]

    results = ["🖥️ System Services:\n"]

    for svc in services:
        results.append(check_systemd_service(svc))

    results.append("\n" + check_docker_containers())

    return "\n".join(results)
