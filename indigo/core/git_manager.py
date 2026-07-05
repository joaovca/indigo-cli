import subprocess
from pathlib import Path
from indigo.core.storage import REPO_DIR, init_storage
import sys
import shutil

def run_git(cmd: str, cwd=REPO_DIR):
    """Executes a git command silently."""
    subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)

def clone_repo(repo_url: str):
    """Performs downstream target download and sets schema files."""
    REPO_DIR.parent.mkdir(parents=True, exist_ok=True)
    
    if not REPO_DIR.exists():
        # Notice we removed capture_output=True so we can see the terminal prompts if Git needs them
        result = subprocess.run(f"git clone {repo_url} {REPO_DIR}", shell=True)
        
        if result.returncode != 0:
            print("\n❌ [ERROR] Git clone failed. Check your repository URL or permissions.")
            # Clean up the broken folder so we can try again later
            if REPO_DIR.exists():
                shutil.rmtree(REPO_DIR)
            sys.exit(1) # Stop the program immediately
            
    init_storage()
    sync_push()

def sync_pull():
    if REPO_DIR.exists():
        run_git("git pull --rebase origin main")

def sync_push():
    if REPO_DIR.exists():
        run_git("git add data.json")
        run_git('git commit -m "indigo: update list"')
        run_git("git push origin main")