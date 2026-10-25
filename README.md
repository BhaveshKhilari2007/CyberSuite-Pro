# ⚡ CyberSuite Pro | Advanced Security Toolkit

> An enterprise-grade, modular cybersecurity assessment suite and network diagnostic workbench built in Python.

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-orange.svg)

---

## 🚀 Overview
**CyberSuite Pro** is a comprehensive desktop cybersecurity utility designed to assist security analysts, network administrators, and students in performing rapid local security audits, threat heuristic checks, and system diagnostics through an intuitive, dark-themed cyberpunk interface.

---

## 🛠️ Key Modules & Features

| Module | Description |
| :--- | :--- |
| **🔒 NetBlocker** | System firewall manager that reroutes malicious domains to local loopback (`127.0.0.1`) via OS host files. |
| **📧 Email Analyzer** | Parses structural integrity, user entropy, and TLD validity of email addresses. |
| **📱 Scam SMS Detector** | Heuristic linguistic analyzer calculating smishing risk scores and detecting phishing keywords. |
| **🛡️ PhishGuard** | Deep domain scanner detecting typosquatting, raw IP usage, and malicious URL structures. |
| **🔐 PasswordChecker** | Cryptographic key entropy auditor measuring password strength and complexity. |
| **🛡️ Port Scanner** | Asynchronous multi-threaded TCP socket scanner for local infrastructure probes. |
| **📄 File Hasher** | Computes cryptographic forensic hashes (MD5, SHA-1, SHA-256) for file integrity checks. |
| **🌐 SubRecon** | DNS topology mapping and subdomain enumeration engine. |
| **🔑 CryptoXOR** | Symmetric XOR encryption/decryption framework utilizing SHA-256 keys and Base64 encoding. |
| **📋 Audit Logs** | Centralized SQLite database telemetry viewer tracking forensic events across all modules. |

---

## ⚙️ Installation & Setup Guide

To run CyberSuite Pro locally on your machine, follow these simple steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/CyberSuite-Pro.git](https://github.com/YOUR-USERNAME/CyberSuite-Pro.git)
   cd CyberSuite-Pro