import datetime
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict


@dataclass
class Error:
    """Shop Error."""

    code: int
    message: str


@dataclass
class CeleryTaskResult:
    """A data class representing the result of a Celery task."""

    task_id: str
    issue_title: str
    issue_reason: str
    issue_state: str
    issued_at: datetime.datetime
    total_retries: int = 0
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def set_kwargs(self, **kwargs):
        """Sets the keyword arguments for the task."""
        self.kwargs = kwargs

    def to_json(self) -> str:
        """Serializes the CeleryTaskResult object to a JSON string."""
        data = asdict(self)
        data["issued_at"] = self.issued_at.strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(data, indent=4)

    @staticmethod
    def from_json(json_str: str) -> "CeleryTaskResult":
        """Deserializes a JSON string to a CeleryTaskResult object."""
        data = json.loads(json_str)
        data["issued_at"] = datetime.datetime.strptime(
            data["issued_at"], "%Y-%m-%d %H:%M:%S"
        )
        return CeleryTaskResult(**data)

    def __str__(self):
        """Returns the JSON string representation of the CeleryTaskResult
        object."""
        return self.to_json()
