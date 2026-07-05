import sys
import os
import typer
from rich.console import Console
sys.path.append(os.path.abspath("."))
from indigo.core import storage, git_manager

app = typer.Typer(help="Indigo: Async Study List Manager")
console = Console()

@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """Indigo: Async Study List Manager"""
    if ctx.invoked_subcommand is None:
        console.print(r"""[bold blue]
 ___ _   _ ____ ___ ____  ___  
|_ _| \ | |  _ \_ _/ ___|/ _ \ 
 | ||  \| | | | | | |  _| | | |
 | || |\  | |_| | | |_| | |_| |
|___|_| \_|____/___\____|\___/ 
        [/bold blue]""")
        console.print("\n[bold]Welcome to Indigo![/bold] Run [cyan]indigo --help[/cyan] to see available commands.\n")

@app.command()
def auth(repo_url: str = typer.Argument(..., help="Your private GitHub repository tracking URL")):
    """Connect a private GitHub tracking repository as your persistent back-end cloud space."""
    console.print(f"🔄 Setting up bridge to [bold blue]{repo_url}[/bold blue]...")
    git_manager.clone_repo(repo_url)
    console.print("✅ [bold green]Authenticated and synchronized structural nodes successfully![/bold green]")

@app.command()
def add(url: str, category: str = typer.Argument("inbox", help="Target category to add to")):
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

from InquirerPy import inquirer
from datetime import datetime

@app.command()
def pipeline():
    """Run interactive evaluation parameters across unorganized Inbox nodes."""
    git_manager.sync_pull()
    data = storage.load_data()
    
    inbox = data.get("inbox", [])
    if not inbox:
        console.print("✨ Inbox zero reached! Nothing left to optimize.")
        return

    item = inbox.pop(0)
    console.print(f"\n🚀 [bold]Processing Node:[/bold] {item['url']}\n")

    # Collecting qualitative user choices via terminal prompts
    chamou_atencao = inquirer.text(message="O que chamou atenção?").execute()
    espera_aprender = inquirer.text(message="O que você espera aprender?").execute()
    prioridade = inquirer.select(
        message="Selecione a prioridade:",
        choices=["Alta", "Média", "Baixa"]
    ).execute()
    prazo = inquirer.text(message="Prazo opcional (YYYY-MM-DD ou deixe em branco):").execute()
    target_category = inquirer.text(message="Qual a categoria de destino? (ex: tech-basics):", default="geral").execute()

    # Mapping meta structural parameters
    item["pipeline"] = {
        "promoted_at": datetime.now().isoformat(),
        "motivo": chamou_atencao,
        "objetivo": espera_aprender,
        "prioridade": prioridade,
        "prazo": prazo if prazo else None
    }

    if target_category not in data:
        data[target_category] = []
    data[target_category].append(item)
    
    storage.save_data(data)
    git_manager.sync_push()
    console.print(f"\n✅ Successfully promoted and moved target resource downstream to [bold green]{target_category}[/bold green]!")

@app.command()
def lists():
    """Show all existing study lists and their item counts."""
    git_manager.sync_pull()
    data = storage.load_data()
    
    console.print("\n📁 [bold]Available Lists:[/bold]")
    for category_name, items in data.items():
        count = len(items)
        console.print(f" - [bold blue]{category_name}[/bold blue] ({count} items)")

if __name__ == "__main__":
    app()