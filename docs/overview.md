# StudexHub Mini Control Plane (Bot)

## 📅 Last Updated
9 April 2026 (MYT)

---

## 🧠 Overview

This system-level Telegram bot acts as the operational control plane for StudexHub infrastructure.

It provides:
- System monitoring commands
- Service control actions
- Backup operations
- Alert intake via webhook

---

## 🏗️ Architecture

Alert Flow:
Prometheus → Alertmanager → Webhook → Bot → Telegram

Control Flow:
User → Telegram → Bot → System / Docker

---

## ⚙️ Core Features

### Monitoring Commands
- /host_status
- /service_status

### Control Commands
- /studexhub_restart
- /studexhub_backup

### Utility
- /ping
- /help

---

## 🚨 Alert Integration

Webhook endpoint:
