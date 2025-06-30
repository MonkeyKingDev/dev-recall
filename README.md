# 🧠 Developer Daily Recall (`dev-recall`)

> A local-first productivity CLI tool that captures everything you do in the terminal — and lets you ask questions about it using local LLMs.

---

## ✨ Features

- 📝 Automatically logs every terminal command
- 🤖 Ask questions like:
  - “What were the Docker commands I used last week?”
  - “How did I set up Gunicorn?”
- 🔍 TUI interface to browse/search command history
- 🔒 100% local: no cloud APIs, no telemetry
- ⚙️ Uses Ollama with local models (e.g. `phi3`, `mistral`, `llama3`)
- 🪄 One-time shell integration — works in the background

---

## ⚡️ Quickstart

### 1. Install with Poetry (or Pipx)

```bash
pipx install git+https://github.com/mishra-ayush08/dev-recall
