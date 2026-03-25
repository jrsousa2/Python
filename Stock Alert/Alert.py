# THIS CODE NEEDS TO BE SCHEDULED IN WINDOWS OR UNIX
# I USED THE WINDOWS TASK SCHEDULER

import yfinance as yf
import smtplib
from email.message import EmailMessage
from os import environ

Ticker = "SMCI"
Target = float(environ["SMCI_TARGET"])

APP_PASSWORD = environ["GMAIL_APP_SMTP_PASSWORD"]
APP_PASSWORD = APP_PASSWORD.replace(" ", "")

data = yf.Ticker(Ticker).history(period="1d")

if data.empty:
    raise RuntimeError("No price data returned")

price = data["Close"].iloc[-1]

if price > Target:
    msg = EmailMessage()
    msg.set_content(f"{Ticker} is above {Target}: {price}")
    msg["Subject"] = Ticker + " Stock Alert"
    msg["From"] = "jrfsousa2@gmail.com"
    msg["To"] = "jrfsousa2@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login("jrfsousa2@gmail.com", APP_PASSWORD)
        s.send_message(msg)
else:
    print("Price is not above target:",Target)        