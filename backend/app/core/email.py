"""Email service for sending verification and reset emails using Gmail"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from typing import Optional

# Gmail SMTP configuration
GMAIL_USER = "sreenilay0909@gmail.com"
GMAIL_APP_PASSWORD = "keoypyainkaxvnpl"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email: str, subject: str, html_content: str):
    """Send email using Gmail SMTP"""
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.FROM_NAME} <{GMAIL_USER}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(message)
        
        print(f"[EMAIL] Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL] Failed to send email: {e}")
        raise

async def send_verification_email(to_email: str, name: str, code: str):
    """Send email verification code"""
    
    print(f"[EMAIL] Sending verification code to {to_email}")
    print(f"[EMAIL] Verification code: {code}")
    
    subject = "Verify Your ElevateAI Account"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify Your Email</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        <!-- Header with gradient -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); padding: 40px 40px 30px 40px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">
                                    🚀 ElevateAI
                                </h1>
                                <p style="margin: 10px 0 0 0; color: #E0E7FF; font-size: 14px; font-weight: 500;">
                                    Career Enhancement Platform
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px;">
                                <h2 style="margin: 0 0 20px 0; color: #1F2937; font-size: 24px; font-weight: 600;">
                                    Welcome, {name}! 👋
                                </h2>
                                
                                <p style="margin: 0 0 24px 0; color: #4B5563; font-size: 16px; line-height: 1.6;">
                                    Thank you for signing up with ElevateAI. To complete your registration and start building your developer profile, please verify your email address using the code below.
                                </p>
                                
                                <!-- Verification Code Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border: 2px solid #3B82F6; border-radius: 12px; padding: 30px; display: inline-block;">
                                                <p style="margin: 0 0 12px 0; color: #6B7280; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                                                    Your Verification Code
                                                </p>
                                                <p style="margin: 0; color: #1E40AF; font-size: 42px; font-weight: 700; letter-spacing: 12px; font-family: 'Courier New', monospace;">
                                                    {code}
                                                </p>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="margin: 24px 0 0 0; color: #6B7280; font-size: 14px; line-height: 1.6;">
                                    Enter this code on the verification page to activate your account. This code will expire in <strong style="color: #DC2626;">15 minutes</strong>.
                                </p>
                                
                                <!-- Features Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0; background-color: #F9FAFB; border-radius: 8px; padding: 20px;">
                                    <tr>
                                        <td>
                                            <p style="margin: 0 0 12px 0; color: #374151; font-size: 14px; font-weight: 600;">
                                                What's next?
                                            </p>
                                            <ul style="margin: 0; padding-left: 20px; color: #6B7280; font-size: 14px; line-height: 1.8;">
                                                <li>Connect your coding platforms (GitHub, LeetCode, etc.)</li>
                                                <li>Upload your resume for ATS analysis</li>
                                                <li>Get personalized career recommendations</li>
                                                <li>Track your progress over time</li>
                                            </ul>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #F9FAFB; padding: 30px 40px; border-top: 1px solid #E5E7EB;">
                                <p style="margin: 0 0 8px 0; color: #9CA3AF; font-size: 12px; line-height: 1.5;">
                                    If you didn't create an account with ElevateAI, you can safely ignore this email.
                                </p>
                                <p style="margin: 0; color: #9CA3AF; font-size: 12px;">
                                    © 2026 ElevateAI. All rights reserved.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    send_email(to_email, subject, html_content)

async def send_password_reset_email(to_email: str, name: str, code: str):
    """Send password reset code"""
    
    print(f"[EMAIL] Sending password reset code to {to_email}")
    print(f"[EMAIL] Reset code: {code}")
    
    subject = "Reset Your ElevateAI Password"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Your Password</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        <!-- Header with gradient -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%); padding: 40px 40px 30px 40px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">
                                    🔐 Password Reset
                                </h1>
                                <p style="margin: 10px 0 0 0; color: #FEE2E2; font-size: 14px; font-weight: 500;">
                                    ElevateAI Security
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px;">
                                <h2 style="margin: 0 0 20px 0; color: #1F2937; font-size: 24px; font-weight: 600;">
                                    Hi {name},
                                </h2>
                                
                                <p style="margin: 0 0 24px 0; color: #4B5563; font-size: 16px; line-height: 1.6;">
                                    We received a request to reset your password. Use the verification code below to create a new password for your account.
                                </p>
                                
                                <!-- Reset Code Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <div style="background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); border: 2px solid #DC2626; border-radius: 12px; padding: 30px; display: inline-block;">
                                                <p style="margin: 0 0 12px 0; color: #6B7280; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                                                    Your Reset Code
                                                </p>
                                                <p style="margin: 0; color: #991B1B; font-size: 42px; font-weight: 700; letter-spacing: 12px; font-family: 'Courier New', monospace;">
                                                    {code}
                                                </p>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="margin: 24px 0 0 0; color: #6B7280; font-size: 14px; line-height: 1.6;">
                                    Enter this code on the password reset page to create a new password. This code will expire in <strong style="color: #DC2626;">15 minutes</strong>.
                                </p>
                                
                                <!-- Security Notice -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0; background-color: #FEF3C7; border-left: 4px solid #F59E0B; border-radius: 4px; padding: 16px;">
                                    <tr>
                                        <td>
                                            <p style="margin: 0; color: #92400E; font-size: 14px; line-height: 1.6;">
                                                <strong>⚠️ Security Notice:</strong> If you didn't request this password reset, please ignore this email. Your password will remain unchanged.
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Tips Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0; background-color: #F9FAFB; border-radius: 8px; padding: 20px;">
                                    <tr>
                                        <td>
                                            <p style="margin: 0 0 12px 0; color: #374151; font-size: 14px; font-weight: 600;">
                                                Password Tips:
                                            </p>
                                            <ul style="margin: 0; padding-left: 20px; color: #6B7280; font-size: 14px; line-height: 1.8;">
                                                <li>Use at least 8 characters</li>
                                                <li>Include uppercase and lowercase letters</li>
                                                <li>Add numbers and special characters</li>
                                                <li>Avoid common words or patterns</li>
                                            </ul>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #F9FAFB; padding: 30px 40px; border-top: 1px solid #E5E7EB;">
                                <p style="margin: 0 0 8px 0; color: #9CA3AF; font-size: 12px; line-height: 1.5;">
                                    This is an automated security email from ElevateAI. Please do not reply to this message.
                                </p>
                                <p style="margin: 0; color: #9CA3AF; font-size: 12px;">
                                    © 2026 ElevateAI. All rights reserved.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    send_email(to_email, subject, html_content)

async def send_welcome_email(to_email: str, name: str):
    """Send welcome email after email verification"""
    
    print(f"[EMAIL] Sending welcome email to {to_email}")
    
    subject = "Welcome to ElevateAI! 🎉"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to ElevateAI</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        <!-- Header with gradient -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 40px 40px 30px 40px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 32px; font-weight: 700;">
                                    🎉 Welcome to ElevateAI!
                                </h1>
                                <p style="margin: 10px 0 0 0; color: #D1FAE5; font-size: 16px; font-weight: 500;">
                                    Your journey to career excellence starts now
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px;">
                                <h2 style="margin: 0 0 20px 0; color: #1F2937; font-size: 24px; font-weight: 600;">
                                    Hi {name}! 👋
                                </h2>
                                
                                <p style="margin: 0 0 24px 0; color: #4B5563; font-size: 16px; line-height: 1.6;">
                                    Your email has been verified successfully! You're all set to start building your comprehensive developer profile and take your career to the next level.
                                </p>
                                
                                <!-- CTA Button -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <a href="{settings.FRONTEND_URL}/dashboard" style="display: inline-block; background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); color: #ffffff; text-decoration: none; padding: 16px 40px; border-radius: 8px; font-size: 16px; font-weight: 600; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);">
                                                Go to Dashboard →
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Features Grid -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td>
                                            <h3 style="margin: 0 0 20px 0; color: #374151; font-size: 18px; font-weight: 600;">
                                                Get Started:
                                            </h3>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td style="padding: 16px; background-color: #EFF6FF; border-radius: 8px; margin-bottom: 12px;">
                                                        <p style="margin: 0; color: #1E40AF; font-size: 16px; font-weight: 600;">
                                                            💻 Connect Platforms
                                                        </p>
                                                        <p style="margin: 8px 0 0 0; color: #6B7280; font-size: 14px; line-height: 1.5;">
                                                            Link your GitHub, LeetCode, GeeksforGeeks, and other coding profiles
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr><td style="height: 12px;"></td></tr>
                                    <tr>
                                        <td>
                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td style="padding: 16px; background-color: #F0FDF4; border-radius: 8px;">
                                                        <p style="margin: 0; color: #166534; font-size: 16px; font-weight: 600;">
                                                            📄 Upload Resume
                                                        </p>
                                                        <p style="margin: 8px 0 0 0; color: #6B7280; font-size: 14px; line-height: 1.5;">
                                                            Get AI-powered ATS analysis and personalized recommendations
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr><td style="height: 12px;"></td></tr>
                                    <tr>
                                        <td>
                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td style="padding: 16px; background-color: #FEF3C7; border-radius: 8px;">
                                                        <p style="margin: 0; color: #92400E; font-size: 16px; font-weight: 600;">
                                                            📊 Track Progress
                                                        </p>
                                                        <p style="margin: 8px 0 0 0; color: #6B7280; font-size: 14px; line-height: 1.5;">
                                                            Monitor your coding journey and skill development over time
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr><td style="height: 12px;"></td></tr>
                                    <tr>
                                        <td>
                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td style="padding: 16px; background-color: #FDF2F8; border-radius: 8px;">
                                                        <p style="margin: 0; color: #831843; font-size: 16px; font-weight: 600;">
                                                            🎯 Get Recommendations
                                                        </p>
                                                        <p style="margin: 8px 0 0 0; color: #6B7280; font-size: 14px; line-height: 1.5;">
                                                            Receive personalized career advice and skill improvement tips
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="margin: 30px 0 0 0; color: #4B5563; font-size: 16px; line-height: 1.6;">
                                    Happy coding! 💻✨
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #F9FAFB; padding: 30px 40px; border-top: 1px solid #E5E7EB;">
                                <p style="margin: 0 0 8px 0; color: #9CA3AF; font-size: 12px; line-height: 1.5;">
                                    Need help? Reply to this email or visit our support page.
                                </p>
                                <p style="margin: 0; color: #9CA3AF; font-size: 12px;">
                                    © 2026 ElevateAI. All rights reserved.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    try:
        send_email(to_email, subject, html_content)
    except Exception as e:
        print(f"[EMAIL] Failed to send welcome email: {e}")
        # Don't raise, welcome email is not critical
