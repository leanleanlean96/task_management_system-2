# Task Management Platform

A small task-management platform demonstrating encapsulation and invariant
protection in a domain model. Tasks can be loaded from JSONL files or piped in
over stdin, validated via custom descriptors and `@property`, and printed to
the terminal.

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
    is_completed: bool                # True when completion_date is set
    status: Literal["Created", "Completed"]
```

Invariants enforced on every construction path:

- `completion_date`, when set, must not precede `creation_date`.

---

## Input formats

Tasks can be loaded from 3 sources.

### JSONL file (`--jsonl PATH`)

One JSON object per line, matching the fields above:

```json
{"id": "c9b1e4a2-3f8a-4b7d-8e1c-5f9a2b8c7d6e", "title": "Scout the dragon's lair", "description": "Map the entrances from the ridge.", "priority": 3, "creation_date": "2026-03-23T20:15:00", "completion_date": null}
```

### Stdin (`--stdin`)

One task per line, `;`-separated:

```
title;description;priority[;creation_date[;completion_date]]
```

- `title`, `description`, `priority` — required.
- `creation_date`, `completion_date` — optional; leave empty or omit trailing fields.
- Dates are ISO 8601.
- `id` is generated automatically — users don't supply it.

### Generated with in-build command

Tasks can be generated with in-build TaskGenerator class (see below)

---

## Examples

### Loading from JSONL

Input file `tasks.jsonl`:

```jsonl
{"id":"c9b1e4a2-3f8a-4b7d-8e1c-5f9a2b8c7d6e","title":"Scout the dragon's lair","description":"Map the entrances from the ridge.","priority":3,"creation_date":"2026-03-23T20:15:00","completion_date":null}
{"id":"a1b2c3d4-5e6f-4a7b-8c9d-0e1f2a3b4c5d","title":"Broker peace with the druids","description":"Meet the grove's emissary at the standing stones.","priority":2,"creation_date":"2026-03-23T19:30:00","completion_date":"2026-03-23T19:45:00"}
{"id":"b2c3d4e5-6f7a-4b8c-9d0e-1f2a3b4c5d6e","title":"Cleanse the cursed well","description":"Descend into the old village well.","priority":2,"creation_date":"2026-03-23T21:00:00","completion_date":"2026-03-23T20:00:00"}
```

Command:

```bash
poetry run python -m src.main read --jsonl tasks.jsonl
```

Output:

```
----------------------------------------
Task: Scout the dragon's lair
short_id: c9b1e4a2
description: Map the entrances from the ridge.
status: Not Completed
created at: 2026-03-23 20:15:00
completed at: None
----------------------------------------
----------------------------------------
Task: Broker peace with the druids
short_id: a1b2c3d4
description: Meet the grove's emissary at the standing stones.
status: Completed
created at: 2026-03-23 19:30:00
completed at: 2026-03-23 19:45:00
----------------------------------------
Skipping task at line 3: completion_date can't be before creation_date
```

The third record violates the ordering invariant and is skipped; the loader
continues normally.

### Loading from stdin

Command:

```bash
poetry run python -m src.main read --stdin
```
Input:

```
Retrieve the stolen relic;Recover the temple relic from the bandit camp.;3
Cleanse the cursed well;Descend and destroy the taint.;4;2026-03-20T09:00:00;2026-03-22T17:30:00
```

Output:

```
----------------------------------------
Task: Retrieve the stolen relic
short_id: 7f3a2b1c
description: Recover the temple relic from the bandit camp.
status: Not Completed
created at: 2026-04-12 13:16:42.367941+00:00
completed at: None
----------------------------------------
----------------------------------------
Task: Cleanse the cursed well
short_id: 4d8e9a01
description: Descend and destroy the taint.
status: Completed
created at: 2026-03-20 09:00:00
completed at: 2026-03-22 17:30:00
----------------------------------------
```

### Generating tasks with TaskGenerator

Command:

```bash
poetry run python -m src.main read --gen
```

Output:

```
----------------------------------------
Task: Clear the goblin ambush
short_id: 1fa11571
description: Gather your party, prepare supplies, and see the contract through to its end.
status: Completed
priority: 4
created at: 2026-03-01 11:00:00
completed at: 2026-03-12 15:00:00
----------------------------------------
----------------------------------------
Task: Clear the goblin ambush
short_id: 8387a751
description: Accept the commission from the guild and return once the work is done.
status: Completed
priority: 5
created at: 2026-03-01 11:00:00
completed at: 2026-03-20 17:00:00
----------------------------------------

Total: 2
```
### Error handling

Malformed inputs are skipped with an informative message, not fatal.

```
;;3
```
→ `Skipping task at line 1: title must not be empty`

```
Scout the dragon's lair;Map the ridge.;abc
```
→ `Skipping task at line 1: invalid literal for int() with base 10: 'abc'`

```
Clear the goblin ambush;Handle the raiders.;2;2026-03-25T10:00:00;2026-03-24T10:00:00
```
→ `Skipping task at line 1: completion_date can't be before creation_date`

---



## Dependencies
This project uses poetry for dependencies management, so you must have it installed.
Install dependencies:

```bash
poetry install
```