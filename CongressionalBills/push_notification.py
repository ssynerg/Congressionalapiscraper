import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

# Load environment variables
load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_PHONE = os.getenv("PUSH_NOTIFICATION_PHONE")

def generate_push_notification(input_file):
    """
    Generate a short summary of bills for push notification.
    """
    try:
        # Read the processed bills file
        df = pd.read_csv(input_file)
        if 'title' not in df.columns or 'plain_language_summary' not in df.columns:
            return "No data found to include in the push notification."

        # Create a short summary message
        message = "Legislative Update:\n"
        for index, row in df.iterrows():
            message += f"- {row['title'][:30]}: {row['plain_language_summary'][:50]}...\n"

        return message
    except Exception as e:
        print(f"Error generating push notification: {e}")
        return "Error generating push notification."

def send_push_notification(subject, message):
    """
    Send a push notification via email-to-SMS.
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_PHONE
        msg['Subject'] = subject

        # Attach the message
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Push notification sent to {RECIPIENT_PHONE}")
    except Exception as e:
        print(f"Error sending push notification: {e}")

if __name__ == "__main__":
    # File with processed bills
    input_csv = "bills_with_expenditures.csv"

    # Generate and send push notification
    message = generate_push_notification(input_csv)
    if message:
        send_push_notification("Legislative Update", message)
