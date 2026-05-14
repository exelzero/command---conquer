import subprocess
from pathlib import Path

from peons.base_peon import BasePeon
from shared.task import Task, TaskStatus

GH = "/opt/homebrew/bin/gh"
_AGENT_MD = Path(__file__).parent / "AGENT.md"


class Giddy(BasePeon):
    AGENT_MD = str(_AGENT_MD)

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
        dispatch = {
            "review_pr": self._review_pr,
            "create_pr": self._create_pr,
            "request_changes": self._request_changes,
        }
        handler = dispatch.get(action)
        if handler:
            await handler(task)
        else:
            print(f"[GIDY] Unknown action: {action}")

    async def _review_pr(self, task: Task):
        pr = task.payload.get("pr_number")
        repo = task.payload.get("repo")
        task.update_status(TaskStatus.IN_PROGRESS)

        diff = self._get_pr_diff(repo, pr)
        if not diff:
            print(f"[GIDY] Could not fetch diff for PR #{pr}")
            task.update_status(TaskStatus.FAILED)
            return

        review_body = await self.think(
            f"Review this pull request diff and provide constructive feedback:\n\n{diff}",
            use_thinking=True,
        )

        result = subprocess.run(
            [GH, "pr", "review", str(pr), "--repo", repo, "--comment", "--body", review_body],
            capture_output=True, text=True,
        )
        print(f"[GIDY] PR #{pr} reviewed: {result.stdout or result.stderr}")
        task.update_status(TaskStatus.COMPLETED)

    async def _create_pr(self, task: Task):
        repo = task.payload.get("repo")
        title = task.payload.get("title", "")
        body = task.payload.get("body", "")
        base = task.payload.get("base", "main")
        task.update_status(TaskStatus.IN_PROGRESS)
        result = subprocess.run(
            [GH, "pr", "create", "--repo", repo, "--title", title,
             "--body", body, "--base", base],
            capture_output=True, text=True,
        )
        print(f"[GIDY] PR created: {result.stdout or result.stderr}")
        task.update_status(TaskStatus.COMPLETED)

    async def _request_changes(self, task: Task):
        pr = task.payload.get("pr_number")
        repo = task.payload.get("repo")
        body = task.payload.get("body", "Changes requested by GIDY.")
        task.update_status(TaskStatus.IN_PROGRESS)
        result = subprocess.run(
            [GH, "pr", "review", str(pr), "--repo", repo,
             "--request-changes", "--body", body],
            capture_output=True, text=True,
        )
        print(f"[GIDY] Changes requested on PR #{pr}: {result.stdout or result.stderr}")
        task.update_status(TaskStatus.COMPLETED)

    def _get_pr_diff(self, repo: str, pr_number: int) -> str:
        result = subprocess.run(
            [GH, "pr", "diff", str(pr_number), "--repo", repo],
            capture_output=True, text=True,
        )
        return result.stdout if result.returncode == 0 else ""
