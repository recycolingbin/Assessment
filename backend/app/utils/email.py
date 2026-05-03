import os
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "noreply@portfolioiq.com")

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_verification_token(email: str) -> str:
    """Generate a verification token for email"""
    return serializer.dumps(email, salt='email-verification')

def generate_reset_token(email: str) -> str:
    """Generate a password reset token"""
    return serializer.dumps(email, salt='password-reset')

def verify_token(token: str, max_age: int = 3600) -> str:
    """Verify the token and return the email. Token expires after max_age seconds (default 1 hour)"""
    try:
        email = serializer.loads(token, salt='email-verification', max_age=max_age)
        return email
    except Exception:
        return None

def verify_reset_token(token: str, max_age: int = 3600) -> str:
    """Verify the password reset token and return the email"""
    try:
        email = serializer.loads(token, salt='password-reset', max_age=max_age)
        return email
    except Exception:
        return None

def send_verification_email(email: str, token: str):
    """Send verification email to user"""
    verification_url = f"{FRONTEND_URL}/verify-email?token={token}"

    subject = "Verify Your PortfolioIQ Account"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #1e293b;
                margin: 0;
                padding: 0;
                background-color: #f8fafc;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            }}
            .header {{
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
                letter-spacing: -0.5px;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .content h2 {{
                color: #0f172a;
                font-size: 20px;
                font-weight: 600;
                margin: 0 0 20px 0;
            }}
            .content p {{
                color: #475569;
                font-size: 15px;
                line-height: 1.7;
                margin: 0 0 20px 0;
            }}
            .button-container {{
                text-align: center;
                margin: 35px 0;
            }}
            .button {{
                display: inline-block;
                padding: 14px 40px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 15px;
                transition: background 0.2s;
            }}
            .button:hover {{
                background: #2563eb;
            }}
            .link-box {{
                background: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 16px;
                margin: 25px 0;
                word-break: break-all;
            }}
            .link-box p {{
                margin: 0 0 8px 0;
                font-size: 13px;
                color: #64748b;
                font-weight: 500;
            }}
            .link-box a {{
                color: #3b82f6;
                font-size: 13px;
                text-decoration: none;
            }}
            .footer {{
                background: #f8fafc;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            .footer p {{
                color: #64748b;
                font-size: 13px;
                margin: 5px 0;
            }}
            .security-note {{
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 16px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            .security-note p {{
                margin: 0;
                color: #92400e;
                font-size: 14px;
            }}
            .security-note strong {{
                color: #78350f;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>PortfolioIQ</h1>
            </div>
            <div class="content">
                <h2>Welcome to PortfolioIQ</h2>
                <p>Thank you for creating your account. To ensure the security of your portfolio and complete your registration, please verify your email address.</p>

                <div class="button-container">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </div>

                <div class="link-box">
                    <p>Or copy and paste this link into your browser:</p>
                    <a href="{verification_url}">{verification_url}</a>
                </div>

                <div class="security-note">
                    <p><strong>Security Notice:</strong> This verification link will expire in 1 hour for your protection. If you didn't create an account with PortfolioIQ, please disregard this email.</p>
                </div>

                <p style="margin-top: 30px;">If you have any questions or need assistance, please don't hesitate to contact our support team.</p>

                <p style="margin-top: 25px; color: #64748b; font-size: 14px;">Best regards,<br><strong style="color: #1e293b;">The PortfolioIQ Team</strong></p>
            </div>
            <div class="footer">
                <p>&copy; {datetime.now().year} PortfolioIQ. All rights reserved.</p>
                <p>Professional Portfolio Management Platform</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Send email via SMTP
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"PortfolioIQ <{SMTP_FROM}>"
        msg['To'] = email

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Use SMTP_SSL for port 465, SMTP with STARTTLS for port 587
        if SMTP_PORT == 465:
            # Port 465 uses SSL from the start
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                server.set_debuglevel(0)
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            # Port 587 uses STARTTLS
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                server.set_debuglevel(0)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)

        print(f"✓ Verification email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"✗ Error sending verification email: {e}")
        # Log the verification URL for development/debugging
        print(f"\n{'='*80}")
        print(f"EMAIL VERIFICATION LINK (SMTP Failed - Check Logs)")
        print(f"{'='*80}")
        print(f"To: {email}")
        print(f"Verification URL: {verification_url}")
        print(f"{'='*80}\n")
        raise Exception(f"Failed to send verification email: {str(e)}")

def send_password_reset_email(email: str, token: str):
    """Send password reset email to user"""
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"

    subject = "Reset Your PortfolioIQ Password"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #1e293b;
                margin: 0;
                padding: 0;
                background-color: #f8fafc;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            }}
            .header {{
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
                letter-spacing: -0.5px;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .content h2 {{
                color: #0f172a;
                font-size: 20px;
                font-weight: 600;
                margin: 0 0 20px 0;
            }}
            .content p {{
                color: #475569;
                font-size: 15px;
                line-height: 1.7;
                margin: 0 0 20px 0;
            }}
            .button-container {{
                text-align: center;
                margin: 35px 0;
            }}
            .button {{
                display: inline-block;
                padding: 14px 40px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 15px;
                transition: background 0.2s;
            }}
            .button:hover {{
                background: #2563eb;
            }}
            .link-box {{
                background: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 16px;
                margin: 25px 0;
                word-break: break-all;
            }}
            .link-box p {{
                margin: 0 0 8px 0;
                font-size: 13px;
                color: #64748b;
                font-weight: 500;
            }}
            .link-box a {{
                color: #3b82f6;
                font-size: 13px;
                text-decoration: none;
            }}
            .footer {{
                background: #f8fafc;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            .footer p {{
                color: #64748b;
                font-size: 13px;
                margin: 5px 0;
            }}
            .warning {{
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 16px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            .warning p {{
                margin: 0;
                color: #92400e;
                font-size: 14px;
            }}
            .warning strong {{
                color: #78350f;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>PortfolioIQ</h1>
            </div>
            <div class="content">
                <h2>Password Reset Request</h2>
                <p>We received a request to reset the password for your PortfolioIQ account. To proceed with resetting your password, please click the button below:</p>

                <div class="button-container">
                    <a href="{reset_url}" class="button">Reset Password</a>
                </div>

                <div class="link-box">
                    <p>Or copy and paste this link into your browser:</p>
                    <a href="{reset_url}">{reset_url}</a>
                </div>

                <div class="warning">
                    <p><strong>Security Notice:</strong> This password reset link will expire in 1 hour for your protection. If you didn't request a password reset, please ignore this email and your password will remain unchanged. We recommend reviewing your account security if you receive this email unexpectedly.</p>
                </div>

                <p style="margin-top: 30px;">For security reasons, we never ask for your password via email. If you have any concerns about your account security, please contact our support team immediately.</p>

                <p style="margin-top: 25px; color: #64748b; font-size: 14px;">Best regards,<br><strong style="color: #1e293b;">The PortfolioIQ Team</strong></p>
            </div>
            <div class="footer">
                <p>&copy; {datetime.now().year} PortfolioIQ. All rights reserved.</p>
                <p>Professional Portfolio Management Platform</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Send email via SMTP
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"PortfolioIQ <{SMTP_FROM}>"
        msg['To'] = email

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Use SMTP_SSL for port 465, SMTP with STARTTLS for port 587
        if SMTP_PORT == 465:
            # Port 465 uses SSL from the start
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                server.set_debuglevel(0)
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            # Port 587 uses STARTTLS
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                server.set_debuglevel(0)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)

        print(f"✓ Password reset email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"✗ Error sending password reset email: {e}")
        # Log the reset URL for development/debugging
        print(f"\n{'='*80}")
        print(f"PASSWORD RESET LINK (SMTP Failed - Check Logs)")
        print(f"{'='*80}")
        print(f"To: {email}")
        print(f"Subject: Reset Password Request")
        print(f"Message: Someone has requested a link to change your password, and you can do this through the link below.")
        print(f"If you didn't request this, please ignore this email. Your password won't change until you access the link below and create a new one.")
        print(f"Note: This link will expire in 1 hour. If you didn't request this, please ignore this email.")
        print(f"Reset URL: {reset_url}")
        print(f"{'='*80}\n")
        raise Exception(f"Failed to send password reset email: {str(e)}")
