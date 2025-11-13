import os
import requests
from email.message import EmailMessage
import smtplib
from datetime import datetime

QUERY = "fresher ai jobs OR gen ai fresher jobs OR entry level machine learning engineer"

def search_jobs():
    api_key = os.environ["SEARCH_API_KEY"]
    params = {
        "engine": "google",
        "q": QUERY,
        "api_key": api_key,
        "num": 20
    }
    r = requests.get("https://serpapi.com/search", params=params)
    r.raise_for_status()
    data = r.json()
    return data.get("organic_results", [])

def send_email(results):
    sender = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASS"]
    recipient = "saipramod1449@gmail.com"

    msg = EmailMessage()
    msg["Subject"] = "Daily AI/GenAI Fresher Job Updates"
    msg["From"] = sender
    msg["To"] = recipient

    body = f"Checked at: {datetime.now()}

"
    for r in results:
        title = r.get("title", "")
        link = r.get("link", "")
        snippet = r.get("snippet", "")
        body += f"{title}\n{link}\n{snippet}\n\n"

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

def main():
    results = search_jobs()
    send_email(results)

if __name__ == "__main__":
    main()
