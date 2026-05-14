import asyncio

from peons.base_peon import BasePeon
from shared.task import Task, TaskStatus


class DevWorker(BasePeon):
    async def start(self):
        self.active = True
        print(f"[{self.session_id}] Online")

    async def stop(self):
        self.active = False
        print(f"[{self.session_id}] Offline")

    async def handle_task(self, task: Task):
        print(f"[{self.session_id}] Starting {task.id}")
        task.update_status(TaskStatus.IN_PROGRESS)
        await asyncio.sleep(1)  # placeholder for real work
        task.update_status(TaskStatus.COMPLETED)
        print(f"[{self.session_id}] Completed {task.id}")
