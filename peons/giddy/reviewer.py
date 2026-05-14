import subprocess

from peons.base_peon import BasePeon
from shared.task import Task, TaskStatus

GH = "/opt/homebrew/bin/gh"


class Giddy(BasePeon):
    def __init__(self):
        super().__init__("GIDY")

    async def start(self):
        self.active = True
        print(f"[{self.session_id}] Online — GitHub operations ready")

    async def stop(self):
        self.active = False
        print(f"[{self.session_id}] Offline")

    async def handle_task(self, task: Task):
        action = task.payload.get("action")
        if action == "review_pr":
            await self._review_pr(task)
        elif action == "create_pr":
            await self._create_pr(task)
        elif action == "request_changes":
            await self._request_changes(task)
        else:
            print(f"[GIDY] Unknown action: {action}")

    async def _review_pr(self, task: Task):
        pr = task.payload.get("pr_number")
        repo = task.payload.get("repo")
        body = task.payload.get("body", "Reviewed by GIDY.")
        task.update_status(TaskStatus.IN_PROGRESS)
        result = subprocess.run(
            [GH, "pr", "review", str(pr), "--repo", repo, "--approve", "--body", body],
            capture_output=True, text=True
        )
        print(f"[GIDY] {result.stdout or result.stderr}")
        task.update_status(TaskStatus.COMPLETED)

    async def _create_pr(self, task: Task):
        repo = task.payload.get("repo")
        title = task.payload.get("title")
        body = task.payload.get("body", "")
        base = task.payload.get("base", "main")
        task.update_status(TaskStatus.IN_PROGRESS)
        result = subprocess.run(
            [GH, "pr", "create", "--repo", repo, "--title", title, "--body", body, "--base", base],
            capture_output=True, text=True
        )
        print(f"[GIDY] {result.stdout or result.stderr}")
        task.update_status(TaskStatus.COMPLETED)

    async def _request_changes(self, task: Task):
        pr = task.payload.get("pr_number")
        repo = task.payload.get("repo")
        body = task.payload.get("body", "Changes requested by GIDY.")
        task.update_status(TaskStatus.IN_PROGRESS)
        result = subprocess.run(
            [GH, "pr", "review", str(pr), "--repo", repo, "--request-changes", "--body", body],
            capture_output=True, text=True
        )
        print(f"[GIDY] {result.stdout or result.stderr}")
        task.update_status(TaskStatus.COMPLETED)
