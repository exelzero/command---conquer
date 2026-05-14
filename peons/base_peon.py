from abc import ABC, abstractmethod
from pathlib import Path

from shared.claude_client import chat, load_system_prompt, make_client
from shared.session import new_session_id
from shared.task import Task


class BasePeon(ABC):
    AGENT_MD: str = ""

    def __init__(self, name: str):
        self.name = name
        self.session_id = new_session_id(name)
        self.active = False
        self._client = make_client()
        self._system_prompt = load_system_prompt(self.AGENT_MD) if self.AGENT_MD else ""

    async def think(self, prompt: str, use_thinking: bool = False) -> str:
        return chat(self._client, self._system_prompt, prompt, thinking=use_thinking)

    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def stop(self): ...

    @abstractmethod
    async def handle_task(self, task: Task): ...

    def status(self) -> dict:
        return {
            "name": self.name,
            "session_id": self.session_id,
            "active": self.active,
        }
