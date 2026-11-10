import os
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

def send_daily_email(pdf_path: Path, jobs: list, env: dict, candidate_name: str = "Rohith Vandana") -> bool:
    """Dispatches transactional job alert email with inline HTML styling and PDF attachment."""
    sender = env.get("GMAIL_USER")
    app_pass = env.get("GMAIL_APP_PASS")
    recipient = env.get("RECIPIENT_EMAIL", sender)

    if not sender or not app_pass:
        raise ValueError("Missing GMAIL_USER or GMAIL_APP_PASS in environment.")

    today_str = datetime.now().strftime("%d %b %Y")

    msg = MIMEMultipart("related")
    msg["Subject"] = f"Job Research - {today_str} ({len(jobs)} Verified Openings: AI Engineer / Python Developer)"
    msg["From"] = f"JobScout AI <{sender}>"
    msg["To"] = recipient

    # Build dynamic table rows
    rows_html = ""
    for idx, j in enumerate(jobs[:10]):
        bg = "#ffffff" if idx % 2 == 0 else "#f8fafc"
        rows_html += f"""
        <tr style="background-color: {bg};">
            <td style="padding: 8px 10px; border: 1px solid #e2e8f0;">{j['num']}</td>
            <td style="padding: 8px 10px; border: 1px solid #e2e8f0;"><strong>{j['role']}</strong></td>
            <td style="padding: 8px 10px; border: 1px solid #e2e8f0;">{j['company']}</td>
            <td style="padding: 8px 10px; border: 1px solid #e2e8f0;">{j['location']}</td>
            <td style="padding: 8px 10px; border: 1px solid #e2e8f0;">{j['platform']}</td>
            <td style="padding: 8px 10px; border: 1px solid #e2e8f0; text-align: center;">
                <a href="{j['link']}" style="color: #2563eb; font-weight: 700; text-decoration: underline;">Apply &rarr;</a>
            </td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 20px;">
        <div style="max-width: 720px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background-color: #0f172a; padding: 24px; color: #ffffff;">
                <h2 style="margin: 0 0 6px 0; font-size: 20px; font-weight: 700; color: #ffffff;">Daily Job Research Report &mdash; {today_str}</h2>
                <p style="margin: 0; font-size: 13px; color: #94a3b8;">
                    Curated for <strong>{candidate_name}</strong> &bull; B.Tech ECE (Batch 2027) &bull; SRM IST
                </p>
            </div>
            
            <div style="padding: 20px 24px;">
                <div style="background-color: #f1f5f9; border-left: 4px solid #2563eb; padding: 12px 16px; margin-bottom: 20px; border-radius: 0 4px 4px 0;">
                    <p style="margin: 0; font-size: 13px; line-height: 1.5; color: #334155;">
                        Found <strong>{len(jobs)} live, HTTP-verified openings</strong> matching your Agentic AI, AI/ML, Python/FastAPI Backend, and Full-Stack tracks. All direct ATS forms &mdash; zero generic homepages.
                    </p>
                </div>

                <h3 style="font-size: 15px; margin: 0 0 12px 0; color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">
                    Top Verified Opportunities (High Fit First)
                </h3>

                <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 24px;">
                    <thead>
                        <tr style="background-color: #1e293b; color: #ffffff; text-align: left;">
                            <th style="padding: 8px 10px; border: 1px solid #cbd5e1;">#</th>
                            <th style="padding: 8px 10px; border: 1px solid #cbd5e1;">Role Title</th>
                            <th style="padding: 8px 10px; border: 1px solid #cbd5e1;">Company</th>
                            <th style="padding: 8px 10px; border: 1px solid #cbd5e1;">Location</th>
                            <th style="padding: 8px 10px; border: 1px solid #cbd5e1;">Platform</th>
                            <th style="padding: 8px 10px; border: 1px solid #cbd5e1; text-align: center;">Direct Link</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>

                <p style="font-size: 13px; color: #475569; margin: 0 0 16px 0;">
                    &bull; <em>The complete Landscape A4 PDF with all {len(jobs)} verified openings is attached.</em>
                </p>

                <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 12px 16px; border-radius: 6px;">
                    <p style="margin: 0; font-size: 12px; color: #1e40af;">
                        <strong>Tip:</strong> Apply to <strong>SingleStore Engine-2027</strong> and <strong>Meraki-Labs</strong> immediately before screening pools cap out.
                    </p>
                </div>
            </div>

            <div style="background-color: #f8fafc; padding: 14px 24px; border-top: 1px solid #e2e8f0; text-align: center; font-size: 11px; color: #94a3b8;">
                JobScout AI &bull; Autonomous Career Opportunity Pipeline
            </div>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            pdf_attach = MIMEApplication(f.read(), _subtype="pdf")
            pdf_attach.add_header("Content-Disposition", "attachment", filename=pdf_path.name)
            msg.attach(pdf_attach)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_pass)
        server.send_message(msg)

    return True
