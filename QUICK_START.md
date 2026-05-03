# Quick Start Guide

## ✅ All Features Are Now Live!

Your application is running with all the new features:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Database**: PostgreSQL on port 5432
- **Redis**: Redis on port 6379

## 🎉 What's New

### 1. **Profile Settings** 
   - Access via "Profile" button in dashboard
   - Edit username, full name, phone number
   - Change password securely

### 2. **Email Verification**
   - New users must verify their email
   - Verification links printed to backend console (development mode)
   - Check `docker logs portfolio_backend` to see verification links

### 3. **Enhanced Password Security**
   - Real-time password strength indicator
   - Must include: 8+ chars, uppercase, lowercase, number, special character
   - Visual checklist shows requirements

### 4. **Google OAuth Login**
   - "Continue with Google" button on login page
   - **Note**: Requires Google OAuth setup (see below)

### 5. **Passkey Login**
   - "Sign in with Passkey" button on login page
   - Biometric authentication (fingerprint, Face ID, etc.)
   - Works on localhost for development

## 🚀 Testing the Features

### Test Email Verification (No Setup Required)
1. Go to http://localhost:3000/login
2. Click "Don't have an account? Sign up"
3. Register with:
   - Email: test@example.com
   - Username: testuser
   - Password: Test123!@# (meets all requirements)
4. After registration, check backend logs for verification link:
   ```bash
   docker logs portfolio_backend | grep "Verification URL"
   ```
5. Copy the verification URL and paste it in your browser
6. Login with your credentials

### Test Password Validation
1. Try registering with weak passwords
2. Watch the password strength indicator change colors
3. See the checklist update as you type

### Test Profile Settings
1. Login to dashboard
2. Click "Profile" button
3. Update your information
4. Try changing your password

### Test Passkey Login (Advanced)
1. Login with regular credentials
2. Go to Profile settings
3. Look for passkey registration option (coming soon - needs additional UI)
4. For now, passkey endpoints are ready in the backend

## 🔧 Optional: Setup Google OAuth

If you want to test Google OAuth:

1. **Get Google OAuth Credentials:**
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add authorized origin: `http://localhost:3000`

2. **Update Frontend Environment:**
   Edit `frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   ```

3. **Update Backend Environment:**
   Create `backend/.env`:
   ```
   DATABASE_URL=postgresql://portfolio_user:portfolio_pass@postgres:5432/portfolio
   REDIS_URL=redis://redis:6379
   SECRET_KEY=your-secret-key-change-in-production
   FRONTEND_URL=http://localhost:3000
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

4. **Restart containers:**
   ```bash
   docker-compose restart backend frontend
   ```

## 📧 Optional: Setup Email Sending

To send actual verification emails (instead of console output):

1. **For Gmail:**
   - Enable 2FA on your Google account
   - Generate App Password: https://support.google.com/accounts/answer/185833

2. **Update Backend `.env`:**
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=465
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SMTP_FROM=noreply@portfolioiq.com
   ```

3. **Restart backend:**
   ```bash
   docker-compose restart backend
   ```

## 🛠️ Useful Commands

```bash
# View all container logs
docker-compose logs -f

# View backend logs only
docker logs portfolio_backend -f

# View frontend logs only
docker logs portfolio_frontend -f

# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Start all services
docker-compose up -d

# Rebuild and start (after code changes)
docker-compose up -d --build
```

## 🎨 UI/UX Improvements

The dashboard now features:
- Professional banking-grade design
- Elegant color scheme (navy, slate, blue)
- Comprehensive accessibility features:
  - ARIA labels and roles
  - Keyboard navigation
  - Screen reader support
  - Skip-to-content link
  - Focus indicators
  - Semantic HTML
- Responsive design for all screen sizes
- Smooth transitions and hover effects
- Professional icons and visual hierarchy

## 📝 API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

New endpoints:
- `POST /auth/register` - Register with email verification
- `POST /auth/verify-email` - Verify email
- `POST /auth/google` - Google OAuth login
- `GET /auth/me` - Get current user
- `PUT /auth/me` - Update profile
- `POST /auth/passkey/*` - Passkey endpoints

## 🐛 Troubleshooting

**Can't login after registration?**
- Check backend logs for verification link
- Verify your email before logging in

**Google OAuth not working?**
- Make sure you've set up OAuth credentials
- Check that Client ID is in both frontend and backend configs

**Password validation errors?**
- Ensure password has: 8+ chars, uppercase, lowercase, number, special char

**Database errors?**
- Migration already completed ✅
- If issues persist: `docker-compose down -v && docker-compose up -d`

## 🎯 Next Steps

1. Test all the new features
2. Optionally set up Google OAuth
3. Optionally configure email sending
4. Customize the design to your preferences
5. Add more features as needed!

Enjoy your enhanced PortfolioIQ application! 🚀
