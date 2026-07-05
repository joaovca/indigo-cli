import json
import uuid
from datetime import datetime
from pathlib import Path

INDIGO_DIR = Path.home() / ".indigo"
REPO_DIR = INDIGO_DIR / "repo"
DATA_FILE = REPO_DIR / "data.json"

def init_storage():
    """Creates the JSON file if it doesn't exist."""
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_data({"inbox": []})

def load_data() -> dict:
    if not DATA_FILE.exists():
        return {"inbox": []}
    return json.loads(DATA_FILE.read_text())

def save_data(data: dict):
    DATA_FILE.write_text(json.dumps(data, indent=2))

def create_item(url: str) -> dict:
    return {
        "id": str(uuid.uuid4())[:8],
        "url": url,
        "title": url, # In v2, an AI will fetch the real title
        "added_at": datetime.now().isoformat()
    }