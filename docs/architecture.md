# StudexHub Mini Control Plane — Architecture

## 📅 Last Updated

9 April 2026 (MYT)

---

## 🧠 Purpose

The Mini Control Plane is a system-level Telegram bot designed to act as the operational interface for StudexHub infrastructure.

It serves four main roles:

* Execute system-level commands via Telegram
* Provide real-time infrastructure visibility
* Receive and process alerts from monitoring stack
* Centralize operational workflows into a single control channel

---

## 🏗️ High-Level Architecture

### Control Flow (User → System)

```
User (Telegram)
→ Telegram Bot API
→ Mini Control Plane
→ System (Docker / Services / OS)
→ Response → Telegram
```

---

### Alert Flow (System → User)

```
Prometheus
→ Alertmanager
→ Webhook (HTTP POST)
→ Mini Control Plane
→ Telegram Notification
```

---

## 🔁 Detailed Flow Breakdown

### 1. Command Execution Flow

1. User sends command via Telegram (e.g., `/host_status`)
2. Telegram Bot API forwards update to bot
3. Bot parses command and validates input
4. Command handler routes execution logic
5. System-level action executed (Docker, systemctl, scripts)
6. Output formatted and sent back to Telegram

---

### 2. Alert Processing Flow

1. Prometheus evaluates alert rules continuously
2. Alert condition met (e.g., `probe_success == 0`)
3. Alertmanager triggers alert event
4. Alertmanager sends HTTP POST to webhook endpoint
5. Webhook receives JSON payload
6. Bot parses alert fields:

   * alert name
   * severity
   * status (firing/resolved)
   * summary
   * description
7. Bot formats message
8. Telegram notification sent to user

---

## 🧩 Core Components

### Telegram Bot Interface

* Primary user interaction layer
* Handles incoming commands and outgoing responses
* Uses Telegram Bot API

---

### Command Handler

* Parses and validates commands
* Routes execution logic
* Ensures safe command execution
* Maintains structured command flow

---

### Webhook Server

* Lightweight HTTP server (Flask)
* Endpoint: `/alerts`
* Receives Alertmanager payloads
* Stateless processing design

---

### System Execution Layer

Responsible for executing:

* Docker commands (`docker ps`, restart, etc.)
* Service management (`systemctl`)
* Backup operations (e.g., PostgreSQL dump)
* System checks (CPU, memory, disk)

---

## 🔐 Security Model

### Execution Isolation

* Runs under dedicated user: `bot-runner`
* No direct root execution
* Controlled permissions via group membership (e.g., docker)

---

### Command Safety

* Critical operations require explicit confirmation
* Strict command allowlist
* No arbitrary shell execution exposed

---

### Network Exposure

* Webhook bound to local interface (`localhost:5001`)
* Not publicly exposed
* Only Alertmanager communicates with webhook

---

## ⚙️ Deployment Architecture

```
/opt/bot/mini-control-plane
├── webhook.py
├── main bot logic
├── env/
│   └── .env
├── logs/
└── docs/
```

---

### Runtime Environment

* Python virtual environment
* Dependencies managed via `.venv`
* Environment variables loaded from `.env`

---

### Process Management

Managed via systemd:

```
alert-webhook.service
```

Behavior:

* Auto-start on boot
* Auto-restart on failure
* Persistent background execution

---

## 📡 Integration Points

### Prometheus Stack

* Receives alerts from Alertmanager via webhook
* Processes monitoring events into notifications

---

### Docker Environment

* Direct interaction with StudexHub containers
* Enables service control and inspection

---

### Telegram Platform

* Input: user commands
* Output: system responses and alerts

---

## 🧠 Design Philosophy

* Minimal complexity, maximum control
* Event-driven architecture
* Human-in-the-loop decision making
* No blind automation
* Clear separation between monitoring and execution

---

## 🚀 Current Status

* Command execution: ✅ Operational
* Alert webhook: ✅ Integrated
* Telegram notifications: ✅ Working
* systemd service: ✅ Deployed
* Security model: ✅ Enforced

---

## 📌 Notes

* Designed to complement monitoring stack, not replace it
* Alertmanager handles alert lifecycle; bot handles delivery and control
* Future extensions may include:

  * command suggestions in alerts
  * runbook integration
  * controlled automation workflows

