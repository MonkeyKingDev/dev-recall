from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import DataTable, Footer, Header, Input, Static

from dev_recall.recall.log import get_recent_logs
from dev_recall.recall.query import ask_local_llm


class LogViewer(App):
    CSS_PATH = "./style.css"

    query_mode = reactive(False)
    logs = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Type a filter or `/ask your question`", id="search")
        yield DataTable(id="log-table")
        yield Static("", id="status")
        yield Footer()

    def on_mount(self):
        self.logs = get_recent_logs(200)
        table = self.query_one("#log-table", DataTable)
        table.add_columns("Timestamp", "Command")
        self.load_logs(self.logs)

    def load_logs(self, logs):
        table = self.query_one("#log-table", DataTable)
        table.clear()
        for entry in logs:
            parts = entry.split("] $ ")
            if len(parts) == 2:
                ts = parts[0][1:]
                cmd = parts[1]
                table.add_row(ts, cmd)

    def on_input_submitted(self, event: Input.Submitted):
        text = event.value.strip()
        status = self.query_one("#status", Static)

        if text.startswith("/ask"):
            question = text[4:].strip()
            status.update("🧠 Thinking...")
            response = ask_local_llm(question)
            status.update("💬 " + response)
        else:
            filtered = [log for log in self.logs if text.lower() in log.lower()]
            self.load_logs(filtered)
            status.update(f"🔎 Showing {len(filtered)} results")


def main():
    app = LogViewer()
    app.run()
