import json
from pathlib import Path
from datetime import datetime
from src.config import DATA_DIR

HISTORY_FILE = DATA_DIR / "history.json"

def _normalize(text: str) -> str:
    return "".join(c.lower() for c in text if c.isalnum())

def load_history():
    """Loads all previously sent job URLs and fingerprints."""
    seen_urls = set()
    seen_fingerprints = set()

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("sent_jobs", []):
                    url = item.get("link", "").strip()
                    comp = _normalize(item.get("company", ""))
                    role = _normalize(item.get("role", ""))
                    if url:
                        seen_urls.add(url.lower())
                    if comp and role:
                        seen_fingerprints.add(f"{comp}|{role}")
        except Exception as e:
            print(f"[Warning] Could not load history.json: {e}")

    return seen_urls, seen_fingerprints

def is_job_seen(link: str, company: str, role: str) -> bool:
    """Checks if a job URL or (company + role) fingerprint was already sent."""
    seen_urls, seen_fingerprints = load_history()
    
    clean_url = link.strip().lower()
    if clean_url in seen_urls:
        return True

    fp = f"{_normalize(company)}|{_normalize(role)}"
    if fp in seen_fingerprints:
        return True

    return False

def record_sent_jobs(jobs: list):
    """Appends newly dispatched jobs to history.json so they are never repeated."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    existing_data = {"sent_jobs": []}

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception:
            existing_data = {"sent_jobs": []}

    sent_list = existing_data.get("sent_jobs", [])
    seen_urls = {item.get("link", "").strip().lower() for item in sent_list}

    for j in jobs:
        url = j.get("link", "").strip()
        if url and url.lower() not in seen_urls:
            sent_list.append({
                "company": j.get("company", ""),
                "role": j.get("role", ""),
                "link": url,
                "sent_at": today_str
            })
            seen_urls.add(url.lower())

    existing_data["sent_jobs"] = sent_list

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)

    print(f"[History] Recorded {len(jobs)} jobs in {HISTORY_FILE}. Total historical sent: {len(sent_list)}.")
