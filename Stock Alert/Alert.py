# CODE NEEDS TO BE SCHEDULED IN WINDOWS OR UNIX

import yfinance as yf
import smtplib
from email.message import EmailMessage

Ticker = "VALE"
Target = 100

price = yf.Ticker(Ticker).history(period="1d")["Close"].iloc[-1]

if price > Target:
    msg = EmailMessage()
    msg.set_content(f"{Ticker} is above {Target}: {price}")
    msg["Subject"] = Ticker + "Stock Alert"
    msg["From"] = "jrfsousa2@gmail.com"
    msg["To"] = "jrfsousa2@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login("jrfsousa2@gmail.com", "APP_PASSWORD")
        s.send_message(msg)