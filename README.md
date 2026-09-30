# CodeK

CodeK is a small coding-agent project inspired by the main idea behind OpenAI Codex CLI.

I built it as a student-sized version of a much larger coding agent. You give it a coding task, it makes a small plan, orders dependent steps, uses a few local tools, and saves the run so you can inspect what happened.


## What it does

A CodeK run looks roughly like this:

```text
User request
    ↓
Planner
    ↓
Task Graph
    ↓
Scheduler (priority queue)
    ↓
Tools
    ├── list files
    ├── read file
    ├── search text
    └── run safe Python commands
    ↓
Shared run state
    ↓
Saved result
```

The default demo mode does not need an API key. It uses a small rule-based planner and clearly labels that mode as a mock/heuristic mode. If an API key is supplied, the optional LLM client can ask an OpenAI-compatible chat endpoint for a plan.

## Why I built it

The original project is a large terminal coding agent. Reading the whole codebase at once hides the important ideas behind authentication, protocol types, UI code, sandbox implementations, integrations, streaming, and many production concerns.

CodeK keeps the part I can explain line by line:

- a coding-agent session
- a task/dependency graph
- topological ordering
- a priority queue for ready tasks
- a few tools
- a small LLM interface
- persistent run history
- a FastAPI API

## Main DSA concepts

- **Graph:** tasks are vertices and dependencies are directed edges.
- **Topological sort:** dependent tasks are not run before their prerequisites.
- **Queue / heap:** ready tasks are stored in a priority queue so higher-priority work is selected first.
- **Hash maps:** dictionaries are used for task lookup, file indexing, and run state.
- **DFS-style cycle detection:** the graph rejects circular dependencies.

## Python concepts

- classes and inheritance
- `dataclass`
- type hints
- enums
- exceptions
- file handling
- subprocesses
- SQLite
- FastAPI
- basic testing with pytest

## Project structure

```text
codeK/
├── README.md
├── .gitignore
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── models.py
│   │   │   ├── graph.py
│   │   │   └── runner.py
│   │   ├── dsa/
│   │   │   └── scheduler.py
│   │   ├── agents/
│   │   │   └── planner.py
│   │   ├── tools/
│   │   │   └── workspace.py
│   │   ├── llm/
│   │   │   └── client.py
│   │   ├── storage/
│   │   │   └── database.py
│   │   └── api/
│   │       └── routes.py
│   └── tests/
│       ├── test_graph.py
│       ├── test_scheduler.py
│       ├── test_tools.py
│       └── test_api.py
├── frontend/
│   ├── pubspec.yaml
│   └── lib/
│       ├── main.dart
│       ├── api.dart
│       └── screens/home_screen.dart
└── docs/
    └── architecture.md
```

## How to run the backend

Python 3.11+ is recommended.

```bash
cd backend
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API starts at `http://127.0.0.1:8000`.

Try:

```bash
curl http://127.0.0.1:8000/health
```

Then run a demo task:

```bash
curl -X POST http://127.0.0.1:8000/run   -H "Content-Type: application/json"   -d '{"prompt":"inspect this project and find Python files"}'
```

You can also use the CLI:

```bash
python -m app.main "inspect this project and find Python files"
```

## Optional LLM mode

CodeK does not require an LLM to run.

To use an OpenAI-compatible endpoint, set:

```bash
export CODEK_API_KEY="your-key"
export CODEK_BASE_URL="https://api.openai.com/v1"
export CODEK_MODEL="gpt-4o-mini"
```

The LLM client is deliberately small. It only asks for a JSON plan; CodeK still owns task ordering and tool execution.

## Tests

From `backend/`:

```bash
pytest -q
```

The tests cover graph construction, cycle detection, scheduling, workspace safety, and the API health endpoint.

## Current limitations

- The planner is intentionally small.
- The default mode does not generate or edit arbitrary code with an LLM.
- Only a small set of read/search/Python commands is allowed.
- There is no real operating-system sandbox like the original project.
- Authentication is intentionally absent.
- SQLite is used for simple local history.
- The Flutter app is a small client, not a full IDE.

## Possible future improvements

- Add an approval screen before a write operation.
- Add a proper patch/diff tool.
- Add more workspace search features.
- Add streaming task status.
- Add a richer LLM planner.
- Add session resume.
- Add a real sandbox after learning OS/process isolation.

This is a learning project, not a production coding agent.
