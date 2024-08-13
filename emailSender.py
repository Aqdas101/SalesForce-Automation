import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic import BaseModel, EmailStr, ValidationError
from loggingConfig import logger
import loggingConfig
import os


class EmailModel(BaseModel):
  receiver_email: EmailStr
  sender_email: EmailStr
  app_password: str
  email_body: str
  email_subject: str


def sent_email(email_subject,
               email_body,
               receiver_email: str,
               sender_email: str,
               app_password: str) -> None:

  try:
    email_data = EmailModel(receiver_email=receiver_email,
                            sender_email=sender_email,
                            email_subject=email_subject,
                            email_body=email_body,
                            app_password=app_password)
  except ValidationError as e:
    logger.error('Error validating email data: %s', e)
    raise ValueError(f"Email Model Error: {e}")

  message = MIMEMultipart()
  message['From'] = email_data.sender_email
  message['To'] = email_data.receiver_email

  message['Subject'] = email_data.email_subject
  body = email_data.email_body

  try:
    message.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_data.sender_email, email_data.app_password)
    server.sendmail(email_data.sender_email, email_data.receiver_email,
                    message.as_string())
    server.quit()
    logger.info('Email sent successfully')
    print('Email sent successfully')

  except Exception as e:
    logger.error('Error sending email: %s', e)
    raise ValueError(f"Email sending failed: {e}")
