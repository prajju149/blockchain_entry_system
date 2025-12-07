# 🚀 Deployment Guide - Production Ready

Complete guide for deploying the Blockchain Entry/Exit System to production environments.

---

## Table of Contents
1. [GitHub Actions Deployment](#github-actions-deployment)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Azure Deployment](#azure-deployment)
6. [Heroku Deployment](#heroku-deployment)
7. [Self-Hosted (Linux)](#self-hosted-linux)
8. [Security Checklist](#security-checklist)
9. [Monitoring & Maintenance](#monitoring--maintenance)

---

## GitHub Actions Deployment

Automatic deployment to Heroku on every push to `main` or `master` branch.

### Prerequisites
- GitHub repository created and pushed
- Heroku account (free or paid)
- Heroku app created

### Step 1: Create Heroku App
```bash
heroku login
heroku create your-app-name
```

### Step 2: Add GitHub Secrets
Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:
| Secret Name | Value | How to Get |
|---|---|---|
| `HEROKU_API_KEY` | Your Heroku API key | `heroku auth:token` in terminal |
| `HEROKU_APP_NAME` | Your app name | From `heroku create` output |
| `HEROKU_EMAIL` | Your Heroku email | Your Heroku account email |

### Step 3: Push to GitHub
```bash
git add .
git commit -m "Add GitHub Actions deployment"
git push origin main
```

### Step 4: Monitor Deployment
- Go to **GitHub Repository** → **Actions**
- Watch the **Deploy to Heroku** workflow run
- Check logs for any errors
- Once complete, visit `https://your-app-name.herokuapp.com`

### Troubleshooting

**Deployment fails with "Procfile not found"**
- Ensure `Procfile` is in repository root
- Check: `git ls-files | grep Procfile`

**Build fails with missing dependencies**
- Update `requirements.txt`: `pip freeze > requirements.txt`
- Commit and push again

**App crashes after deploy**
- Check Heroku logs: `heroku logs --tail`
- Verify environment variables: `heroku config`

---

## Local Development Setup

### Prerequisites
- Python 3.8+
- pip & virtualenv
- Git

### Installation

```bash
# Clone repository
git clone <repo-url>
cd blockchain_entry_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python wsgi.py
```

Server runs on: **http://127.0.0.1:5000**

### Environment Variables (Development)
Create `.env` file:
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
CORS_ORIGINS=*
DATABASE_URL=sqlite:///app.db
LOG_LEVEL=DEBUG
```

---

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]
```

### docker-compose.yml (Single Container)
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
    volumes:
      - ./server/data:/app/server/data
      - ./logs:/app/logs
    restart: unless-stopped
```

### Build & Run
```bash
# Build image
docker build -t blockchain-entry-system:latest .

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/server/data:/app/server/data \
  blockchain-entry-system:latest

# Or use docker-compose
docker-compose up -d
```

---

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

#### Step 1: Initialize EB
```bash
pip install awsebcli

eb init -p python-3.11 blockchain-entry-system \
  --region us-east-1

eb create prod-env --instance-type t3.micro
```

#### Step 2: Create .ebextensions/python.config
```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:elasticbeanstalk:container:python:
    WSGIPath: wsgi:app
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.micro
    SecurityGroups: default
```

#### Step 3: Deploy
```bash
# Create RDS database
aws rds create-db-instance \
  --db-instance-identifier blockchain-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password 'YourPassword123!'

# Deploy to Elastic Beanstalk
eb deploy

# Open application
eb open
```

### Option 2: AWS EC2 + RDS

#### Step 1: Launch EC2 Instance
```bash
# Using AWS CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name your-key-pair \
  --security-groups allow-http-https
```

#### Step 2: Connect & Setup
```bash
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y

# Install Python & dependencies
sudo yum install -y python3 python3-pip git
sudo yum groupinstall -y "Development Tools"

# Clone repository
git clone <repo-url>
cd blockchain_entry_system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/blockchain-app.service
```

#### systemd Service File
```ini
[Unit]
Description=Blockchain Entry/Exit System
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/blockchain_entry_system
Environment="PATH=/home/ec2-user/blockchain_entry_system/venv/bin"
ExecStart=/home/ec2-user/blockchain_entry_system/venv/bin/gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --timeout 120 \
  wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Step 3: Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl start blockchain-app
sudo systemctl enable blockchain-app
sudo systemctl status blockchain-app
```

#### Step 4: Setup Nginx
```bash
sudo yum install -y nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/blockchain
```

#### Nginx Config
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files cache
    location /static/ {
        alias /var/www/blockchain-entry-system/static/;
        expires 30d;
    }
}
```

#### Step 5: Enable & Start Nginx
```bash
sudo systemctl start nginx
sudo systemctl enable nginx

# Test configuration
sudo nginx -t
```

---

## Azure Deployment

### Option 1: Azure App Service

#### Step 1: Create App Service
```bash
# Using Azure CLI
az group create --name blockchain-rg --location eastus

az appservice plan create \
  --name blockchain-plan \
  --resource-group blockchain-rg \
  --sku B1 \
  --is-linux

az webapp create \
  --name blockchain-app \
  --resource-group blockchain-rg \
  --plan blockchain-plan \
  --runtime "PYTHON:3.11"
```

#### Step 2: Deploy from Git
```bash
az webapp deployment user set \
  --user-name <username> \
  --password <password>

# Configure local deployment
git remote add azure <git-clone-url>

# Deploy
git push azure main
```

#### Step 3: Configure App Settings
```bash
az webapp config appsettings set \
  --resource-group blockchain-rg \
  --name blockchain-app \
  --settings \
    FLASK_ENV=production \
    SECRET_KEY="your-secret-key" \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    WEBSITES_PORT=5000
```

### Option 2: Azure Container Instances

```bash
# Build and push Docker image
az acr create \
  --resource-group blockchain-rg \
  --name blockchainregistry \
  --sku Basic

az acr build \
  --registry blockchainregistry \
  --image blockchain-app:latest .

# Deploy container
az container create \
  --resource-group blockchain-rg \
  --name blockchain-app \
  --image blockchainregistry.azurecr.io/blockchain-app:latest \
  --cpu 1 \
  --memory 1 \
  --registry-login-server blockchainregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 80 \
  --environment-variables FLASK_ENV=production \
  --dns-name-label blockchain-app
```

---

## Heroku Deployment

### Step 1: Prepare Repository
Create `Procfile`:
```
web: gunicorn wsgi:app
release: python manage.py db upgrade
```

Create `runtime.txt`:
```
python-3.11.0
```

### Step 2: Login & Deploy
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create application
heroku create blockchain-entry-system

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY="your-secret-key"

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open application
heroku open
```

### Step 3: Add PostgreSQL (Optional)
```bash
# Add PostgreSQL add-on (free tier)
heroku addons:create heroku-postgresql:hobby-dev

# Migration will run automatically via Procfile release phase
```

---

## Self-Hosted (Linux)

### Prerequisites
- Ubuntu 20.04 LTS or later
- Root/sudo access
- Domain name (optional, for HTTPS)

### Step 1: System Setup
```bash
#!/bin/bash
set -e

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    git \
    nginx \
    curl \
    wget \
    build-essential

# Create application user
sudo useradd -m -s /bin/bash -d /var/www blockchain-app || true
```

### Step 2: Install Application
```bash
# Switch to app user
sudo su - blockchain-app

# Clone repository
git clone <repo-url> app
cd app

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Exit back to root
exit
```

### Step 3: Create Systemd Service
```bash
sudo tee /etc/systemd/system/blockchain-app.service > /dev/null <<EOF
[Unit]
Description=Blockchain Entry/Exit System
After=network.target

[Service]
Type=notify
User=blockchain-app
WorkingDirectory=/var/www/app
Environment="PATH=/var/www/app/venv/bin"
EnvironmentFile=/var/www/app/.env
ExecStart=/var/www/app/venv/bin/gunicorn \
    --bind unix:/tmp/blockchain-app.sock \
    --workers 4 \
    --timeout 120 \
    --access-logfile /var/log/blockchain-app/access.log \
    --error-logfile /var/log/blockchain-app/error.log \
    wsgi:app

Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
sudo mkdir -p /var/log/blockchain-app
sudo chown blockchain-app:blockchain-app /var/log/blockchain-app

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable blockchain-app
sudo systemctl start blockchain-app
```

### Step 4: Setup Nginx
```bash
# Create nginx configuration
sudo tee /etc/nginx/sites-available/blockchain-app > /dev/null <<EOF
upstream app {
    server unix:/tmp/blockchain-app.sock fail_timeout=0;
}

server {
    listen 80;
    server_name _;
    client_max_body_size 20M;

    location / {
        proxy_pass http://app;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /var/www/app/static/;
        expires 30d;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/blockchain-app \
    /etc/nginx/sites-enabled/blockchain-app

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart nginx
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Setup SSL/TLS (Using Certbot)
```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Update Nginx config
sudo nano /etc/nginx/sites-available/blockchain-app

# Add to server block:
# listen 443 ssl;
# ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

# Redirect HTTP to HTTPS
# server {
#     listen 80;
#     server_name yourdomain.com;
#     return 301 https://$server_name$request_uri;
# }

sudo systemctl reload nginx

# Setup auto-renewal
sudo systemctl enable certbot.timer
```

---

## Security Checklist

### Before Production Deployment

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Enable HTTPS/SSL/TLS
- [ ] Configure CORS properly (whitelist domains)
- [ ] Setup database backups (automated daily)
- [ ] Enable application logging
- [ ] Setup error monitoring (Sentry, New Relic)
- [ ] Implement rate limiting on API endpoints
- [ ] Setup Web Application Firewall (WAF)
- [ ] Configure security headers:
  ```python
  app.config['SESSION_COOKIE_SECURE'] = True
  app.config['SESSION_COOKIE_HTTPONLY'] = True
  app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
  ```
- [ ] Setup database encryption
- [ ] Rotate cryptographic keys regularly
- [ ] Implement audit logging
- [ ] Setup DDoS protection
- [ ] Regular security updates (weekly)
- [ ] Penetration testing (quarterly)

---

## Monitoring & Maintenance

### Application Monitoring

```python
# Add to app.py for health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'blockchain_blocks': len(blockchain.chain),
        'residents_count': len(storage.get_all_residents())
    }), 200
```

### Monitoring Tools

1. **Sentry** (Error tracking)
```bash
pip install sentry-sdk
```

2. **New Relic** (Performance monitoring)
```bash
pip install newrelic
newrelic-admin run-program gunicorn wsgi:app
```

3. **Datadog** (Infrastructure monitoring)
```bash
pip install datadog
```

### Backup Strategy

```bash
#!/bin/bash
# Backup script (daily via cron)

DATE=$(date +%Y-%m-%d-%H%M%S)
BACKUP_DIR="/backups/blockchain-app"

mkdir -p $BACKUP_DIR

# Backup data
tar -czf $BACKUP_DIR/data-$DATE.tar.gz \
    /var/www/app/server/data

# Backup database
if [ -f /var/www/app/app.db ]; then
    cp /var/www/app/app.db $BACKUP_DIR/app-$DATE.db
fi

# Upload to S3
aws s3 cp $BACKUP_DIR s3://my-backup-bucket/ --recursive

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Cron Job
```bash
# Add to crontab
0 2 * * * /var/www/app/scripts/backup.sh
```

---

## Troubleshooting Deployment

### Application Won't Start
```bash
# Check systemd status
sudo systemctl status blockchain-app

# View systemd journal
sudo journalctl -u blockchain-app -n 50

# Check for port conflicts
sudo lsof -i :5000

# Check permissions
sudo chown -R blockchain-app:blockchain-app /var/www/app
```

### High CPU/Memory Usage
```bash
# Monitor resources
top -u blockchain-app

# Check gunicorn workers
ps aux | grep gunicorn

# Adjust worker count in systemd service
# Edit /etc/systemd/system/blockchain-app.service
# Change --workers parameter
```

### Database Connection Issues
```bash
# Test database connection
psql -h localhost -U username -d dbname -c "SELECT 1;"

# Check database logs
tail -f /var/log/postgresql/postgresql.log
```

---

## Scaling Guide

### Horizontal Scaling (Multiple Servers)

1. **Load Balancer Setup**
   - Use Nginx/HAProxy
   - Round-robin across multiple app servers
   - Session persistence (sticky sessions)

2. **Shared Database**
   - Migrate from JSON to PostgreSQL
   - Setup database replication
   - Configure connection pooling

3. **Distributed Cache**
   - Setup Redis for caching
   - Session storage in Redis
   - Blockchain block caching

### Vertical Scaling (Bigger Server)

- Upgrade EC2/VPS instance size
- Increase gunicorn workers
- Increase database connections
- Add more RAM for caching

### Capacity Planning

| Residents | Daily Scans | Recommended | Infrastructure |
|-----------|-------------|-------------|-----------------|
| 10-100 | 50-500 | t3.micro | 1x 512MB RAM |
| 100-1000 | 500-5000 | t3.small | 1x 2GB RAM |
| 1000-10000 | 5000-50000 | t3.medium | 2x 4GB RAM + Load Balancer |
| 10000+ | 50000+ | t3.large+ | 3x+ 8GB RAM + DB Cluster |

---

**Deployment Complete! 🎉**

For support: [support@example.com](mailto:support@example.com)
