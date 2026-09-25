from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import BaseModel
from typing import Literal, Annotated
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
import json

mcp = FastMCP(
    name="Todo",
    instructions=(
        "A simple todo list. Use create_todo, list_todos, get_todo,"
        "update_todo, and delete_todo to manage your todos."
    )
)

Status = Literal["pending", "completed", "deleted"]

STORE_PATH = Path(__file__).with_name("todos.json") # local file to store the todos 

class Todo(BaseModel):
    id: str
    title: str
    description: str = ""
    status: Status = "pending"
    created_at:str
    updated_at:str


def _now()->str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _save(todos:dict[str, Todo]) -> None: # convert the todos to a dictionary of strings and todos
    STORE_PATH.write_text(
        json.dumps(
            [todo.model_dump() for todo in todos.values()],
            indent=2 + "\n"
        )
    )


def _load() -> dict[str, Todo]:
    if not STORE_PATH.exists():
        return {}
    rows = json.loads(STORE_PATH.read_text() or "[]")
    return { item["id"]: Todo.model_validate(item) for item in rows}

def _get_or_raise(todo_id:str) -> tuple[dict[str, Todo], bool]:
    todos = _load()
    todo = todos.get(todo_id)
    if todo is None:
     raise ValueError(f"Todo with id {todo_id} not found")
    return todos, todo


def create_todo(
    title:Annotated[str, "Short title for the todo"],
    description:Annotated[str, "Optional long description"]="",
    status:Annotated[Status, "pending, completed, or deleted"]="pending",
    ) -> Todo | None: 
    """
    Create a todo and return it.
    """

    title = title.strip()
    if not title:
        raise ToolError("Title can't be empty")

    now = _now()
    todo = Todo(
        id=uuid4().hex[:8],
        title=title,
        description=description,
        status=status,
        created_at=now,
        updated_at=now,
    )

