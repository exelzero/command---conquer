from pathlib import Path

from peons.base_peon import BasePeon
from shared.task import Task, TaskStatus

_AGENT_MD = Path(__file__).parent / "AGENT.md"


class DevWorker(BasePeon):
    AGENT_MD = str(_AGENT_MD)

    async def start(self):
        self.active = True
        print(f"[{self.session_id}] Online")

    async def stop(self):
        self.active = False
        print(f"[{self.session_id}] Offline")

    async def handle_task(self, task: Task):
        print(f"[{self.session_id}] Starting {task.id}")
        task.update_status(TaskStatus.IN_PROGRESS)
        prompt = self._build_prompt(task)
        try:
            result = await self.think(prompt)
            print(f"[{self.session_id}] {task.id} result:\n{result[:300]}")
            task.update_status(TaskStatus.COMPLETED)
        except Exception as e:
            print(f"[{self.session_id}] {task.id} failed: {e}")
            task.update_status(TaskStatus.FAILED)

    def _build_prompt(self, task: Task) -> str:
        parts = [f"Task ID: {task.id}"]
        for key, value in task.payload.items():
            parts.append(f"{key.upper()}: {value}")
        return "\n".join(parts)
