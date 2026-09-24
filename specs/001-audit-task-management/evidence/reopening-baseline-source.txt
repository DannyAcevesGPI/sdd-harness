from dataclasses import dataclass, replace


class IdentityRequiredError(ValueError):
    pass


class InvalidTitleError(ValueError):
    pass


class TaskUnavailableError(ValueError):
    pass


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    owner_id: str
    status: str


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    @staticmethod
    def _require_actor(actor_id: str) -> None:
        if not isinstance(actor_id, str) or not actor_id.strip():
            raise IdentityRequiredError("Valid actor identity required")

    def create_task(self, *, actor_id: str, title: str) -> Task:
        self._require_actor(actor_id)
        if not isinstance(title, str) or not title.strip():
            raise InvalidTitleError("Valid title required")
        task = Task(self._next_id, title.strip(), actor_id, "PENDING")
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(self, *, actor_id: str) -> list[Task]:
        self._require_actor(actor_id)
        return [task for task in self._tasks.values() if task.owner_id == actor_id]

    def complete_task(self, *, actor_id: str, task_id: int) -> Task:
        self._require_actor(actor_id)
        if isinstance(task_id, bool) or not isinstance(task_id, int) or task_id <= 0:
            raise TaskUnavailableError("Task unavailable")
        task = self._tasks.get(task_id)
        if task is None or task.owner_id != actor_id:
            raise TaskUnavailableError("Task unavailable")
        completed = replace(task, status="COMPLETED")
        self._tasks[task_id] = completed
        return completed
