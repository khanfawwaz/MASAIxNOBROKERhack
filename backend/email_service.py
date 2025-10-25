import os
import asyncio
from typing import Optional, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from jinja2 import Template
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY", "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")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@citizenissuetracker.com")
        self.from_name = os.getenv("FROM_NAME", "Citizen Issue Tracker")
        
        if not self.api_key:
            logger.warning("SendGrid API key not found. Email functionality will be disabled.")
            self.client = None
        else:
            try:
                self.client = SendGridAPIClient(api_key=self.api_key)
                logger.info("SendGrid client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize SendGrid client: {e}")
                self.client = None
    
    async def send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str, 
        plain_text_content: Optional[str] = None
    ) -> bool:
        """Send an email using SendGrid"""
        if not self.client:
            logger.warning("SendGrid client not initialized. Email not sent.")
            return False
        
        try:
            from_email = Email(self.from_email, self.from_name)
            to_email = To(to_email)
            
            if plain_text_content:
                content = Content("text/plain", plain_text_content)
            else:
                content = Content("text/html", html_content)
            
            mail = Mail(from_email, to_email, subject, content)
            
            # Send email asynchronously
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.send(mail)
            )
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    async def send_welcome_email(self, user_email: str, user_name: str, role: str) -> bool:
        """Send welcome email to new users"""
        subject = "Welcome to Citizen Issue Tracker!"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to Citizen Issue Tracker</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Citizen Issue Tracker!</h1>
                </div>
                <div class="content">
                    <h2>Hello {{ user_name }}!</h2>
                    <p>Welcome to the Citizen Issue Tracker platform! We're excited to have you join our community.</p>
                    
                    {% if role == 'citizen' %}
                    <p>As a citizen, you can:</p>
                    <ul>
                        <li>Report issues in your local area (potholes, garbage, streetlights, etc.)</li>
                        <li>Track the progress of your reported issues</li>
                        <li>Receive updates when issues are resolved</li>
                        <li>View the status of all your submissions</li>
                    </ul>
                    {% else %}
                    <p>As an administrator, you can:</p>
                    <ul>
                        <li>View and manage all reported issues</li>
                        <li>Update issue status and assign them to team members</li>
                        <li>Add comments and progress updates</li>
                        <li>Access analytics and reporting tools</li>
                    </ul>
                    {% endif %}
                    
                    <p>Your account has been successfully created and you can now start using the platform.</p>
                    
                    <a href="http://localhost:3001" class="button">Get Started</a>
                    
                    <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
                    
                    <p>Best regards,<br>The Citizen Issue Tracker Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent from Citizen Issue Tracker. If you didn't create an account, please ignore this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(user_name=user_name, role=role)
        
        plain_text = f"""
        Welcome to Citizen Issue Tracker!
        
        Hello {user_name}!
        
        Welcome to the Citizen Issue Tracker platform! We're excited to have you join our community.
        
        Your account has been successfully created and you can now start using the platform.
        
        Visit: http://localhost:3001
        
        Best regards,
        The Citizen Issue Tracker Team
        """
        
        return await self.send_email(user_email, subject, html_content, plain_text)
    
    async def send_login_notification(self, user_email: str, user_name: str, login_time: str) -> bool:
        """Send login notification email"""
        subject = "Login Notification - Citizen Issue Tracker"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Login Notification</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .alert { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Login Notification</h1>
                </div>
                <div class="content">
                    <h2>Hello {{ user_name }}!</h2>
                    <p>We're notifying you that someone has logged into your Citizen Issue Tracker account.</p>
                    
                    <div class="alert">
                        <strong>Login Details:</strong><br>
                        <strong>Time:</strong> {{ login_time }}<br>
                        <strong>Account:</strong> {{ user_email }}
                    </div>
                    
                    <p>If this was you, you can safely ignore this email.</p>
                    
                    <p><strong>If this wasn't you:</strong></p>
                    <ul>
                        <li>Your account may have been compromised</li>
                        <li>Please change your password immediately</li>
                        <li>Contact our support team if you need assistance</li>
                    </ul>
                    
                    <p>For security reasons, we recommend using a strong, unique password for your account.</p>
                    
                    <p>Best regards,<br>The Citizen Issue Tracker Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated security notification. If you have concerns, please contact support.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(user_name=user_name, user_email=user_email, login_time=login_time)
        
        plain_text = f"""
        Login Notification - Citizen Issue Tracker
        
        Hello {user_name}!
        
        We're notifying you that someone has logged into your Citizen Issue Tracker account.
        
        Login Details:
        Time: {login_time}
        Account: {user_email}
        
        If this was you, you can safely ignore this email.
        
        If this wasn't you:
        - Your account may have been compromised
        - Please change your password immediately
        - Contact our support team if you need assistance
        
        Best regards,
        The Citizen Issue Tracker Team
        """
        
        return await self.send_email(user_email, subject, html_content, plain_text)
    
    async def send_issue_update_email(
        self, 
        user_email: str, 
        user_name: str, 
        issue_title: str, 
        issue_status: str, 
        update_message: str,
        issue_id: str
    ) -> bool:
        """Send issue update notification email"""
        subject = f"Issue Update: {issue_title}"
        
        status_colors = {
            "pending": "#ffc107",
            "in_progress": "#17a2b8", 
            "completed": "#28a745",
            "rejected": "#dc3545"
        }
        
        status_color = status_colors.get(issue_status, "#6c757d")
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Issue Update</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .status-badge { display: inline-block; padding: 8px 16px; border-radius: 20px; color: white; font-weight: bold; margin: 10px 0; }
                .issue-card { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 20px 0; }
                .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Issue Update</h1>
                </div>
                <div class="content">
                    <h2>Hello {{ user_name }}!</h2>
                    <p>We have an update on your reported issue.</p>
                    
                    <div class="issue-card">
                        <h3>{{ issue_title }}</h3>
                        <div class="status-badge" style="background-color: {{ status_color }};">
                            Status: {{ issue_status.title() }}
                        </div>
                        <p><strong>Update:</strong> {{ update_message }}</p>
                    </div>
                    
                    <p>You can view more details about this issue by clicking the button below.</p>
                    
                    <a href="http://localhost:3001/issue/{{ issue_id }}" class="button">View Issue Details</a>
                    
                    <p>Thank you for using Citizen Issue Tracker to help improve our community!</p>
                    
                    <p>Best regards,<br>The Citizen Issue Tracker Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent regarding your reported issue. You can unsubscribe from these notifications in your account settings.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            user_name=user_name,
            issue_title=issue_title,
            issue_status=issue_status,
            status_color=status_color,
            update_message=update_message,
            issue_id=issue_id
        )
        
        plain_text = f"""
        Issue Update: {issue_title}
        
        Hello {user_name}!
        
        We have an update on your reported issue.
        
        Issue: {issue_title}
        Status: {issue_status.title()}
        Update: {update_message}
        
        You can view more details about this issue at: http://localhost:3001/issue/{issue_id}
        
        Thank you for using Citizen Issue Tracker to help improve our community!
        
        Best regards,
        The Citizen Issue Tracker Team
        """
        
        return await self.send_email(user_email, subject, html_content, plain_text)

# Global email service instance
email_service = EmailService()
