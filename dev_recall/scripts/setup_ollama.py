import platform
import shutil
import subprocess
import sys

SUPPORTED_MODELS = {
    "phi3": "phi3:medium",
    "mistral": "mistral",
    "llama3": "llama3:8b",
    "gemma": "gemma:2b",
}


def command_exists(cmd):
    return shutil.which(cmd) is not None


def detect_gpu():
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3"],
            input=b"Do you support GPU?",
            capture_output=True,
            timeout=10,
        )
        return "GPU" in result.stdout.decode()
    except Exception:
        return False


def install_ollama():
    system = platform.system()
    print(f"Detected OS: {system}")

    if system in ["Linux", "Darwin"]:
        print("Installing Ollama...")
        try:
            subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "-o", "install.sh"],
                check=True,
            )
            subprocess.run(["sh", "install.sh"], check=True)
        except Exception as e:
            print(f"⚠️ Failed to install Ollama: {e}")
            sys.exit(1)
    elif system == "Windows":
        print("⚠️ Please install Ollama manually: https://ollama.com/download")
        input("Press Enter after you’ve installed Ollama...")
    else:
        print(f"❌ Unsupported OS: {system}")
        sys.exit(1)


def pull_model(model_name):
    print(f"Pulling model: {model_name}")
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
    except Exception as e:
        print(f"⚠️ Failed to pull model '{model_name}': {e}")
        sys.exit(1)


def choose_model():
    print("📦 Available models:")
    for key, val in SUPPORTED_MODELS.items():
        print(f"  [{key}] → {val}")
    choice = (
        input("👉 Choose model to install [phi3/mistral/llama3/gemma] (default: phi3): ")
        .strip()
        .lower()
    )
    return SUPPORTED_MODELS.get(choice, SUPPORTED_MODELS["phi3"])


def main():
    if not command_exists("ollama"):
        print("❌ Ollama is not installed.")
        install_ollama()
    else:
        print("✅ Ollama is already installed.")

    model = choose_model()

    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, check=True)
        if model not in result.stdout.decode():
            pull_model(model)
        else:
            print(f"✅ Model '{model}' already installed.")
    except Exception as e:
        print(f"⚠️ Could not verify model: {e}")
        pull_model(model)

    print("🔍 Checking GPU support...")
    if detect_gpu():
        print("🚀 Ollama is using GPU acceleration.")
    else:
        print("⚠️ Ollama appears to be running on CPU only.")


if __name__ == "__main__":
    main()
