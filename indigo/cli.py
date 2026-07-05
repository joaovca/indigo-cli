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

@app.command()
def add(url: str, category: str = "inbox"):
    """Insert a standard link metadata node to targeted categories."""
    git_manager.sync_pull()
    data = storage.load_data()
    
    if category not in data:
        data[category] = []
        
    new_item = storage.create_item(url)
    data[category].append(new_item)
    
    storage.save_data(data)
    git_manager.sync_push()
    console.print(f"✅ Added [bold blue]{url}[/bold blue] into target list [bold green]{category}[/bold green].")

@app.command()
def list(category: str = typer.Argument("inbox", help="Target category to search through")):
    """Render items residing in selected arrays."""
    git_manager.sync_pull()
    data = storage.load_data()
    
    if category not in data or not data[category]:
        console.print(f"📭 Nothing found in list container: [bold yellow]{category}[/bold yellow].")
        return

    console.print(f"\n📂 [bold green]{category.upper()}[/bold green]")
    for item in data[category]:
        console.print(f" - [{item['id']}] {item['title']}")

if __name__ == "__main__":
    app()