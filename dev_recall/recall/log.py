import re
from collections import deque
from pathlib import Path
from typing import Deque, Tuple

LOG_LINE_RE = re.compile(r"^(.+?)\s+\[.*?\]\s+(.*)$")

DEFAULT_LOG = Path.home() / ".dev-recall" / "dev-recall.log"


def get_recent_logs(n: int = 100, log_path: Path = DEFAULT_LOG) -> list[str]:
    """
    Return the last `n` entries from dev-recall.log as (timestamp, command)
    without hard-coding any lengths.
    """
    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    recent: Deque[Tuple[str, str]] = deque(maxlen=n)
    with log_path.open("r") as f:
        for line in f:
            line = line.rstrip("\n")
            m = LOG_LINE_RE.match(line)
            if m:
                ts, cmd = m.groups()
            else:
                # fallback if it doesn't match our expected format
                ts, cmd = "", line
            recent.append((ts, cmd))

    return [f"{ts} → {cmd}" for ts, cmd in recent]
