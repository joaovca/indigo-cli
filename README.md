# Indigo CLI 🟣

> An opinionated, Git-synchronized study list manager that cures the "Bookmark Graveyard."

Most people use read-it-later apps to passively hoard links they will never look at again. **Indigo** introduces "mindful friction." It acts as a staging ground for your learning resources, forcing you to define the *intent* behind a saved link before it gets organized into your active projects.

Because Indigo uses a private Git repository as its backend, your study list is perfectly synchronized across your personal and work computers—with zero database costs, no API keys, and no hosting required.

---

## ⚡ Features

* **The Mindful Pipeline:** An interactive terminal UI that forces you to answer *why* you saved a link and *what* you expect to learn before it leaves your inbox.
* **Invisible Git Synchronization:** Operates a headless Git loop in the background. Every time you add an item or run the pipeline, Indigo automatically pulls, commits, and pushes to a private repository. 
* **Zero-Infrastructure:** No cloud database or web server required. Your data lives in a standard `data.json` file backed by Git.
* **Terminal Native:** Built with modern Python CLI libraries for a beautiful, keyboard-navigable interface.

---

## 🛠️ Installation

You can install Indigo globally on your machine directly from this repository using `pip` or `pipx` (recommended):

```bash
# Using pipx (Recommended for isolated global CLIs)
pipx install git+[https://github.com/joaovca/indigo-cli.git](https://github.com/joaovca/indigo-cli.git)

# Or using standard pip
pip install git+[https://github.com/joaovca/indigo-cli.git](https://github.com/joaovca/indigo-cli.git)
```

---

## 🚀 Quick Start

### 1. Authentication & Setup
Create an empty private repository on GitHub, then link your CLI to it. This sets up the background bridge.

```bash
indigo auth git@github.com:YOUR_USERNAME/YOUR-PRIVATE-REPO.git
```

### 2. The Inbox
Whenever you find an article, video, or repository you want to study later, add it to your inbox. Indigo will automatically sync it to your remote repository.

```bash
indigo add "[https://youtube.com/watch?v=xpto](https://youtube.com/watch?v=xpto)"
```

### 3. The Pipeline (The Core Loop)
When you are ready to organize your learning, run the pipeline. Indigo will pop the oldest item from your inbox and walk you through an interactive assessment:

```bash
indigo pipeline
```
* **O que chamou atenção?** (What caught your attention?)
* **O que você espera aprender?** (What do you expect to learn?)
* **Prioridade:** (High / Medium / Low)
* **Prazo:** (Optional deadline)
* **Destino:** (Target category, e.g., `tech-basics`, `product-design`)

### 4. Review Your Lists
View the items you've committed to studying, cleanly categorized.

```bash
indigo list product-design
```

### 5. Managing Lists and Links
Indigo allows strict structural control over your environments.

```bash
# View all categories and item counts
indigo lists

# Explicitly create an empty study list
indigo create-list product-design

# Track deadlines added during the pipeline phase
indigo dates

# Clean up unwanted resources
indigo delete-link product-design <ITEM_ID>
indigo delete-list product-design

---

## 🏗️ Architecture & Tech Stack

Indigo is built to be fast, cross-platform, and easily extensible.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Routing** | `Typer` | Handles command parsing and argument validation natively using Python type hints. |
| **Terminal UI** | `Rich` & `InquirerPy` | Provides colored outputs, formatted text, and interactive keyboard-navigated menus. |
| **Persistence** | `JSON` | Data is stored in `~/.indigo/repo/data.json` for lightweight, human-readable storage. |
| **Synchronization** | `subprocess` & `Git` | Automates `git pull --rebase`, `git commit`, and `git push` hooks silently during standard CLI operations to maintain state across multiple devices. |

---

## 🗺️ Roadmap (V2)

- [ ] **Auto-Metadata Extraction:** Fetch the `<title>` tag from the URL automatically during the `add` command.
- [ ] **SQLite Migration:** Transition from `data.json` to a local SQLite database for advanced querying and deadline sorting.
- [ ] **Export to Markdown:** Generate automated study notes skeletons from the pipeline metadata.

---

*Designed and engineered by João Clasen.*
