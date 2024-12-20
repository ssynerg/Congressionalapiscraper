import os
import requests
import smtplib
from email.mime.text import MIMEText

# Configuration
API_KEY = "your_api_key_here"
START = 10515
SMTP_SERVER = "smtp.your-email-provider.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
RECIPIENT_EMAIL = "recipient_email@example.com"

def send_email_notification(subject, body):
    """Send an email notification."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        print("Notification email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def download_congress_data():
    """Download congressional data and notify upon issues."""
    i = START
    while True:
        output_file = f"response-{i}.json"

        # Skip if file already exists
        if os.path.exists(output_file):
            print(f"{output_file} already exists. Skipping.")
            i += 1
            continue

        # API URL (replace with the actual API endpoint)
        url = f"https://api.congress.gov/v3/bill/118/hr/{i}?api_key={API_KEY}"

        # Make the API request
        response = requests.get(url, headers={"Accept": "application/json"})

        # Handle HTTP response
        if response.status_code != 200:
            print(f"Non-200 response ({response.status_code}) encountered at {i}. Stopping.")
            send_email_notification(
                "Congress API Download Stopped",
                f"Non-200 response code {response.status_code} encountered at ID {i}."
            )
            break

        # Save the response to a file
        with open(output_file, "w") as f:
            f.write(response.text)
        print(f"Successfully downloaded {output_file}")

        # Increment for the next iteration
        i += 1

if __name__ == "__main__":
    try:
        download_congress_data()
    except Exception as e:
        send_email_notification(
            "Congress API Script Error",
            f"An error occurred while running the script: {e}"
        )
