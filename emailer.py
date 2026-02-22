import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(items: list[dict]):
    if not items:
        return

    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    to_email = os.getenv("TO_EMAIL")

    # Build HTML email
    html = "<h2>🚀 Startup Intelligence Update</h2>"

    categories = ["Funding", "New Startup", "News", "Jobs"]
    icons = {"Funding": "💰", "New Startup": "🌱", "News": "📰", "Jobs": "💼"}

    for cat in categories:
        cat_items = [i for i in items if i.get("category") == cat]
        if not cat_items:
            continue
        html += f"<h3>{icons.get(cat, '')} {cat}</h3><ul>"
        for item in cat_items:
            html += f"""
                <li>
                    <a href="{item['url']}"><strong>{item['title']}</strong></a><br/>
                    <span>{item['summary']}</span>
                </li><br/>
            """
        html += "</ul>"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚀 Startup Digest — {len(items)} new updates"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        print(f"✅ Email sent with {len(items)} items")