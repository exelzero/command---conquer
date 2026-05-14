from abc import ABC, abstractmethod

from shared.session import new_session_id
from shared.task import Task


class BasePeon(ABC):
    def __init__(self, name: str):
        self.name = name
        self.session_id = new_session_id(name)
        self.active = False

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
