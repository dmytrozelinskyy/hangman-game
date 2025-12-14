import os
from dotenv import load_dotenv
import yagmail
import logging

load_dotenv("settings.env")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

logger = logging.getLogger(__name__)

yag = None
if SENDER_EMAIL or APP_PASSWORD:
    yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)


# -- Send Welcome Email -- #
def send_welcome_email(to_email: str, username: str):
    if not yag:
        logger.warning("Email client not initialized. Welcome Email skipped.")
        return False

    try:
        subject = "Welcome to Hangman Game!"
        body = f"""
            Hello {username},

            Welcome to the Hangman Game!
            We are excited to have you on board.

            Enjoy playing!
            ⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡
            PPY<>PJATK<>2025
            s31639    
            """
        yag.send(to=to_email, subject=subject, contents=body)
        logger.info(f"Welcome email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
        return False


# -- Send Reset Password Email -- #
def send_reset_password_email(to_email: str, username: str, new_password: str):
    if not yag:
        logger.warning("Email client not initialized. Password Reset Email skipped.")
        return False

    try:
        subject = "Hangman Password Reset"
        body = f"""
            Hello {username}

            Your password has been reset.

            Your new password is: {new_password}
            """
        yag.send(to=to_email, subject=subject, contents=body);
        logger.info(f"Password reset email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email: {e}")
        return False
