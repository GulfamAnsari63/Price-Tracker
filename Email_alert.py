import smtplib
from email.message import EmailMessage
import os

def alert_system(product, link):
    email_id = os.environ.get('EMAIL_ID')
    email_pass = os.environ.get('EMAIL_PASS')
    receiver_email = os.environ.get('RECEIVER_EMAIL')

    if not (email_id and email_pass and receiver_email):
        print("Email configuration is incomplete. Please set EMAIL_ID, EMAIL_PASS, and RECEIVER_EMAIL environment variables.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Price Drop Alert'
    msg['From'] = 'imperiousakagulf@gmail.com'
    msg['To'] = 'gulfam2020cs119@abesit.edu.in'
    msg.set_content(f'Hey, the price of {product} dropped!\n{link}')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_id, email_pass)
            smtp.send_message(msg)
        print('Email alert sent successfully!')
    except Exception as e:
        print(f"Error sending email: {e}")

# Uncomment the line below and replace placeholders with your actual values
# alert_system("Product Name", "Product Link")
