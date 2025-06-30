import subprocess

from dev_recall.recall.log import get_recent_logs


def ask_local_llm(question: str):
    logs = "\n".join(get_recent_logs(50))
    prompt = f"""
    You are a helpful assistant for developers. Use the following terminal history:

    {logs}

    Now answer this question about the developer's command history:
    {question}
    """

    result = subprocess.run(
        ["ollama", "run", "phi3"], input=prompt.encode(), capture_output=True
    )
    return result.stdout.decode()
