# GitHub Deployment Quick Start

## What's Ready
✅ GitHub Actions workflow (`.github/workflows/deploy.yml`)
✅ Procfile for Heroku
✅ Python runtime.txt
✅ Updated requirements.txt with gunicorn

## Steps to Deploy

### 1. Create Heroku Account & App
```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
heroku create my-blockchain-app
```

### 2. Add GitHub Secrets
Go to your GitHub repo → **Settings → Secrets and variables → Actions**

Click **New repository secret** and add:
- `HEROKU_API_KEY`: Run `heroku auth:token` in terminal
- `HEROKU_APP_NAME`: Use the app name from Heroku (e.g., `my-blockchain-app`)
- `HEROKU_EMAIL`: Your Heroku email

### 3. Push to GitHub
```bash
git add .
git commit -m "Setup GitHub Actions deployment"
git push origin main
```
*(or `master` if that's your default branch)*

### 4. Watch Deployment
- Go to **Actions** tab in GitHub
- Click the latest **Deploy to Heroku** workflow
- Wait for ✅ all steps to complete
- Visit `https://my-blockchain-app.herokuapp.com`

### 5. Verify App Works
```bash
curl https://my-blockchain-app.herokuapp.com/
# Should return HTML dashboard or JSON response
```

---

## Environment Variables (Optional)
If you need to set config vars on Heroku:
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
```

---

## File Structure
```
.github/
  workflows/
    deploy.yml          ← GitHub Actions workflow
Procfile              ← Heroku process definition
runtime.txt           ← Python version
requirements.txt      ← Dependencies (includes gunicorn)
wsgi.py              ← Flask app entry point
server/
  app.py              ← Flask application
```

---

## Common Issues

**"Procfile not found"**
- Commit Procfile: `git add Procfile && git commit -m "Add Procfile"`

**"Secret not provided"**
- Go to repo Settings → Secrets → verify all 3 secrets are added

**"Build timeout"**
- Check for large files; may need to gitignore them

**"Port binding error"**
- Heroku sets PORT env var automatically; `wsgi.py` should handle this

---

## Next: Monitor & Scale
```bash
# View real-time logs
heroku logs --tail

# Check app status
heroku ps

# Scale dynos if needed (may cost)
heroku ps:scale web=1
```

Enjoy your deployment! 🚀
