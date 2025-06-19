# 🔐 Ethical Keylogger Educational Project

> A comprehensive exploration of keylogging for **educational and ethical research purposes only** — featuring secure logging, encrypted data transmission, and web-based data management.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web--Server-000000?style=flat-square&logo=flask)
![Status](https://img.shields.io/badge/Status-Educational--Use--Only-orange?style=flat-square)

---

## 🚀 Overview

This project offers a hands-on educational demonstration of a **Python-based keylogger** integrated with a **Flask web server**. It covers ethical usage, legal implications, and detection & defense techniques — all for learning cybersecurity.

---

## ⚠️ Disclaimer

> **This project is strictly for educational and ethical use only. Unauthorized usage is illegal and unethical. Always obtain explicit written consent before monitoring any system.**

---

## 📁 Features

### 🧠 Keylogger (`keylogger.py`)
- Tracks **keystrokes**, **mouse clicks**, and **cursor movement**
- AES-256 **encrypted log storage**
- Auto-upload to a secure Flask server
- Runs in background and exits cleanly with `Esc` key

### 🌐 Server (`server.py`)
- Web interface (Flask-based) for:
  - Session listing
  - Viewing & downloading encrypted logs
  - Password-protected access
- Stores each session in **timestamped folders**
- Session-based **ZIP downloads** with included `decryptor.py`

### 📄 Whitepaper
- In-depth PDF and Markdown whitepaper covering:
  - Legal frameworks (GDPR, CCPA, HIPAA)
  - Ethical guidelines and use cases
  - Keylogger misuse case studies

### 🧑‍🏫 Presentation
- 10-slide educational deck for academic/corporate training
- Topics: keylogging concepts, detection, defenses

---

## 🛠 Installation

### 📦 Prerequisites

```bash
pip install pynput cryptography flask pillow requests
```

---

## 🧪 How to Use

### 🔴 Start Keylogger

```bash
python3 keylogger.py
```

- Automatically starts the server if not already running
- Uploads logs periodically or on triggers (e.g., Ctrl+S, ESC)
- Clean exit with `Esc` key (also forces data upload)

### 🌐 Start Server Manually (Optional)

```bash
python3 server.py
```

### 🔐 Access Web Dashboard

1. Open browser: `http://127.0.0.1:5000`
2. Login:
   - **Username**: `admin`
   - **Password**: `password123`
3. View sessions, download logs or ZIP archives, decrypt files with included script.

---

## 📚 Legal & Ethical Guidelines

✅ Acceptable:
- Academic use with consent  
- Cybersecurity training  
- Personal systems  

❌ Prohibited:
- Monitoring without consent  
- Malicious use (spying, corporate espionage)  
- Use on others' devices or networks  

⚖️ You **must** comply with:
- Consent laws  
- Local data privacy regulations  
- Institutional or organizational policies  

---

## 📂 Project Structure

```
keylogger_project/
├── keylogger.py
├── server.py
├── decryptor.py
├── whitepaper.md / whitepaper_updated.pdf
├── presentation/
├── todo.md
└── README.md
```

---

## 🎯 Educational Goals

- Learn how keyloggers operate (tech perspective)
- Understand threats and how attackers bypass detection
- Practice secure data handling and encryption
- Explore legal frameworks and ethical boundaries

---

## 🧑‍💻 Contributing

We welcome educational collaboration. Please:
- Follow laws & institutional policies
- Use only in ethical testing environments
- Suggest improvements via Issues or Pull Requests

---

## 📬 Contact

This project is open for learning and research purposes only.  
**No support for unethical usage.**

> “With great power comes great responsibility.” — Use your knowledge to secure, not exploit.

---

## 📘 License

This project is distributed for educational purposes. Not intended for production or commercial use.
