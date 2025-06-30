# 🧠 Developer Daily Recall (`dev-recall`)

[![Made with ❤️ Local-first](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20local--first-blue)](https://github.com/mishra-ayush08/dev-recall)
[![Powered by Ollama](https://img.shields.io/badge/Powered%20by-Ollama-green)](https://ollama.com)

> A local-first productivity CLI tool that captures everything you do in the terminal — and lets you ask questions about it using local LLMs.

---

## ✨ Features

- 📝 Automatically logs every terminal command in the background
- 🤖 Ask natural language questions like:
  - “What were the Docker commands I used last week?”
  - “How did I set up Gunicorn?”
  - “Give me an example of how to run a FastAPI app with Gunicorn”
- 🔍 TUI interface to browse/search command history
- 🔒 100% local:
  - No cloud APIs
  - No telemetry
  - Logs are stored locally in `recall.db`
- ⚙️ Uses Ollama with local models (`phi3`, `mistral`, `llama3`, etc.)
- 🪄 One-time shell integration — logs every command automatically

---

## ⚡️ Quickstart

### 1. Install via `pipx`

```bash
pipx install git+https://github.com/mishra-ayush08/dev-recall
```

### 2. Enable terminal command logging
```bash
dev-recall install-hook
source ~/.zshrc
```

### 3. Ask questions
```bash
dev-recall ask "What command did I use to create a virtualenv?"
dev-recall ask "Give me an example of using rsync with ssh"
```

### 4. Launch the TUI
```bash
dev-recall tui
```

