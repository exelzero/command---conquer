from shared.naming import assign_name
from shared.task import Task, TaskStatus


class CommandCenter:
    def __init__(self, wire):
        self.wire = wire
        self.wire.set_cc(self)
        self.tasks: dict[str, Task] = {}

    async def dispatch(self, assignee: str, payload: dict) -> Task:
        task = Task(creator="CC", assignee=assignee, payload=payload)
        self.tasks[task.id] = task
        await self.wire.route(task)
        return task

    async def on_task_update(self, task: Task):
        self.tasks[task.id] = task
        print(f"[CC] {task.id} → {task.status.value}")

    def spawn_worker(self) -> str:
        from peons.devworker.worker import DevWorker
        name = assign_name()
        worker = DevWorker(name)
        self.wire.register(worker)
        return name

    def task_status(self, task_id: str) -> dict:
        task = self.tasks.get(task_id)
        if not task:
            return {"error": f"{task_id} not found"}
        return task.to_dict()

    def all_tasks(self) -> list:
        return [t.to_dict() for t in self.tasks.values()]
