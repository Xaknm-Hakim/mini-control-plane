from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv("env/.env")

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("ADMIN_TELEGRAM_ID")

def send_telegram(message: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_BOT_TOKEN or ADMIN_TELEGRAM_ID")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=10,
    )
    print("Telegram status:", response.status_code)
    print("Telegram response:", response.text)

@app.route("/alerts", methods=["POST"])
def alerts():
    data = request.json or {}
    alerts = data.get("alerts", [])

    for alert in alerts:
        status = alert.get("status", "unknown")
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        name = labels.get("alertname", "UnknownAlert")
        severity = labels.get("severity", "unknown")
        summary = annotations.get("summary", "No summary")
        description = annotations.get("description", "No description")

        message = f"""[{severity.upper()}] {name}

Status: {status}

{summary}
{description}
"""
        send_telegram(message)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
