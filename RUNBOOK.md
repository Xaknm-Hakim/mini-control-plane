# mini-control-plane RUNBOOK

## 📌 Overview

This runbook defines operational procedures for managing, debugging, and recovering the **mini-control-plane**.

The focus is on:

* bot availability
* command execution reliability
* system integrations (systemd, Docker, filesystem)
* permission issues

---

## 🧠 System Context

mini-control-plane is a **systemd-managed Telegram bot** that:

* receives admin commands
* executes system-level operations
* interacts with:

  * system services (nginx, cloudflared)
  * Docker containers
  * filesystem (logs, backups)

---

## 🚨 Incident Classification

| Level | Description                   |
| ----- | ----------------------------- |
| Low   | Minor issue, partial function |
| Med   | Some commands failing         |
| High  | Bot not responding at all     |

---

## 🔍 Basic Health Check

### Step 1: Check Bot Responsiveness

Send:

```text
/ping
```

If no response → proceed to system checks

---

### Step 2: Check Service Status

```bash
systemctl status mini-control-plane
```

Check:

* active (running / failed)
* recent logs

---

## ⚠️ Common Incidents

---

## 1. 🤖 Bot Not Responding

### Symptoms

* no reply from any command
* Telegram bot appears offline

---

### Diagnosis

```bash
systemctl status mini-control-plane
```

---

### Resolution

```bash
sudo systemctl restart mini-control-plane
```

Then verify:

```bash
journalctl -u mini-control-plane -f
```

---

## 2. ❌ Bot Fails to Start

### Symptoms

* service shows `failed`
* restart does not fix

---

### Diagnosis

```bash
journalctl -u mini-control-plane -n 50
```

Look for:

* Python errors
* missing environment variables
* import errors

---

### Common Causes

#### Missing Virtual Environment

* `.venv` not activated properly in systemd

#### Missing Environment Variables

* token or config not loaded

#### Code Error

* syntax / runtime error in bot

---

### Resolution

Fix root cause, then:

```bash
sudo systemctl restart mini-control-plane
```

---

## 3. 🔐 Permission Denied Errors

### Symptoms

* `PermissionError` in logs
* bot cannot:

  * write logs
  * access Docker
  * read files

---

### Diagnosis

Check logs:

```bash
journalctl -u mini-control-plane
```

---

### Common Cases

#### A. Log File Permission

Error:

```text
Permission denied: logs/bot.log
```

Fix:

```bash
sudo chown -R prod-node:studexhub /opt/bot/mini-control-plane
sudo chmod -R 2775 /opt/bot/mini-control-plane
```

---

#### B. Docker Permission

Error:

```text
permission denied while accessing docker
```

Fix:

```bash
sudo usermod -aG docker bot-runner
```

Then restart session/service:

```bash
sudo systemctl restart mini-control-plane
```

---

#### C. Group Access Issues

Ensure:

```bash
groups bot-runner
```

Includes:

```text
studexhub docker
```

---

## 4. ⚙️ Command Execution Failure

### Symptoms

* command responds with error
* partial output
* timeout or no result

---

### Diagnosis

Check logs:

```bash
journalctl -u mini-control-plane -f
```

---

### Possible Causes

* service not available (nginx/docker down)
* command execution error
* incorrect path or environment

---

### Resolution

* verify target service manually
* retry command
* check service layer implementation

---

## 5. 📂 Logging Issues

### Symptoms

* no logs generated
* log file not updating

---

### Diagnosis

Check:

```bash
ls -l /opt/bot/mini-control-plane/logs
```

---

### Resolution

```bash
sudo chown -R prod-node:studexhub logs
sudo chmod -R 2775 logs
```

---

## 6. 🔄 Restart Procedure

### Safe Restart

```bash
sudo systemctl restart mini-control-plane
```

---

### Verify

```bash
systemctl status mini-control-plane
journalctl -u mini-control-plane -f
```

---

## 📊 Logs & Debugging

### Live Logs

```bash
journalctl -u mini-control-plane -f
```

---

### Recent Logs

```bash
journalctl -u mini-control-plane -n 100
```

---

## ⚠️ Safety Rules

* Always check logs before acting
* Do not blindly restart repeatedly
* Fix root cause, not symptoms
* Ensure permissions are correct before retrying
* Validate system state after recovery

---

## 🚀 Future Improvements

* automatic alerting when bot goes down
* command timeout handling
* retry mechanisms for failed operations
* health check automation

---

## 🏁 Conclusion

This runbook ensures that the mini-control-plane can be:

* reliably operated
* safely debugged
* quickly recovered during failures

---

