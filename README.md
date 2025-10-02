
**A simple, educational IoT honeypot written in Python.**  
This project provides a lightweight honeypot that listens on common IoT/network ports (Telnet-like, SSH-like, HTTP), presents simple banners, and logs all incoming connections and payloads. It's designed for learning, research, and small lab deployments — **not** for offensive use.

---

## Quick Summary
- **Purpose:** Capture and log attacker behavior against emulated IoT services for study and defensive improvements.
- **Language:** Python 3 (standard library only)
- **Primary files:** `honeypot.py`, `.gitignore`, `README.md`
- **Logs:** Saved to `logs/` (ignored by git)
- **Recommended environment:** Local VM (Kali/Ubuntu) or isolated Raspberry Pi in a lab network

---

## Tools & Technologies Used
- **Python 3** — core language/runtime for the honeypot
- **Git** — version control for code backup and collaboration
- **VS Code** — recommended editor (remote development supported)
- **tmux / systemd** — optional, for background execution
- **Docker** — optional, containerized deployment for isolation
- **Ngrok / Port forwarding** — optional, expose honeypot to the internet (use with caution)
- **GitHub** — remote repository hosting

---

## Safety & Legal Notice
- Only run this honeypot in an isolated lab network or on machines you own
- Do NOT deploy on networks with sensitive resources
- Logs may contain malicious payloads — treat as untrusted
- Do not use captured credentials/payloads to attack other systems
- Ensure compliance with local laws and institutional policies

---

