import os
from pathlib import Path
import yaml

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
ASSETS_DIR = PROJECT_ROOT / "assets"
ENV_FILE = PROJECT_ROOT / ".env"

OUTPUT_DIR.mkdir(exist_ok=True)

def load_env():
    """Loads environment variables from .env file without external dependencies."""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
                    os.environ[k.strip()] = v.strip()
    return env_vars

def load_profile():
    """Loads candidate matching profile."""
    profile_path = DATA_DIR / "profile.yaml"
    if profile_path.exists():
        with open(profile_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

ENV = load_env()
PROFILE = load_profile()
