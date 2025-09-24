from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",
    MAIL_PASSWORD="your_password",
    MAIL_FROM="your_email@example.com",
    MAIL_PORT=587,   # use 465 if SSL
    MAIL_SERVER="smtp.gmail.com",  # Gmail example
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(recipients: List[EmailStr], subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,  # must be a list
        body=body,
        subtype="html"  # you can also use "plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)