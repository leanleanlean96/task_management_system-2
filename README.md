# Task Management Platform

A highly efficient, iterator-based task management platform demonstrating encapsulation, domain model invariant protection, and lazy evaluation pipelines. 

Tasks can be loaded from multiple concurrent sources (JSONL files, stdin, or in-memory generators), validated via custom descriptors, lazily filtered without memory duplication, and printed to the terminal.

---

## Task structure

```python
class Task:
    id: str                           # UUID string, generated automatically, immutable
    title: str                        # non-empty
    description: str                  # may be empty; defaults to ""
    priority: int                     # 0 < priority < 6
    creation_date: datetime           # ISO 8601; automatically sets to now for new tasks
    completion_date: datetime | None  # None for uncompleted tasks

    short_id: str                     # first 8 chars of id
    is_completed: str                 # "Completed" if completion_date is set, else "Not Completed"
```

Invariants enforced on every construction path:

- `completion_date`, when set, must not precede `creation_date`.
- Identifiers (`id`) are strictly validated as actual UUIDs.
- `priority` must be an integer between 1 and 5.

---

## Input formats

The system can read and merge tasks from 3 different sources simultaneously. All sources stream data dynamically into a unified Task Queue.

### 1. JSONL file (`--jsonl PATH`)

One JSON object per line, matching the fields above:

```json
{"id": "c9b1e4a2-3f8a-4b7d-8e1c-5f9a2b8c7d6e", "title": "Scout the dragon's lair", "description": "Map the entrances from the ridge.", "priority": 3, "creation_date": "2026-03-23T20:15:00", "completion_date": null}
```

### 2. Stdin (`--stdin`)

One task per line, `;`-separated:

```text
title;description;priority[;creation_date[;completion_date]]
```

- `title`, `description`, `priority` — required.
- `creation_date`, `completion_date` — optional; leave empty or omit trailing fields.
- Dates are ISO 8601.
- `id` is generated automatically — users don't supply it.

### 3. Generated with in-build command (`--gen`)

Tasks can be dynamically generated with random properties using the built-in `TaskGenerator` class.

---

## Command Line Usage

### Basic Reading (Unified Stream)

Read tasks from a JSONL file:
```bash
poetry run python -m src.main read --jsonl tasks.jsonl
```

Read tasks from stdin:
```bash
poetry run python -m src.main read --stdin
```

### Lazy Filtering

The platform utilizes a custom Iterator state-machine and chained Generators to filter tasks with **zero memory overhead**. 

Filter tasks by a specific priority (1-5):
```bash
poetry run python -m src.main read --gen --priority 3
```

Filter tasks by completion status (1 for Completed, 0 for Not Completed):
```bash
poetry run python -m src.main read --jsonl tasks.jsonl --completed 1
```

---

## Examples

### Using filters on generated tasks

Command:

```bash
poetry run python -m src.main read --gen --priority 5
```

Output:

```text
----------------------------------------
Task: Retrieve the stolen relic
short_id: 8387a751
description: Handle the matter discreetly and bring proof of completion to claim the reward.
status: Completed
priority: 5
created at: 2026-03-01 11:00:00
completed at: 2026-03-20 17:00:00
----------------------------------------

Total: 1
```

### Loading from stdin

Command:

```bash
poetry run python -m src.main read --stdin
```
Input:

```text
Retrieve the stolen relic;Recover the temple relic from the bandit camp.;3
Cleanse the cursed well;Descend and destroy the taint.;4;2026-03-20T09:00:00;2026-03-22T17:30:00
```

Output:

```text
----------------------------------------
Task: Retrieve the stolen relic
short_id: 7f3a2b1c
description: Recover the temple relic from the bandit camp.
status: Not Completed
priority: 3
created at: 2026-04-12 13:16:42.367941+00:00
completed at: None
----------------------------------------
----------------------------------------
Task: Cleanse the cursed well
short_id: 4d8e9a01
description: Descend and destroy the taint.
status: Completed
priority: 4
created at: 2026-03-20 09:00:00
completed at: 2026-03-22 17:30:00
----------------------------------------

Total: 2
```

### Error handling

Malformed inputs are skipped with an informative message, and the iterator continues seamlessly to the next task.

```text
;;3
```
→ `Skipping task at line 1: title must not be empty`

```text
Clear the goblin ambush;Handle the raiders.;2;2026-03-25T10:00:00;2026-03-24T10:00:00
```
→ `Skipping task at line 1: completion_date can't be before creation_date`

```json
{"id": "not-a-uuid", "title": "Test", "creation_date": "2026-03-23T10:00:00"}
```
→ `Skipping task at line 1: id must be a valid UUID, got not-a-uuid`

---

## Dependencies
This project uses `poetry` for dependencies management, so you must have it installed.
Install dependencies:

```bash
poetry install
```

Run tests:
```bash
poetry run pytest
```