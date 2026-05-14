import subprocess
from pathlib import Path

_CLAUDE = "/Users/exelzero/.local/bin/claude"


def load_system_prompt(agent_md_path: str) -> str:
    path = Path(agent_md_path)
    if not path.exists():
        return ""
    content = path.read_text()
    if "## System Prompt" in content:
        return content.split("## System Prompt", 1)[-1].strip()
    return content


def run(system_prompt: str, user_message: str) -> str:
    prompt = f"{system_prompt}\n\n---\n\n{user_message}" if system_prompt else user_message
    result = subprocess.run(
        [_CLAUDE, "-p", prompt],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "claude exited non-zero")
    return result.stdout.strip()
