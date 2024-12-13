import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_notification(user, message):
    # configure email settings
    sender_email = "sebbievayo2@gmail.com"
    sender_password = "Seb#@Evayo1"

    # create message
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = user.email
    email_message['Subject'] = f"Whatsapp Message from {message.sender_number}"

    body = f"""
    You have a new whatsapp message:
    From: {message.sender_number}
    Message: {message.message_cotent}
    Received at: {message.timestamp}
    """

    email_message.attach(MIMEText(body, 'plain'))

    # send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        return True
    except Exception as e:
        print("Email sending failed:{e}")
        return False