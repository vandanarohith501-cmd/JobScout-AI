import argparse
import sys
from datetime import datetime
from pathlib import Path

from src.config import PROJECT_ROOT, OUTPUT_DIR, ASSETS_DIR, ENV, PROFILE
from src.ats_verifier import get_verified_openings
from src.pdf_builder import generate_report, render_preview_images
from src.mailer import send_daily_email

def main():
    parser = argparse.ArgumentParser(description="JobScout AI - Autonomous Career Discovery & Dispatch Agent")
    parser.add_argument("--dry-run", action="store_true", help="Generate PDF report without sending email")
    parser.add_argument("--render-preview", action="store_true", help="Render preview PNGs for README / UI")
    args = parser.parse_args()

    today_tag = datetime.now().strftime("%Y-%m-%d")
    pdf_filename = f"Job_Research_Report_{today_tag}.pdf"
    pdf_path = OUTPUT_DIR / pdf_filename

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === Starting JobScout AI Pipeline ===")
    
    # 1. Fetch & Verify Openings
    print("[1/3] Fetching and verifying active ATS job postings...")
    jobs = get_verified_openings()
    print(f"      Verified {len(jobs)} active, deep ATS application forms.")

    # 2. Build Landscape A4 PDF
    print(f"[2/3] Compiling Landscape A4 PDF report: {pdf_path}...")
    generate_report(pdf_path, jobs, PROFILE)
    print("      PDF report generated successfully.")

    if args.render_preview:
        print("[*] Rendering high-definition PNG previews into assets/...")
        render_preview_images(pdf_path, ASSETS_DIR)
        print("    Preview images updated.")

    # 3. Email Dispatch
    if args.dry_run:
        print("[3/3] Dry run enabled: Skipping email dispatch.")
    else:
        print("[3/3] Dispatching daily email to configured recipient...")
        try:
            candidate_name = PROFILE.get("candidate", {}).get("name", "Rohith Vandana")
            send_daily_email(pdf_path, jobs, ENV, candidate_name=candidate_name)
            print(f"      SUCCESS: Email delivered to {ENV.get('RECIPIENT_EMAIL')}!")
        except Exception as e:
            print(f"      ERROR sending email: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === Pipeline Finished Successfully ===")

if __name__ == "__main__":
    main()
