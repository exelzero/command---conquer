import itertools
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

_counter = itertools.count(1)


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    creator: str
    assignee: str
    payload: dict
    id: str = field(init=False)
    status: TaskStatus = field(default=TaskStatus.PENDING)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        seq = next(_counter)
        self.id = f"TSK-{seq:04d}-{self.creator}"

    def update_status(self, status: TaskStatus):
        self.status = status
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "creator": self.creator,
            "assignee": self.assignee,
            "status": self.status.value,
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
