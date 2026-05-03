# Email Sending Troubleshooting Guide

## Current Issue
The application is configured to send emails via Gmail SMTP, but Docker containers are experiencing connection timeouts when trying to reach Gmail's SMTP server (`smtp.gmail.com:465`).

**Error:** `SMTP error sending email: Connection unexpectedly closed: timed out`

## Why This Happens
1. **Docker Network Isolation**: Docker containers may have restricted network access
2. **Gmail Security**: Gmail may block connections from Docker containers or unfamiliar IPs
3. **Firewall/Network**: Your network or firewall may be blocking outbound SMTP connections

## Solutions

### Option 1: Use Development Mode (Current Default)
When SMTP credentials are not working, the app automatically falls back to **Development Mode**, which prints email links to the console instead of sending actual emails.

**How to use:**
1. Check the backend logs: `docker logs portfolio_backend --tail 50`
2. Look for sections like:
   ```
   ================================================================================
   EMAIL VERIFICATION LINK (Development Mode)
   ================================================================================
   To: user@example.com
   Verification URL: http://localhost:3000/verify-email?token=...
   ================================================================================
   ```
3. Copy the verification URL and paste it in your browser

**This is the recommended approach for local development and testing.**

### Option 2: Fix Gmail SMTP Connection

#### Step 1: Verify Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Generate a new App Password for "Mail"
3. Update the password in `docker-compose.yml` under `SMTP_PASSWORD`

#### Step 2: Test SMTP Connection from Host
```bash
# Test if your host machine can reach Gmail SMTP
telnet smtp.gmail.com 465
# or
nc -zv smtp.gmail.com 465
```

If this fails, your network is blocking SMTP connections.

#### Step 3: Allow Docker Container Network Access
Add to `docker-compose.yml` under the backend service:
```yaml
backend:
  network_mode: "host"  # Use host network instead of bridge
```

**Note:** This removes network isolation and may not work on all systems.

### Option 3: Use a Different SMTP Provider

Some SMTP providers work better with Docker:

#### Mailgun (Recommended for Production)
```yaml
SMTP_HOST: smtp.mailgun.org
SMTP_PORT: 465
SMTP_USER: postmaster@your-domain.mailgun.org
SMTP_PASSWORD: your-mailgun-password
```

#### SendGrid
```yaml
SMTP_HOST: smtp.sendgrid.net
SMTP_PORT: 465
SMTP_USER: apikey
SMTP_PASSWORD: your-sendgrid-api-key
```

#### Mailtrap (Best for Development/Testing)
```yaml
SMTP_HOST: smtp.mailtrap.io
SMTP_PORT: 2525
SMTP_USER: your-mailtrap-username
SMTP_PASSWORD: your-mailtrap-password
```

### Option 4: Run Backend Outside Docker
If you need to test actual email sending:

1. Stop the backend container:
   ```bash
   docker-compose stop backend
   ```

2. Run backend directly on your host:
   ```bash
   cd backend
   pip install -r requirements.txt
   export DATABASE_URL=postgresql://portfolio_user:portfolio_pass@localhost:5432/portfolio
   export REDIS_URL=redis://localhost:6379
   # ... copy other env vars from docker-compose.yml
   uvicorn app.main:app --reload
   ```

3. The backend running on your host machine will have better network access to Gmail SMTP.

## Current Configuration

The app is configured with:
- **SMTP Host:** smtp.gmail.com
- **SMTP Port:** 465
- **SMTP User:** 2026webapp.test@gmail.com
- **Timeout:** 10 seconds
- **Fallback:** Development mode (prints to console)

## Verification

To verify emails are working:

1. **Check logs for success:**
   ```bash
   docker logs portfolio_backend 2>&1 | grep "email sent successfully"
   ```

2. **Check logs for errors:**
   ```bash
   docker logs portfolio_backend 2>&1 | grep "SMTP error"
   ```

3. **Test registration:**
   - Register a new user at http://localhost:3000
   - Check backend logs for the verification link
   - Copy and paste the link to verify the account

## Recommended Approach for Development

**Use Development Mode** - it's faster, doesn't require external services, and works reliably:

1. Register a user
2. Check backend logs: `docker logs portfolio_backend --tail 50`
3. Copy the verification URL from the logs
4. Paste it in your browser to verify

This is how most developers test email functionality locally before deploying to production with real SMTP.
