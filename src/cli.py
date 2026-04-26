from pathlib import Path
from typing import Any, Optional

import typer

from src.app.task_management_system import TaskManagementSystem
from src.task_sources.generator_data.data_lists import (
    completion_date_list,
    creation_date_list,
    description_list,
    name_list,
)
from src.task_sources.sources_list import SOURCES

app = typer.Typer(no_args_is_help=True)


@app.command("plugins")
def plugins_list() -> None:
    typer.echo("Available plugins:")
    for name in sorted(SOURCES):
        typer.echo(name)


def _build_sources(stdin: bool, generator: bool, jsonl: Path | None) -> list[Any]:
    sources: list[Any] = []
    if stdin:
        sources.append(SOURCES["stdin"]())
    if generator:
        sources.append(
            SOURCES["generator"](
                name_list, description_list, creation_date_list, completion_date_list
            )
        )
    if jsonl:
        sources.append(SOURCES["json"](jsonl))
    return sources


@app.command("read")
def read(
    stdin: bool = typer.Option(False, "--stdin", help="Read messages from stdin"),
    generator: bool = typer.Option(False, "--gen", help="Generate tasks"),
    jsonl: Optional[Path] = typer.Option(
        None,
        "--jsonl",
        help="Read messages from stdin",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    priority: Optional[int] = typer.Option(
        None,
        "--priority",
        help="Filter tasks by priority (1-5)",
        min=1,
        max=5,
    ),
    completed: Optional[int] = typer.Option(
        None,
        "--completed",
        help="Filter tasks to show only completed ones",
    ),
):
    raw_sources = _build_sources(stdin, generator, jsonl)
    inbox = TaskManagementSystem(raw_sources)
    numbers = 0
    for task in inbox.iter_tasks():
        task_completed = 1 if task.is_completed == "Completed" else 0
        if priority is not None and task.priority != priority:
            typer.echo("No tasks match the specified priority.")
            continue
        if completed is not None and task_completed != completed:
            typer.echo("No tasks match the specified completion status.")
            continue
        numbers += 1
        typer.echo(str(task))

    typer.echo(f"\nTotal: {numbers}")
