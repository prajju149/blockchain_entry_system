# 🔐 Blockchain-Based Entry/Exit Identity System for Flats/Hostels

A comprehensive identity & access control system for residential buildings using **blockchain**, **biometric authentication** (Face + Voice), **QR codes**, and **cryptographic signing**.

**Perfect for:** Flats, Hostels, Student Dormitories, Office Buildings, Gated Communities

---

## 📋 Table of Contents
1. [Features](#-features)
2. [Architecture](#-architecture)
3. [System Components](#-system-components)
4. [Installation](#-installation)
5. [Usage](#-usage)
6. [API Documentation](#-api-documentation)
7. [Blockchain Ledger](#-blockchain-ledger)
8. [Security & Cryptography](#-security--cryptography)
9. [Deployment](#-deployment)
10. [Troubleshooting](#-troubleshooting)

---

## ✨ Features

### 🔑 Multi-Factor Authentication
- **QR Code Scanning** - Fast & contactless entry verification
- **Face Recognition** - Perceptual fingerprinting for visual identity
- **Voice Recognition** - Audio signature for voice-based authentication
- **Hybrid Mode** - Combine any authentication methods

### ⛓️ Blockchain Security
- **Tamper-Evident Ledger** - SHA256 hashing with chain verification
- **HMAC-SHA256 Signing** - Cryptographic signatures on every block
- **Immutable Records** - Entry/exit events permanently recorded
- **Chain Integrity** - Detects any unauthorized modifications

### 📱 Multi-Device Support
- **Web Dashboard** - Modern responsive UI (Desktop/Tablet)
- **Android Mobile** - Live QR scanning with device camera
- **Real-time Updates** - Live resident statistics

### 👥 Resident Management
- **Quick Registration** - Name + Room Number (biometrics optional)
- **Extended Profiles** - Email, phone, address, floor, occupation
- **QR Generation** - Auto-generated per resident
- **Biometric Storage** - Face photo + voice sample support

### 📊 Real-time Analytics
- **Active Residents** - Current in/out count
- **Entry/Exit Timeline** - Complete audit trail
- **Block Statistics** - Blockchain metrics
- **Resident Directory** - Search & filter residents

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Dashboard (Frontend)                 │
│  HTML5 + CSS3 + JavaScript (Responsive, Modern UI)          │
│  - Tab Navigation (Register, Residents, Scan, Ledger)       │
│  - Live QR Scanner (jsQR library)                           │
│  - Real-time Statistics                                     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/HTTP API Calls
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 Flask Backend (REST API)                    │
│  Python 3.x + Flask 2.2.5 + Flask-CORS                     │
│                                                             │
│  Routes:                                                    │
│  ├─ POST /api/register       → Register new resident       │
│  ├─ POST /api/scan           → Entry/exit event            │
│  ├─ GET  /api/residents      → List all residents          │
│  └─ GET  /api/ledger         → Blockchain events           │
└────────────────────────┬────────────────────────────────────┘
                         │ File I/O & Cryptography
                         ↓
┌─────────────────────────────────────────────────────────────┐
│            Storage Layer & Blockchain Engine                │
│                                                             │
│  Components:                                                │
│  ├─ blockchain.py   → Blockchain implementation            │
│  ├─ storage.py      → Resident data persistence            │
│  ├─ utils.py        → Biometric fingerprinting & QR gen   │
│  └─ chain.json      → Immutable ledger file               │
│                                                             │
│  Data Files:                                                │
│  ├─ residents.json              → Resident registry        │
│  └─ server/data/{id}/           → Per-resident files       │
│     ├─ photo.jpg               → Face sample               │
│     └─ voice.wav               → Voice sample              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 System Components

### 1. **Frontend (web/dashboard.html)**
- **Modern UI Design** - Gradient backgrounds, smooth animations
- **Responsive Layout** - Mobile-optimized, works on all devices
- **QR Scanner Tab** - Live camera feed with automatic detection
- **Registration Form** - Collect resident details
- **Residents List** - View all registered residents
- **Blockchain Ledger** - Real-time event display

### 2. **Flask Backend (server/app.py)**
```python
Routes:
- POST /api/register      - Register resident (name, room, biometrics)
- POST /api/scan          - Log entry/exit event to blockchain
- GET  /api/residents     - Fetch all residents
- GET  /api/ledger        - Get blockchain events
```

### 3. **Blockchain Engine (server/blockchain.py)**
```python
Features:
- Block creation with SHA256 hashing
- HMAC-SHA256 cryptographic signing
- Chain verification & integrity checking
- Tamper detection
- JSON persistence
```

### 4. **Storage System (server/storage.py)**
```python
Functions:
- create_resident()        - New resident registration
- get_resident()           - Retrieve resident by ID
- save_resident_photo()    - Store face image
- save_resident_voice()    - Store voice recording
- update_resident()        - Update resident data
- get_all_residents()      - List all residents
```

### 5. **Utilities (server/utils.py)**
```python
Functions:
- image_fingerprint()      - Generate face hash (PIL perceptual)
- audio_fingerprint()      - Generate voice hash (SHA256)
- generate_qr_for_resident() - Create QR code PNG
- ensure_dir()             - Utility directory management
```

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git (optional)

### Step 1: Clone/Download Repository
```bash
git clone <repository-url>
cd blockchain_entry_system
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies included:**
- Flask 2.2.5 - Web framework
- Flask-CORS 4.0.0 - Cross-origin requests
- Pillow 10.0.0 - Image processing
- qrcode 7.3.1 - QR code generation
- python-dotenv - Environment variables

### Step 4: Run Server
```bash
# Windows
run_server.bat

# macOS/Linux
./run_local.sh
```

Server will start on **http://127.0.0.1:5000**

### Step 5: Access Dashboard
Open browser and navigate to:
```
http://127.0.0.1:5000/web/dashboard.html
```

---

## 🚀 Usage

### Register a Resident
1. Go to **"📝 Register Resident"** tab
2. Enter:
   - Full Name (required)
   - Room Number (required)
   - Email (optional)
   - Phone (optional)
   - Address (optional)
   - Floor (optional)
   - Move-in Date (optional)
   - Occupation (optional)
   - Emergency Contact (optional)
3. Click **"Register Resident"**
4. ✅ Success message shows resident details + QR code path

### Scan Entry/Exit Event
#### Method 1: QR Code Scanning
1. Go to **"🔍 Entry/Exit Scan"** tab
2. Click **"📷 Start Camera"**
3. Point camera at resident's QR code
4. Auto-detects and logs entry/exit to blockchain

#### Method 2: Face Recognition
1. Select "Face Recognition" from scan mode
2. Upload resident's photo
3. System compares fingerprints

#### Method 3: Voice Recognition
1. Select "Voice Recognition" from scan mode
2. Upload voice recording
3. System compares voice signatures

### View Residents
1. Go to **"👥 Residents"** tab
2. Click **"Refresh List"**
3. View all registered residents with biometric status

### View Blockchain Ledger
1. Go to **"🔗 Blockchain Ledger"** tab
2. Click **"Load Event Ledger"**
3. See complete entry/exit history with timestamps

---

## 📡 API Documentation

### POST /api/register
**Register a new resident**

```bash
curl -X POST http://127.0.0.1:5000/api/register \
  -F "name=John Doe" \
  -F "room=101" \
  -F "email=john@example.com" \
  -F "phone=9876543210" \
  -F "address=123 Main St" \
  -F "floor=1" \
  -F "moveInDate=2024-01-15" \
  -F "occupation=Engineer" \
  -F "emergencyContact=Jane Doe"
```

**Response:**
```json
{
  "resident": {
    "id": "2955d910-c262-45fb-8b35-6ea81ccd7063",
    "name": "John Doe",
    "room": "101",
    "email": "john@example.com",
    "phone": "9876543210",
    "address": "123 Main St",
    "floor": "1",
    "moveInDate": "2024-01-15",
    "occupation": "Engineer",
    "emergencyContact": "Jane Doe",
    "created": "2024-12-06T10:30:00"
  },
  "qr": "server/data/qrs/2955d910-c262-45fb-8b35-6ea81ccd7063.png"
}
```

### POST /api/scan
**Log entry/exit event**

```bash
curl -X POST http://127.0.0.1:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "qr",
    "qr_data": "2955d910-c262-45fb-8b35-6ea81ccd7063"
  }'
```

**Response:**
```json
{
  "event": {
    "resident_id": "2955d910-c262-45fb-8b35-6ea81ccd7063",
    "resident_name": "John Doe",
    "mode": "qr",
    "timestamp": "2024-12-06T10:35:00",
    "status": "IN"
  },
  "block_index": 42
}
```

### GET /api/residents
**Get all residents**

```bash
curl http://127.0.0.1:5000/api/residents
```

**Response:**
```json
{
  "residents": [
    {
      "id": "2955d910-c262-45fb-8b35-6ea81ccd7063",
      "name": "John Doe",
      "room": "101",
      "email": "john@example.com",
      "phone": "9876543210",
      "address": "123 Main St",
      "floor": "1",
      "moveInDate": "2024-01-15",
      "occupation": "Engineer",
      "emergencyContact": "Jane Doe",
      "created": "2024-12-06T10:30:00"
    }
  ],
  "total": 1
}
```

### GET /api/ledger
**Get blockchain events**

```bash
curl http://127.0.0.1:5000/api/ledger
```

**Response:**
```json
{
  "events": [
    {
      "index": 1,
      "timestamp": "2024-12-06T10:35:00",
      "data": {
        "resident_id": "2955d910-c262-45fb-8b35-6ea81ccd7063",
        "resident_name": "John Doe",
        "room": "101",
        "mode": "qr",
        "status": "IN"
      },
      "hash": "abc123...",
      "prev_hash": "def456...",
      "signature": "ghi789..."
    }
  ]
}
```

---

## ⛓️ Blockchain Ledger

### How It Works

1. **Block Structure**
```python
{
    "index": 1,
    "timestamp": "2024-12-06T10:35:00",
    "data": {...event data...},
    "prev_hash": "hash of previous block",
    "hash": "SHA256(index + timestamp + data + prev_hash)",
    "signature": "HMAC-SHA256 with resident's master key"
}
```

2. **Hashing Algorithm**
```
hash = SHA256(
    str(block['index']) + 
    block['timestamp'] + 
    json(block['data']) + 
    block['prev_hash']
)
```

3. **Cryptographic Signing**
```python
signature = HMAC-SHA256(
    key=resident_master_key,
    message=block_hash
)
```

4. **Chain Verification**
```python
def verify_chain():
    for each block in chain:
        # Check hash integrity
        assert block['hash'] == calculate_hash(block)
        
        # Check signature validity
        assert verify_signature(block['signature'], block['hash'])
        
        # Check chain continuity
        assert block['prev_hash'] == previous_block['hash']
```

### Chain File (chain.json)
```json
{
  "blocks": [
    {
      "index": 0,
      "timestamp": "2024-12-06T10:00:00",
      "data": {"type": "genesis"},
      "prev_hash": "0",
      "hash": "abc123...",
      "signature": "xyz789..."
    },
    {
      "index": 1,
      "timestamp": "2024-12-06T10:35:00",
      "data": {
        "resident_id": "2955d910-c262-45fb-8b35-6ea81ccd7063",
        "resident_name": "John Doe",
        "room": "101",
        "mode": "qr",
        "status": "IN"
      },
      "prev_hash": "abc123...",
      "hash": "def456...",
      "signature": "ghi789..."
    }
  ]
}
```

---

## 🔒 Security & Cryptography

### Encryption & Hashing
| Component | Algorithm | Purpose |
|-----------|-----------|---------|
| Block Hash | SHA256 | Ensure block integrity |
| Signature | HMAC-SHA256 | Authenticate block author |
| Face Fingerprint | Perceptual Hash (PIL) | Biometric matching |
| Voice Fingerprint | SHA256 | Audio signature |
| QR Data | UTF-8 Encoded | Resident ID storage |

### Security Best Practices

1. **Production Deployment**
   - Use HTTPS/TLS for all API communication
   - Implement JWT token authentication
   - Store blockchain signing keys in HSM (Hardware Security Module)
   - Use environment variables for sensitive config

2. **Biometric Security**
   - Face/voice fingerprints are hashes, not actual images
   - Store actual biometric samples in encrypted storage
   - Implement fuzzy matching with threshold tolerance (85-90%)
   - Regular biometric re-enrollment (monthly/quarterly)

3. **Key Management**
   - Use unique master key per resident
   - Rotate signing keys periodically
   - Implement key versioning in blockchain
   - Secure key backup & disaster recovery

4. **Data Privacy**
   - GDPR compliant - residents can request data deletion
   - Encrypt sensitive fields (email, phone, address)
   - Implement role-based access control (RBAC)
   - Audit logging for all API calls

---

## 🌐 Deployment

### Local Development
```bash
python wsgi.py
# or
flask run
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
```

### Cloud Platforms

#### Heroku
```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
```

#### AWS EC2
```bash
# Install Python & dependencies
sudo apt-get install python3 python3-pip
pip install -r requirements.txt

# Use gunicorn + nginx
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

#### Azure App Service
```bash
az webapp up --name your-app-name --runtime "python|3.11"
```

---

## 🐛 Troubleshooting

### Server Won't Start
```
Error: Address already in use
Solution: Change port in app.py or kill process using port 5000
lsof -i :5000  # Find process
kill -9 <PID>  # Kill it
```

### Network Error: "Unexpected token '<'"
```
Cause: Flask returning HTML error page instead of JSON
Solution: Check error logs, ensure utils.py and storage.py are not empty
```

### QR Scanner Not Working
```
Cause: Camera permission denied or unsupported browser
Solution: 
- Use Chrome/Firefox (Safari requires HTTPS)
- Grant camera permissions
- Ensure HTTPS in production
```

### Biometric Match Failing
```
Cause: Threshold too strict or poor sample quality
Solution:
- Adjust fingerprint threshold in utils.py (default 85%)
- Retake photo/voice in better conditions
- Ensure lighting is good for face recognition
```

---

## 📁 Folder Structure

```
blockchain_entry_system/
├── server/                          # Backend
│   ├── __init__.py
│   ├── app.py                      # Flask app + routes
│   ├── blockchain.py               # Blockchain implementation
│   ├── storage.py                  # Resident data management
│   ├── utils.py                    # Utilities (fingerprints, QR)
│   ├── chain.json                  # Blockchain ledger (auto-generated)
│   └── data/                       # Resident storage
│       ├── residents.json          # Resident registry
│       ├── qrs/                    # QR code images
│       │   └── {resident_id}.png
│       └── {resident_id}/          # Per-resident folder
│           ├── photo.jpg           # Face sample
│           └── voice.wav           # Voice sample
│
├── web/                            # Frontend
│   ├── dashboard.html              # Main web UI
│   └── requirements.txt            # Frontend dependencies (CDN-based)
│
├── tools/                          # Utility scripts
│   └── generate_qr.py              # QR generation tool
│
├── wsgi.py                         # WSGI entry point
├── requirements.txt                # Python dependencies
├── run_server.bat                  # Windows launch script
├── run_local.sh                    # Linux/macOS launch script
├── README.md                       # Quick start guide
└── .gitignore                      # Git ignore rules
```

---

## 🔄 Workflow

### Resident Registration Flow
```
User Input
    ↓
[Register Form] → Validate input
    ↓
Create resident ID (UUID)
    ↓
Generate QR code → Save as PNG
    ↓
[Optional] Process photo → Face fingerprint
    ↓
[Optional] Process voice → Voice fingerprint
    ↓
Save to residents.json
    ↓
Return success with resident details
```

### Entry/Exit Scan Flow
```
QR Scan / Face Upload / Voice Upload
    ↓
Extract resident ID
    ↓
Lookup resident in registry
    ↓
Verify biometric (if applicable)
    ↓
Toggle resident status (IN/OUT)
    ↓
Create blockchain block with event
    ↓
Sign block with HMAC-SHA256
    ↓
Append to chain.json
    ↓
Return confirmation to dashboard
```

---

## 📊 Sample Data

### residents.json
```json
{
  "residents": [
    {
      "id": "2955d910-c262-45fb-8b35-6ea81ccd7063",
      "name": "John Doe",
      "room": "101",
      "email": "john@example.com",
      "phone": "9876543210",
      "address": "123 Main Street",
      "floor": "1",
      "moveInDate": "2024-01-15",
      "occupation": "Software Engineer",
      "emergencyContact": "Jane Doe",
      "created": "2024-12-06T10:30:00",
      "status": "IN"
    }
  ]
}
```

---

## 🎯 Future Enhancements

- [ ] Siri voice command integration (iOS)
- [ ] Google Assistant integration (Android)
- [ ] Facial recognition with ML (TensorFlow)
- [ ] Advanced voice authentication (speaker verification)
- [ ] Mobile app (React Native)
- [ ] Database (PostgreSQL) instead of JSON
- [ ] Real-time notifications (Firebase)
- [ ] Advanced analytics & reports
- [ ] Multi-building support
- [ ] Integration with building management systems

---

## 📄 License

MIT License - Free for educational and commercial use

---

## 👥 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Submit pull request

---

## 📧 Support & Contact

For issues, questions, or feature requests:
- Open GitHub issue
- Email: support@example.com
- Documentation: See README.md

---

**Made with ❤️ for secure building access management**
