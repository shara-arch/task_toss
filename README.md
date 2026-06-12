# TaskTosser

A command-line project and task management tool for your every day taks to complex projects. 
Requesters post work; Helpers claim and complete it. All data persists locally in a JSON file.

---

## Features

- Two user roles: **Requester** (creates projects and tasks) and **Helper** (claims and completes tasks)
- Full task lifecycle: `Pending → In Progress → Completed`
- Role-based access control enforced at the model layer
- Local JSON persistence with automatic setup on first run
- 3 pytest suites and isolated fixtures

---

## Project Structure

```
task_toss/
├── main.py              # CLI entry point (argparse subcommands)
├── models/
│   ├── base.py          # Person base class (inherited by User)
│   ├── user.py          # User model + email validation
│   ├── project.py       # Project model
│   └── task.py          # Task model + status enforcement
├── utils/
│   └── persistence.py   # JSON read/write layer
├── data/
│   └── storage.json     # Auto-created on first run
├── tests/
|   └──test_app.py          # pytest test suite
└── Pipfile
```

---

## Requirements

- Python 3.12+
- `rich` (terminal output)
- `pytest` (development/testing)

Install dependencies:

```bash
# Using pip
pip install -r Pipfile

# Using pipenv
pipenv install
```

---

## Usage

```bash
** 1. Register users **
python3 main.py add-new-user -name Alexis -email alexis@gmail.com -role client
python3 main.py add-new-user -name Candy  -email candy@gmail.com  -role tasker

** 2. Create a project **
python3 main.py add-new-project -title "Website Rebuild" -user Alex -due 2026-09-01

** 3. Add tasks to the project **
python3 main.py add-task -title "Write tests" -project "Website Rebuild" 
python3 main.py add-task -title "Build API"   -project "Website Rebuild" 

** 4. Helper claims a task **
python3 main.py claim-task -title "Write tests" -project "Website Rebuild" user: Alexis

** 5. Helper marks it done **
python3 main.py complete-task -title "Write tests" -project "Website Rebuild" -user Candy

** 6. View Projects **
python3 main.py render-projects

```

---

## Commands

| Command | Description |
|---|---|
| `add-new-user` | Register a new user |
| `add-new-project` | Create a project workspace |
| `add-new-task` | Add a task to a project |
| `claim-task` | Claim a Pending task (Helpers only) |
| `complete-task` | Mark a task as Completed |
| `render-projects` | View all projects with task progress |

---
## Help Center
Every command supports `--help` for full argument details, e.g.:

```bash
python3 main.py add-new-user --help
python3 main.py add-new-project --help
python3 main.py add-new-task --help
python3 main.py claim-task --help


```

---

## Roles

| | Requester | Helper |
|---|---|---|
| Create projects | ✔ | x |
| Add tasks | ✔ | x |
| Claim tasks | x | ✔ |
| Complete tasks | (any task in their project) |  (only tasks they claimed) |
| View projects/tasks | ✔ | ✔ |

---

## Running Tests

```bash
pytest tests/test_app.py 
```

The test suite uses a temporary file fixture so your real data is never touched during test runs. All  tests cover email validation, user/project/task creation, role enforcement, and task lifecycle.

---

## Data Storage

Data is saved to `data/storage.json`, which is created automatically on first run. The file is plain JSON. Back it up or reset it by deleting it — the app rebuilds it from scratch on the next command.

---

## Author's details
 ** Author ** Sharon Moegi