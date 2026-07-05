import subprocess
from pathlib import Path
from indigo.core.storage import REPO_DIR, init_storage

def run_git(cmd: str, cwd=REPO_DIR):
    """Executes a git command silently."""
    subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)

def clone_repo(repo_url: str):
    REPO_DIR.parent.mkdir(parents=True, exist_ok=True)
    # If the folder exists but is empty, or doesn't exist, clone it
    if not REPO_DIR.exists():
        subprocess.run(f"git clone {repo_url} {REPO_DIR}", shell=True)
    init_storage()
    sync_push() # Push the initial skeleton if new

def sync_pull():
    if REPO_DIR.exists():
        run_git("git pull --rebase origin main")

def sync_push():
    if REPO_DIR.exists():
        run_git("git add data.json")
        run_git('git commit -m "indigo: update list"')
        run_git("git push origin main")