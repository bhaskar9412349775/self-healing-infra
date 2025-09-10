# Self-Healing Infrastructure with Prometheus, Alertmanager & Ansible

## Objective
Automatically detect service failures (like Nginx down or CPU > 90%) and auto-recover using Prometheus alerts, Alertmanager, a custom webhook, and Ansible playbooks.

---

## Tools Used
- Prometheus (monitoring)
- Alertmanager (alert routing)
- Node Exporter (system metrics)
- Blackbox Exporter (service probing)
- Ansible (auto-healing actions)
- Flask (webhook receiver)

---

## Setup
1. Prometheus monitors Nginx & system metrics.
2. Alert rules fire when:
   - Nginx is down
   - CPU > 90% for 5 minutes
3. Alerts sent to Alertmanager → webhook → Ansible playbooks.

---

## Project Structure
```bash
self-healing-infra/
│── prometheus.yml
│── alertmanager.yml
│── webhook.py
│── rules/alerts.yml
│── playbooks/
│     ├── inventory.ini
│     ├── heal_nginx.yml
│     └── mitigate_cpu.yml
```
---

## Demo
- Stopping Nginx → triggers alert → Ansible auto-restarts it.
- Running stress-ng → triggers high CPU alert → Ansible kills stress process.

## Screenshots Available

---

# THANK YOU!
