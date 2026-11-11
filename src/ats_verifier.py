import urllib.request
import json
from collections import defaultdict
from src.history import is_job_seen

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

GH_BOARDS = [
    ('inmobi', 'InMobi'),
    ('rubrik', 'Rubrik'),
    ('stripe', 'Stripe'),
    ('coinbase', 'Coinbase'),
    ('nutanix', 'Nutanix'),
    ('thoughtspot', 'ThoughtSpot'),
    ('zepto', 'Zepto'),
    ('speechify', 'Speechify'),
    ('groww', 'Groww'),
    ('singlestore', 'SingleStore'),
    ('hackerrank', 'HackerRank'),
    ('enterpret', 'Enterpret'),
    ('karya', 'Karya')
]

ASHBY_BOARDS = [
    ('sarvam', 'Sarvam AI'),
    ('plane', 'Plane Software'),
    ('aiprise', 'AiPrise'),
    ('smallest', 'Smallest.ai'),
    ('Meraki-Labs', 'Meraki Labs'),
    ('certa', 'Certa'),
    ('glean', 'Glean'),
    ('cohere', 'Cohere'),
    ('perplexity', 'Perplexity'),
    ('dust', 'Dust')
]

def verify_url(url: str, timeout: int = 5) -> bool:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False

def get_verified_openings(max_rows: int = 16, max_per_company: int = 2):
    """
    Dynamically crawls live ATS boards and returns UNSEEN, fresh openings.
    Enforces strict non-repetition and company diversity (max 2 per company).
    """
    raw_candidates = []

    # 1. Crawl Ashby boards
    for b_id, comp_name in ASHBY_BOARDS:
        try:
            url = f"https://api.ashbyhq.com/posting-api/job-board/{b_id}"
            req = urllib.request.Request(url, headers=HEADERS)
            data = json.loads(urllib.request.urlopen(req, timeout=3).read().decode('utf-8'))
            for j in data.get('jobs', []):
                loc = str(j.get('location', '')).lower()
                title = j.get('title', '')
                t_low = title.lower()
                jurl = j.get('jobUrl', '')

                if any(k in loc for k in ['india', 'bengaluru', 'bangalore', 'remote', 'hyderabad', 'chennai', 'pune']):
                    if any(r in t_low for r in ['intern', 'junior', 'associate', 'trainee', 'engineer', 'developer', 'ai', 'ml', 'python', 'backend', 'frontend', 'data', 'evaluations']):
                        if not any(neg in t_low for neg in ['lead', 'principal', 'staff', 'manager', 'director', 'vp', 'head of', 'architect']):
                            raw_candidates.append({
                                'company': comp_name,
                                'role': title,
                                'location': j.get('location', 'Bengaluru, India'),
                                'platform': 'AshbyHQ',
                                'link': jurl
                            })
        except Exception:
            pass

    # 2. Crawl Greenhouse boards
    for b_id, comp_name in GH_BOARDS:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{b_id}/jobs"
            req = urllib.request.Request(url, headers=HEADERS)
            data = json.loads(urllib.request.urlopen(req, timeout=3).read().decode('utf-8'))
            for j in data.get('jobs', []):
                loc = str(j.get('location', {}).get('name', '')).lower()
                title = j.get('title', '')
                t_low = title.lower()
                jurl = j.get('absolute_url', '')

                if any(k in loc for k in ['india', 'bengaluru', 'bangalore', 'remote', 'hyderabad', 'chennai', 'pune']):
                    if any(r in t_low for r in ['intern', 'junior', 'associate', 'trainee', 'engineer', 'developer', 'ai', 'ml', 'python', 'backend', 'frontend', 'data']):
                        if not any(neg in t_low for neg in ['lead', 'principal', 'staff', 'manager', 'director', 'vp', 'head of', 'architect']):
                            raw_candidates.append({
                                'company': comp_name,
                                'role': title,
                                'location': j.get('location', {}).get('name', 'India'),
                                'platform': 'Greenhouse',
                                'link': jurl
                            })
        except Exception:
            pass

    # 3. Deduplication against history
    unseen_jobs = []
    for j in raw_candidates:
        if is_job_seen(j['link'], j['company'], j['role']):
            continue
        unseen_jobs.append(j)

    print(f"[ATS Verifier] Scanned {len(raw_candidates)} total postings.")
    print(f"[ATS Verifier] {len(unseen_jobs)} FRESH, UNSEEN jobs available in pool.")

    # 4. Diversity Cap: Max 2 jobs per company to ensure high variety
    company_counts = defaultdict(int)
    diverse_selection = []
    for j in unseen_jobs:
        comp = j['company']
        if company_counts[comp] < max_per_company:
            company_counts[comp] += 1
            diverse_selection.append(j)
        if len(diverse_selection) >= max_rows:
            break

    # 5. Format & Enrich
    formatted_jobs = []
    for idx, item in enumerate(diverse_selection):
        role_low = item['role'].lower()
        if any(k in role_low for k in ['agent', 'ai', 'ml', 'machine learning', 'python', 'intern']):
            fit = "HIGH"
            if 'agent' in role_low:
                skills = "Autonomous Agents, Tool Calling, LangGraph, Python, LLMs. Fits your Agentic AI track."
                eligibility = "B.Tech (2026/2027) / Freshers"
            elif 'intern' in role_low:
                skills = "Core Data Structures, Python, Problem Solving, AI/Backend fundamentals. Fits 2027 batch."
                eligibility = "B.Tech Batch of 2026/2027"
            elif 'python' in role_low or 'backend' in role_low:
                skills = "Python, FastAPI/Django, REST APIs, SQL, Data Modeling. Fits your backend portfolio."
                eligibility = "Junior / Entry-Level / Fresher"
            else:
                skills = "PyTorch, Scikit-learn, Machine Learning pipelines, Model Evaluation. Fits ML track."
                eligibility = "Early Career / Pre-final B.Tech"
        else:
            fit = "HIGH" if 'frontend' in role_low or 'react' in role_low else "MEDIUM"
            skills = "Full-stack development, React, JavaScript, APIs. Fits your web & React experience."
            eligibility = "B.Tech Freshers / 0-1 YOE"

        formatted_jobs.append({
            'num': str(idx + 1),
            'role': item['role'],
            'company': item['company'],
            'location': item['location'],
            'eligibility': eligibility,
            'skills': skills,
            'fit': fit,
            'platform': item['platform'],
            'link': item['link']
        })

    return formatted_jobs
