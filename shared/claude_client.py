import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "config" / ".env")

MODEL = "claude-opus-4-7"


def load_system_prompt(agent_md_path: str) -> str:
    path = Path(agent_md_path)
    if not path.exists():
        return ""
    content = path.read_text()
    if "## System Prompt" in content:
        return content.split("## System Prompt", 1)[-1].strip()
    return content


def make_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in config/.env")
    return anthropic.Anthropic(api_key=api_key)


def chat(
    client: anthropic.Anthropic,
    system_prompt: str,
    user_message: str,
    thinking: bool = False,
) -> str:
    kwargs = {
        "model": MODEL,
        "max_tokens": 16000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }
    if thinking:
        kwargs["thinking"] = {"type": "adaptive"}

    with client.messages.stream(**kwargs) as stream:
        return stream.get_final_message().content[0].text
