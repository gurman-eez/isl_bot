# Railway Deployment Quick Checklist

Use this checklist before deploying to Railway.app.

## Pre-Deployment

- [ ] Bot token obtained from @BotFather
- [ ] Railway account created at railway.app
- [ ] Code committed to Git (all changes)

## Configuration Files (Verify)

- [ ] `railway.json` exists at project root
- [ ] `.python-version` exists at project root (contains: 3.13.2)
- [ ] `prayer_times_bot/requirements.txt` has pinned versions
- [ ] `prayer_times_bot/.env.example` exists (for reference)
- [ ] `.gitignore` includes `.env` and `bot.log`
- [ ] `.dockerignore` created

## Railway Setup

- [ ] Project created in Railway dashboard
- [ ] GitHub repository connected (or Railway CLI initialized)
- [ ] Environment variable `BOT_TOKEN` set in Railway Variables tab
- [ ] Deployment started (automatic after repo connection)

## Post-Deployment Verification

- [ ] Deployment status shows "Active" (green)
- [ ] Logs show "Bot is starting polling..."
- [ ] Logs show "Listening for updates. Press Ctrl+C to stop."
- [ ] No error messages in logs

## Functional Testing

- [ ] Bot responds to `/start` command
- [ ] Location sharing button appears
- [ ] Sending GPS location returns prayer times
- [ ] City selection menu works
- [ ] Selecting city returns prayer times
- [ ] Times formatted in monospace with emojis
- [ ] Times match islamicfinder.org (±1 minute)

## Production Readiness

- [ ] Bot token secured (not in repository)
- [ ] Logging working (visible in Railway dashboard)
- [ ] Restart policy configured (ON_FAILURE)
- [ ] No sensitive data logged
- [ ] Bot handles errors gracefully

## Optional (Recommended)

- [ ] Enable auto-deploy on Git push in Railway settings
- [ ] Set up billing alerts in Railway account
- [ ] Document bot commands for users
- [ ] Test with multiple users simultaneously
- [ ] Monitor resource usage for first 24 hours

## Emergency Rollback

If deployment fails:
1. Check logs in Railway dashboard
2. Verify `BOT_TOKEN` environment variable
3. Use Railway CLI: `railway logs`
4. Rollback to previous deployment in Railway UI
5. Test locally: `cd prayer_times_bot && python bot.py`

## Support

- Full guide: `DEPLOYMENT.md`
- Railway docs: docs.railway.app
- Project issues: [Your GitHub issues URL]
