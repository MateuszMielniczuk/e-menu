#!/usr/local/bin/python
import smtplib
import ssl
import sys
from datetime import date, timedelta
from email.message import EmailMessage

from sqlalchemy import Date, cast

sys.path.append("/opt/python/")
from app.core.config import settings  # noqa E402
from app.database.session import SessionLocal  # noqa E402
from app.models.dish import Dish as DishModel  # noqa E402
from app.models.user import User as UserModel  # noqa E402

SMTP_SERVER = settings.SMTP_SERVER
PASSWORD = settings.SMTP_PASSWORD
PORT = settings.SMTP_PORT
SENDER_EMAIL = settings.SENDER_EMAIL

db = SessionLocal()


def get_list(db_query):
    if db_query:
        result = [" -" + element[0] for element in db_query if element]
    else:
        result = []
    return "\n".join(result)


users = db.query(UserModel.email).all()

yesterday = date.today() - timedelta(days=1)

db_dish_created = (
    db.query(DishModel.name).filter(cast(DishModel.date_created, Date) == date.strftime(yesterday, "%Y-%m-%d")).all()
)
db_dish_updated = (
    db.query(DishModel.name).filter(cast(DishModel.date_updated, Date) == date.strftime(yesterday, "%Y-%m-%d")).all()
)
db.close()


users_in_db = [user[0] for user in users if user]
dish_created = get_list(db_dish_created)
dish_updated = get_list(db_dish_updated)


subject = "NO_REPLAY Last updates to e-MENU dishes."

message = EmailMessage()
message["From"] = SENDER_EMAIL
message["To"] = ", ".join(users_in_db)
message["Subject"] = subject

message.set_content(
    f"""\
Hello e-MENU app developer!!!

Below is the list of dishes created or updated yesterday.
Newly added items:
{dish_created if dish_created else " - no dish created yesterday"}

Newly added items:
{dish_updated if dish_updated else " - no dish updated yesterday"}

Best regards,
        e-MENU app ;)
"""
)


def send_email():
    context = ssl.create_default_context()

    # send email from SMTP server
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as smtp:
        smtp.login(SENDER_EMAIL, PASSWORD)
        smtp.send_message(message)


def send_console_email():
    # Send email to local console
    with smtplib.SMTP(SMTP_SERVER, PORT) as smtp:
        smtp.send_message(message)


if users_in_db:
    if SMTP_SERVER == "localhost":
        send_console_email()
    else:
        send_email()
