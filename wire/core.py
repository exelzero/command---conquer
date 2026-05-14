class Wire:
    def __init__(self):
        self._registry: dict = {}
        self._cc = None

    def set_cc(self, cc):
        self._cc = cc

    def register(self, peon):
        self._registry[peon.name] = peon
        print(f"[WIRE] Registered {peon.session_id}")

    def unregister(self, peon):
        self._registry.pop(peon.name, None)
        print(f"[WIRE] Unregistered {peon.session_id}")

    async def route(self, task):
        target = self._registry.get(task.assignee)
        if not target:
            print(f"[WIRE] No agent for '{task.assignee}' — task {task.id} dropped")
            return
        print(f"[WIRE] {task.id} → {task.assignee}")
        await target.handle_task(task)
        await self.report_to_cc(task)

    async def send(self, from_name: str, to_name: str, payload: dict):
        from shared.task import Task
        task = Task(creator=from_name, assignee=to_name, payload=payload)
        await self.route(task)
        return task

    async def report_to_cc(self, task):
        if self._cc:
            await self._cc.on_task_update(task)

    def agents(self) -> list:
        return [p.status() for p in self._registry.values()]
