# Blockchain-Based Entry/Exit Identity System (MVP)

This prototype tracks entry/exit using QR + Face + Voice and writes events to a tamper-evident file-backed blockchain.

## Quick Start (Local)
1. Create and activate venv:
   ```bash
   python3 -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
2. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python wsgi.py
   ```
4. Open: http://127.0.0.1:5000/

## Deploy to Production
See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for automatic GitHub Actions → Heroku deployment.

Or check [DEPLOYMENT.md](DEPLOYMENT.md) for Docker, AWS, Azure, and self-hosted options.

## Features
- ✅ QR code generation & live scanning (browser camera)
- ✅ Biometric fingerprinting (image hash, audio hash)
- ✅ Blockchain ledger with SHA256 + HMAC-SHA256 signatures
- ✅ Flask REST API + Single-page dashboard
- ✅ File-backed JSON storage (residents, chain, QR codes)
- ✅ CORS enabled for mobile/web clients

## Notes
- Face/voice are fingerprint stubs (hashes). Replace with ML models for production.
- Use HTTPS and secure key management for production.
- See START_HERE.md for a guided tour of the codebase.

