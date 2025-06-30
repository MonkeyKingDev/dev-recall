import os
from pathlib import Path

import typer

import dev_recall.scripts.setup_ollama
from dev_recall.recall.query import ask_local_llm
from dev_recall.recall.tui import main as run_tui

cli = typer.Typer()


HOOK_CONTENT = """#!/usr/bin/env bash
# dev-recall-hook.sh

# where to write your log
export DEVRECALL_LOG="$HOME/.dev-recall/dev-recall.log"
mkdir -p "$(dirname "$DEVRECALL_LOG")"

_now() { date "+%Y-%m-%d %H:%M:%S"; }

if [ -n "$ZSH_VERSION" ]; then
  function preexec() {
    echo "$(_now) [ZSH] $1" >> "$DEVRECALL_LOG"
  }
elif [ -n "$BASH_VERSION" ]; then
  trap 'echo "$(_now) [BASH] $BASH_COMMAND" >> "$DEVRECALL_LOG"' DEBUG
fi
"""


@cli.command()
def install_hook():
    """Inject logging hook into shell profile, generating it if needed."""
    home = Path.home()
    rc_file = home / ".zshrc"
    target_dir = home / ".dev-recall"
    hook_file = target_dir / "dev-recall-hook.sh"

    # 1. Ensure target directory exists
    target_dir.mkdir(exist_ok=True)

    # 2. Write the hook script if it's not already there
    if not hook_file.exists():
        hook_file.write_text(HOOK_CONTENT)
        hook_file.chmod(0o755)
        typer.echo(f"✅ Created hook script at {hook_file}")
    else:
        typer.echo(f"✅ Hook script already exists at {hook_file}")

    # 3. Inject source line into ~/.zshrc
    source_line = f'source "{hook_file}"'
    contents = rc_file.read_text() if rc_file.exists() else ""
    if source_line not in contents:
        with rc_file.open("a") as f:
            f.write(f"\n# DevRecall Logging\n{source_line}\n")
        typer.echo(f"✅ Added source line to {rc_file}")
    else:
        typer.echo(f"✅ Source line already present in {rc_file}")


def ensure_setup():
    # Ollama check
    if os.system("ollama --version > /dev/null 2>&1") != 0:
        typer.echo("⚙️ Ollama not found. Running setup...")
        dev_recall.scripts.setup_ollama.main()


@cli.command()
def ask(
    message: str = typer.Argument(..., help="Ask from command history")  # noqa: B008
):
    ensure_setup()
    response = ask_local_llm(message)
    print(response)


@cli.command()
def tui():
    ensure_setup()
    run_tui()


def cli_entry():
    cli()


if __name__ == "__main__":
    cli()
