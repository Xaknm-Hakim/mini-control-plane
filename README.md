# mini-control-plane

A lightweight Telegram-based control plane for managing and observing the StudexHub infrastructure.

---

## 📌 Overview

`mini-control-plane` is a system-level operations bot designed to:

* Monitor host and service health
* Execute controlled operational actions (restart, backup, notices)
* Provide a secure interface for infrastructure management via Telegram

This bot is intentionally **decoupled from the StudexHub application layer**, forming a separate **ops layer** in the system architecture.

---

## 🧠 Architecture Role

The system is structured into three layers:

* **App Layer** → StudexHub (Next.js + PostgreSQL)
* **Ops Layer** → mini-control-plane (this project)
* **Infra Layer** → Docker, systemd, Nginx, Cloudflare Tunnel

This bot operates at the **Ops Layer**, acting as a bridge between the administrator and the infrastructure.

---

## ⚙️ Key Features

### System Monitoring

* `/host_status` → CPU, RAM, disk usage
* `/system_services` → Docker, Nginx, Cloudflare Tunnel, containers
* `/full_status` → Combined system overview

### StudexHub Operations

* `/studexhub_restart` → Safe restart with confirmation
* `/studexhub_backup` → Database backup via `pg_dump`
* `/studexhub_invite` → Generate invite codes
* `/studexhub_templates` → List notice templates
* `/studexhub_notice` → Send system-wide email notices

### Safety Mechanisms

* Admin-only access
* Confirmation system for destructive actions
* Structured logging for all actions

---

## 🔐 Security Model

* Bot access restricted to a single admin ID
* Critical commands require explicit confirmation (`YES`)
* Runs under a dedicated low-privilege system user (`bot-runner`)
* Uses shared group (`studexhub`) for controlled access to resources

---

## 🧱 Deployment

The bot runs as a **systemd service**, not inside Docker.

### Service

```bash
sudo systemctl status mini-control-plane
```

### Restart

```bash
sudo systemctl restart mini-control-plane
```

---

## 📁 Project Structure

```text
src/
├── services/        # system + StudexHub operations
├── formatters/      # output formatting
├── logging_setup.py
├── confirmations.py
├── config.py
└── main.py
```

---

## 🧪 Usage

Example:

```text
/full_status
```

Returns:

* Host system metrics
* Service health
* Container status

---

## 📊 Design Principles

* **Separation of concerns** — app vs ops vs infra
* **Minimal surface area** — only essential commands
* **Operational safety first** — confirmations + logging
* **CLI-first mindset** — reproducible and debuggable

---

## 🚀 Future Improvements

* Alerting system (auto Telegram notifications)
* Scheduled health checks (cron integration)
* Metrics aggregation (Prometheus / Grafana)
* Auto-healing workflows

---

## 🏁 Status

Actively used in production for managing StudexHub infrastructure.

---

