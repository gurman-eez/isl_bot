# Prayer Times Bot - Railway Deployment Quick Start

**5-Minute Deployment Guide**

---

## Prerequisites

Get these ready before starting:

1. **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
2. **Railway Account** at [railway.app](https://railway.app) (free)
3. **GitHub Account** with your code pushed

---

## Deployment Steps

### 1. Railway Setup (2 minutes)

```bash
# Visit railway.app/new
# Click "Deploy from GitHub repo"
# Select: PythonProject
# Wait for auto-detection (Python project)
```

### 2. Environment Variables (1 minute)

```bash
# In Railway dashboard:
# 1. Click "Variables" tab
# 2. Add new variable:
#    Name: BOT_TOKEN
#    Value: <paste your token from BotFather>
# 3. Click "Add"
```

### 3. Deploy (1 minute)

```bash
# Railway auto-deploys on repo connection
# Watch "Deployments" tab for "Active" status
# Check logs for: "Bot is starting polling..."
```

### 4. Test (1 minute)

```bash
# Open Telegram
# Find your bot (search by username)
# Send: /start
# Expected: Welcome message with buttons
# Click "Поделиться локацией" → Share location
# Expected: Prayer times in monospace format
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `railway.json` | Railway configuration |
| `.python-version` | Python 3.13.2 |
| `prayer_times_bot/requirements.txt` | Dependencies |
| `prayer_times_bot/.env.example` | Env template |

---

## Common Issues

### Bot not responding?
```bash
# Check Railway logs:
# Deployments → Click active → View logs
# Look for errors after "Bot is starting polling..."
```

### "BOT_TOKEN not found"?
```bash
# Railway dashboard → Variables
# Ensure BOT_TOKEN is set (no quotes)
# Redeploy if just added
```

### Wrong prayer times?
```bash
# Verify calculation method:
# config.py → CALCULATION_METHOD = 3 (MWL)
# Compare with islamicfinder.org (Muslim World League)
```

---

## Railway CLI (Alternative)

```bash
# Install
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Deploy
cd /Users/admin/PycharmProjects/PythonProject
railway init
railway variables set BOT_TOKEN="your_token_here"
railway up

# View logs
railway logs --follow
```

---

## Project Structure

```
PythonProject/
├── railway.json              ← Railway config
├── .python-version           ← Python 3.13.2
│
└── prayer_times_bot/
    ├── bot.py                ← Entry point
    ├── requirements.txt      ← Dependencies
    ├── .env.example          ← Env template
    └── config.py             ← Bot settings
```

---

## Full Documentation

- **Comprehensive Guide**: `DEPLOYMENT.md` (14 KB)
- **Pre-flight Checklist**: `RAILWAY_CHECKLIST.md`
- **Technical Details**: `DEPLOYMENT_SUMMARY.md`

---

## Support

- Railway docs: [docs.railway.app](https://docs.railway.app)
- aiogram docs: [docs.aiogram.dev](https://docs.aiogram.dev)
- AlAdhan API: [aladhan.com/prayer-times-api](https://aladhan.com/prayer-times-api)

---

## Expected Resource Usage

- **RAM**: 50-80 MB
- **CPU**: < 5%
- **Cost**: Free tier ($5 credit/month)
- **Uptime**: 24/7

---

**Total Deployment Time**: 5 minutes
**Difficulty**: Easy
**Cost**: Free (Railway free tier)
