# CodeK architecture

## 1. Session input

The user sends one coding-oriented request.

## 2. Planner

`Planner` turns the request into a small list of `Task` objects. In the default mode this is a deterministic heuristic, not an AI model.

An optional `LLMClient` exists separately so an actual provider can be connected later.

## 3. Task graph

`TaskGraph` stores dependencies. For example:

```text
inspect → understand → check → summary
```

A task becomes ready only after all of its dependencies are complete.

The graph uses dictionaries for fast task lookup and DFS-based cycle detection. It also supports topological ordering.

## 4. Scheduler

Ready tasks enter `PriorityScheduler`, which uses Python's `heapq`. This demonstrates a priority queue without creating a large framework around it.

## 5. Tools

`Workspace` contains a few tools that operate inside the selected project:

- list files
- read a file
- search text
- run a Python compile check

The path helper prevents `../` traversal outside the workspace.

## 6. Shared state

The runner keeps task status and results in memory during a run. Completed summaries are saved to SQLite.

## 7. API

FastAPI exposes:

- `GET /health`
- `POST /run`
- `GET /runs`

The Flutter client only talks to these endpoints.

## What this leaves out

The original project has many layers that are important for a real product but distract from the core learning goal: authentication, multiple model providers, streaming protocols, MCP, full terminal UI, patch parsing, operating-system sandboxes, approval policies, session rollout machinery, release tooling, and a large Rust workspace.

CodeK deliberately does not reproduce those systems.
