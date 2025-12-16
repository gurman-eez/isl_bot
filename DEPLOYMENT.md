# Prayer Times Bot - Railway.app Deployment Guide

This guide provides step-by-step instructions for deploying the Prayer Times Telegram Bot to Railway.app.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Overview](#project-overview)
- [Railway Configuration](#railway-configuration)
- [Deployment Steps](#deployment-steps)
- [Environment Variables](#environment-variables)
- [Monitoring and Logs](#monitoring-and-logs)
- [Troubleshooting](#troubleshooting)
- [Post-Deployment Testing](#post-deployment-testing)

---

## Prerequisites

Before deploying, ensure you have:

1. **Telegram Bot Token**
   - Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
   - Save the token (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Railway Account**
   - Sign up at [railway.app](https://railway.app)
   - Free tier includes $5/month credit (sufficient for this bot)

3. **Git Repository**
   - Your code pushed to GitHub/GitLab/Bitbucket
   - Or use Railway CLI for local deployment

---

## Project Overview

**Bot Architecture:**
- **Type**: Long-polling Telegram bot (no webhooks)
- **Framework**: aiogram 3.x (async)
- **Language**: Python 3.13.2
- **API**: AlAdhan API for prayer times
- **Database**: None (stateless)

**Key Features:**
- Russian language interface
- Muslim World League calculation method
- Support for 10 major Polish cities
- Location-based prayer times
- Monospace-formatted schedules

---

## Railway Configuration

The project includes the following Railway configuration files:

### 1. `railway.json` (Project Root)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r prayer_times_bot/requirements.txt"
  },
  "deploy": {
    "startCommand": "cd prayer_times_bot && python -u bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Configuration Explanation:**

- **`builder: "NIXPACKS"`**: Railway's default builder (auto-detects Python)
- **`buildCommand`**: Installs dependencies from subdirectory
- **`startCommand`**:
  - `cd prayer_times_bot`: Navigate to bot directory
  - `python -u bot.py`: Run bot with unbuffered output (real-time logs)
- **`restartPolicyType: "ON_FAILURE"`**: Auto-restart if bot crashes
- **`restartPolicyMaxRetries: 10`**: Maximum restart attempts

### 2. `.python-version` (Project Root)

```
3.13.2
```

Forces Railway to use Python 3.13.2 (matches local development).

### 3. `requirements.txt` (prayer_times_bot/)

```
aiogram==3.23.0        # Telegram Bot Framework
aiohttp==3.13.2        # HTTP Client
python-dotenv==1.2.1   # Environment variables
pytz==2025.2           # Timezone handling
```

All dependencies pinned for reproducible builds.

---

## Deployment Steps

### Option A: Deploy from GitHub (Recommended)

1. **Push Code to GitHub**

   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Create Railway Project**

   - Go to [railway.app/new](https://railway.app/new)
   - Click **"Deploy from GitHub repo"**
   - Select your repository
   - Railway will auto-detect Python and use `railway.json` config

3. **Configure Environment Variables**

   - Go to your project → **Variables** tab
   - Add the following variable:

   | Variable Name | Value | Description |
   |--------------|-------|-------------|
   | `BOT_TOKEN` | `your_bot_token_here` | From @BotFather |

   - Click **"Add"** to save

4. **Deploy**

   - Railway will automatically build and deploy
   - Wait for **"Success"** status in deployments tab
   - Check logs to verify bot started successfully

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**

   ```bash
   # macOS/Linux
   curl -fsSL https://railway.app/install.sh | sh

   # Or via npm
   npm i -g @railway/cli
   ```

2. **Login to Railway**

   ```bash
   railway login
   ```

3. **Initialize Project**

   ```bash
   cd /Users/admin/PycharmProjects/PythonProject
   railway init
   ```

4. **Set Environment Variables**

   ```bash
   railway variables set BOT_TOKEN="your_bot_token_here"
   ```

5. **Deploy**

   ```bash
   railway up
   ```

6. **View Logs**

   ```bash
   railway logs
   ```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | `1234567890:ABC...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALADHAN_API_URL` | AlAdhan API base URL | `https://api.aladhan.com/v1` |

**Setting Variables in Railway:**

1. Go to your project dashboard
2. Click **"Variables"** tab
3. Click **"+ New Variable"**
4. Enter name and value
5. Click **"Add"**

**Variables are encrypted and injected at runtime.**

---

## Monitoring and Logs

### Viewing Logs

**Railway Dashboard:**
1. Go to your project
2. Click **"Deployments"** tab
3. Click on the active deployment
4. View real-time logs in the **"Logs"** panel

**Railway CLI:**
```bash
railway logs
railway logs --follow  # Stream logs
```

### Log Output Example

```
2025-12-16 14:30:15 - __main__ - INFO - Starting Prayer Times Bot...
2025-12-16 14:30:15 - __main__ - INFO - Python version: 3.13.2
2025-12-16 14:30:15 - __main__ - INFO - Running in production mode with long-polling
2025-12-16 14:30:15 - __main__ - INFO - Routers registered successfully
2025-12-16 14:30:15 - __main__ - INFO - Bot is starting polling...
2025-12-16 14:30:15 - __main__ - INFO - Listening for updates. Press Ctrl+C to stop.
```

### Health Monitoring

Railway automatically monitors your service:
- **Restart on Failure**: Bot restarts automatically if it crashes (up to 10 times)
- **Resource Usage**: Monitor CPU/RAM in Railway dashboard
- **Uptime**: View deployment history and uptime metrics

---

## Troubleshooting

### Issue: Bot Not Starting

**Error:** `BOT_TOKEN not found in environment variables!`

**Solution:**
1. Check Variables tab in Railway dashboard
2. Ensure `BOT_TOKEN` is set (no quotes needed)
3. Redeploy after adding variable

---

### Issue: Import Errors

**Error:** `ModuleNotFoundError: No module named 'aiogram'`

**Solution:**
1. Verify `requirements.txt` exists in `prayer_times_bot/` directory
2. Check `buildCommand` in `railway.json` points to correct path
3. Redeploy to rebuild dependencies

---

### Issue: Bot Crashes Repeatedly

**Error:** Deployment shows "Crashed" status

**Solution:**
1. Check logs for error messages
2. Common causes:
   - Invalid bot token (check with @BotFather)
   - Network issues with Telegram API
   - AlAdhan API unavailable
3. Verify token with local test:
   ```bash
   cd prayer_times_bot
   python -c "from config import BOT_TOKEN; print(BOT_TOKEN[:10])"
   ```

---

### Issue: Logs Not Updating

**Error:** Old logs displayed

**Solution:**
1. Click refresh icon in Railway logs panel
2. Use Railway CLI: `railway logs --follow`
3. Check deployment is "Active" (green status)

---

### Issue: Bot Responds Slowly

**Cause:** Railway free tier resources

**Solution:**
- Railway free tier provides sufficient resources for low-traffic bots
- Upgrade to Hobby plan ($5/month) for guaranteed resources
- Optimize code (already implemented):
  - Async API calls with `aiohttp`
  - Efficient long-polling with `aiogram`

---

## Post-Deployment Testing

### 1. Verify Bot is Online

Open Telegram and send commands to your bot:

```
/start
```

**Expected Response:** Welcome message with location sharing button

---

### 2. Test Location-Based Prayer Times

1. Send `/start`
2. Click **"Поделиться локацией"** (Share location)
3. Share your GPS coordinates

**Expected Response:** Prayer times formatted in monospace with emojis

---

### 3. Test City Selection

1. Click **"Выбрать город"** (Select city)
2. Choose a Polish city (e.g., "Warszawa")

**Expected Response:** Prayer times for selected city

---

### 4. Verify Calculation Accuracy

Compare bot output with [islamicfinder.org](https://islamicfinder.org):
1. Select same location
2. Choose "Muslim World League" method
3. Times should match within ±1 minute

---

## Railway Platform Features

### Automatic Deployments

- **Auto-deploy on Git push**: Enable in Railway settings
- **Branch deployments**: Deploy staging/production from different branches
- **Rollback**: Revert to previous deployment with one click

### Custom Domains (Hobby Plan)

This bot uses long-polling (no public HTTP endpoint), but if you migrate to webhooks:
1. Add custom domain in Railway settings
2. Update webhook URL in bot code
3. SSL/HTTPS handled automatically by Railway

### Resource Scaling

**Current Configuration:**
- Free tier: $5 credit/month (~500 hours uptime)
- RAM: 512MB (sufficient for this bot)
- CPU: Shared

**Upgrade Path:**
- Hobby plan: $5/month (guaranteed resources)
- Supports up to 10,000+ users with current architecture

---

## Maintenance

### Updating Dependencies

1. Update `requirements.txt` versions
2. Test locally
3. Push to GitHub
4. Railway auto-deploys

### Monitoring Costs

- Check [Railway dashboard](https://railway.app/account/usage) for usage
- Free tier resets monthly
- Set up billing alerts in account settings

### Backup Strategy

This bot is stateless (no database), but backup:
- Bot configuration (`config.py`)
- Bot token (save securely)
- Environment variables (document in team wiki)

---

## Security Best Practices

1. **Never commit `.env` file**
   - Use `.env.example` as template
   - Store secrets in Railway Variables

2. **Bot Token Security**
   - Rotate token if leaked (via @BotFather)
   - Never share token in public repositories

3. **API Rate Limiting**
   - AlAdhan API has no documented rate limits
   - Bot implements efficient caching per request

4. **User Privacy**
   - Location data not stored
   - Logs contain user IDs only (for rate limiting)
   - Complies with GDPR (no persistent user data)

---

## Support and Resources

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **aiogram Documentation**: [docs.aiogram.dev](https://docs.aiogram.dev)
- **AlAdhan API**: [aladhan.com/prayer-times-api](https://aladhan.com/prayer-times-api)
- **Project Repository**: [Your GitHub URL]

---

## Deployment Checklist

Before going live, verify:

- [ ] Bot token obtained from @BotFather
- [ ] Railway account created
- [ ] Code pushed to GitHub
- [ ] `railway.json` configured
- [ ] `.python-version` set to 3.13.2
- [ ] `requirements.txt` dependencies pinned
- [ ] `BOT_TOKEN` environment variable set in Railway
- [ ] Deployment successful (green status)
- [ ] Logs show "Bot is starting polling..."
- [ ] `/start` command responds
- [ ] Location sharing works
- [ ] City selection works
- [ ] Prayer times match islamicfinder.org

---

## Railway Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Railway.app Cloud                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │  Prayer Times Bot Container                 │        │
│  │                                              │        │
│  │  ┌──────────────────────────────┐           │        │
│  │  │  Python 3.13.2 Runtime       │           │        │
│  │  │                               │           │        │
│  │  │  ┌────────────────────────┐  │           │        │
│  │  │  │  bot.py                │  │           │        │
│  │  │  │  (Long-polling)        │  │           │        │
│  │  │  └────────────────────────┘  │           │        │
│  │  └──────────────────────────────┘           │        │
│  │                                              │        │
│  │  Environment Variables:                     │        │
│  │  - BOT_TOKEN                                │        │
│  │                                              │        │
│  └─────────────────────────────────────────────┘        │
│                   ↕                                      │
│            (Long-polling)                                │
│                   ↕                                      │
└───────────────────┼───────────────────────────────────────┘
                    ↕
         ┌──────────┴──────────┐
         │                     │
         │  Telegram API       │
         │  (api.telegram.org) │
         │                     │
         └─────────────────────┘
                    ↕
         ┌──────────┴──────────┐
         │                     │
         │  Users              │
         │  (Telegram Clients) │
         │                     │
         └─────────────────────┘

External API:
┌─────────────────────┐
│  AlAdhan API        │
│  (aladhan.com)      │
│  - Prayer times     │
│  - No auth required │
└─────────────────────┘
        ↑
        │ (HTTPS requests)
        │
   [Bot queries]
```

---

## License

This bot serves Muslim users seeking to fulfill their religious obligations with accuracy and ease. May it be beneficial to the ummah.

---

**Deployment Date**: 2025-12-16
**Railway Platform Version**: Current (Nixpacks)
**Python Version**: 3.13.2
**aiogram Version**: 3.23.0
