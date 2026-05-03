# Resend Verification Email Feature

## Overview
Users who registered but haven't verified their email will see a "Resend verification link" option when they try to login.

## How It Works

### Step 1: User Registers
1. Go to http://localhost:3000
2. Click "Sign up" or toggle to registration
3. Register with email, username, and password
4. User is shown "Check Your Email" message

### Step 2: User Tries to Login Without Verifying
1. User goes back to login page
2. Enters email and password
3. Clicks "Sign in"
4. **Error message appears:** "Please verify your email before logging in"
5. **Below the error, a clickable link appears:** "Cannot receive the email? Resend verification link"

### Step 3: User Clicks Resend Link
1. Click "Cannot receive the email? Resend verification link"
2. System sends a new verification email
3. User is redirected to "Check Your Email" page
4. Check backend logs for the verification link (Development Mode)

### Step 4: Verify Email
1. Check backend logs: `docker logs portfolio_backend --tail 50`
2. Look for the verification URL:
   ```
   ================================================================================
   EMAIL VERIFICATION LINK (Development Mode - SMTP Failed)
   ================================================================================
   To: user@example.com
   Verification URL: http://localhost:3000/verify-email?token=...
   ================================================================================
   ```
3. Copy and paste the URL into browser
4. Account is now verified
5. User can login successfully

## UI/UX Features

### Error Display with Resend Link
When login fails due to unverified email:
```
┌─────────────────────────────────────────────────────┐
│ ⚠️ Please verify your email before logging in      │
│                                                     │
│ Cannot receive the email? Resend verification link │
│ (clickable link in indigo color)                   │
└─────────────────────────────────────────────────────┘
```

### Loading States
- Button shows spinner while resending
- Button is disabled during the process
- Prevents multiple clicks

### Success Flow
After clicking resend:
1. Loading spinner appears
2. Request is sent to backend
3. New verification email is generated
4. User sees "Check Your Email" confirmation page
5. Link is printed to backend logs (Development Mode)

## Testing

### Test Scenario 1: Unverified User Login
```bash
# 1. Register a new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Test123!@#"}'

# 2. Try to login without verifying
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'

# Expected: {"detail":"Please verify your email before logging in"}
```

### Test Scenario 2: Resend Verification
```bash
# Resend verification email
curl -X POST "http://localhost:8000/auth/resend-verification?email=test@example.com" \
  -H "Content-Type: application/json"

# Expected: {"message":"Verification email sent"}

# Check logs for verification link
docker logs portfolio_backend --tail 30
```

### Test Scenario 3: Verify and Login
```bash
# 1. Get verification token from logs
# 2. Visit: http://localhost:3000/verify-email?token=YOUR_TOKEN
# 3. Try login again
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'

# Expected: {"access_token":"...","token_type":"bearer"}
```

## API Endpoints

### POST /auth/resend-verification
**Query Parameters:**
- `email` (required): Email address to resend verification to

**Response:**
```json
{
  "message": "Verification email sent"
}
```

**Error Responses:**
- `404`: User not found
- `400`: Email already verified

## Frontend Implementation

### State Management
```typescript
const [showResendLink, setShowResendLink] = useState(false);
const [unverifiedEmail, setUnverifiedEmail] = useState('');
```

### Error Detection
```typescript
if (errorDetail.includes('verify your email')) {
  setShowResendLink(true);
  setUnverifiedEmail(formData.email);
}
```

### Resend Handler
```typescript
const handleResendVerification = async () => {
  await authAPI.resendVerification(unverifiedEmail);
  setShowVerificationMessage(true);
};
```

## Security Considerations

1. **Rate Limiting**: Consider adding rate limiting to prevent abuse
2. **Token Expiry**: Verification tokens expire after 1 hour
3. **Email Validation**: Only registered emails can request resend
4. **Already Verified**: Returns error if email is already verified

## Future Enhancements

1. Add rate limiting (max 3 resends per hour)
2. Show countdown timer before allowing another resend
3. Add email delivery status tracking
4. Implement email queue for better reliability
5. Add notification when verification is successful
