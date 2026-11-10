# JobScout AI

An automated career intelligence pipeline that queries, verifies, and delivers fresh job openings directly to your inbox.

---

## Overview

JobScout AI automates daily technical job discovery by:
1. Querying applicant tracking systems (Greenhouse, AshbyHQ, Unstop).
2. Verifying live HTTP status (HTTP 200) to filter out expired or inactive links.
3. Matching openings against candidate profiles (degree, batch, tech stack).
4. Generating a formatted Landscape A4 PDF report using ReportLab.
5. Delivering an HTML digest with the PDF attached via SMTP SSL.

---

## Project Structure

```text
JobScout-AI/
├── assets/             # Report preview screenshots
├── data/
│   └── profile.yaml    # Candidate targeting parameters
├── scripts/
│   ├── run_daily.bat   # Windows batch execution wrapper
│   └── setup_scheduler.ps1 # Task Scheduler configuration script
├── src/
│   ├── ats_verifier.py # HTTP endpoint verification and filtering logic
│   ├── config.py       # Configuration and environment loaders
│   ├── mailer.py       # SMTP MIME email delivery module
│   └── pdf_builder.py  # ReportLab document generation engine
├── main.py             # CLI entry point
├── requirements.txt    # Python dependencies
└── .env.example        # Environment variable template
```

---

## Getting Started

### 1. Installation

Clone this repository and install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your values:
* `GMAIL_USER`: Sender Gmail address
* `GMAIL_APP_PASS`: 16-character Google App Password
* `RECIPIENT_EMAIL`: Target recipient address

Update `data/profile.yaml` with your target roles, graduation batch, and tech stack.

---

## Usage

### Run the Full Pipeline

```bash
python main.py
```

### Dry Run (Generate PDF without Emailing)

```bash
python main.py --dry-run
```

### Render Image Previews

```bash
python main.py --dry-run --render-preview
```

---

## Automated Scheduling (Windows)

To run the pipeline daily at 5:00 PM IST with battery-bypass and catch-up support:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_scheduler.ps1
```

---

## License

This project is open-source under the MIT License.
