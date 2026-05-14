from abc import ABC, abstractmethod

from shared.claude_runner import load_system_prompt, run as claude_run
from shared.session import new_session_id
from shared.task import Task


class BasePeon(ABC):
    AGENT_MD: str = ""

    def __init__(self, name: str):
        self.name = name
        self.session_id = new_session_id(name)
        self.active = False
        self._system_prompt = load_system_prompt(self.AGENT_MD) if self.AGENT_MD else ""

    async def think(self, prompt: str, use_thinking: bool = False) -> str:
        return claude_run(self._system_prompt, prompt)

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
