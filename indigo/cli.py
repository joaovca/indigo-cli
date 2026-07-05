import sys
import os
import typer
from rich.console import Console
sys.path.append(os.path.abspath("."))
from indigo.core import storage, git_manager

app = typer.Typer(help="Indigo: Async Study List Manager")
console = Console()

@app.command()
def auth(repo_url: str = typer.Argument(..., help="Your private GitHub repository tracking URL")):
    """Connect a private GitHub tracking repository as your persistent back-end cloud space."""
    console.print(f"🔄 Setting up bridge to [bold blue]{repo_url}[/bold blue]...")
    git_manager.clone_repo(repo_url)
    console.print("✅ [bold green]Authenticated and synchronized structural nodes successfully![/bold green]")

if __name__ == "__main__":
    app()