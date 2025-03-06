from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "dhrudevloper@gmail.com"
SENDER_PASSWORD = "jbil clwz izib matg"

# Function to send an email
def send_email(recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        print(f"Email sent to {recipient_email}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to send email to {recipient_email}: {e.smtp_code} - {e.smtp_error}")
    except Exception as e:
        print(f"An error occurred while sending email to {recipient_email}: {e}")