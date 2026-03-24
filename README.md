# agent-events

> **Event bus and pub/sub system for multi-agent coordination.**  
> Zero infrastructure. Zero dependencies. Pure Python 3.10+.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Why agent-events?

Multi-agent systems need agents to communicate without tight coupling:

| Approach | Problem |
|---|---|
| Direct function calls | Tight coupling — Agent A must know about Agent B |
| Message queues (Redis, RabbitMQ) | Infrastructure dependency — extra ops overhead |
| Shared state (dict, DB) | Race conditions, mutex hell |
| **agent-events** ✅ | In-process pub/sub — zero infra, zero deps, thread-safe queue |

---

## Installation

```bash
pip install agent-events
```

Or from source:

```bash
git clone https://github.com/darshjme-codes/agent-events
cd agent-events
pip install -e ".[dev]"
```

---

## Quick Start — Multi-Agent Coordination

```python
from agent_events import Event, EventBus, EventFilter, EventHistory

# ── Shared infrastructure ────────────────────────────────────────────────────
bus     = EventBus()
history = EventHistory(max_size=500)

# ── Agent B: subscribes BEFORE Agent A runs ──────────────────────────────────
@EventFilter.where(source="agent-A", data_contains={"status": "done"})
def on_task_complete(event: Event) -> None:
    history.record(event)
    print(f"[Agent B] Task finished by {event.source}!")
    print(f"          Result: {event.data['result']}")
    print(f"          Event ID: {event.id}")

bus.subscribe("task.complete", on_task_complete)

# ── Agent A: publishes when done ─────────────────────────────────────────────
def agent_a_run() -> None:
    print("[Agent A] Processing …")
    result = sum(range(1_000_000))          # heavy computation

    bus.publish(Event(
        type   = "task.complete",
        source = "agent-A",
        data   = {"status": "done", "result": result},
    ))

agent_a_run()
```

**Output:**
```
[Agent A] Processing …
[Agent B] Task finished by agent-A!
          Result: 499999500000
          Event ID: 3f2e1d4c-…
```

Agent B is **automatically triggered** the moment Agent A publishes. No polling, no shared variables, no imports between agents.

---

## API Reference

### `Event`

```python
from agent_events import Event

evt = Event(
    type   = "task.complete",   # required
    data   = {"key": "value"},  # optional, default {}
    source = "agent-1",         # optional, default ""
    # timestamp and id are auto-generated
)

# Serialization
d   = evt.to_dict()
evt = Event.from_dict(d)
```

### `EventBus`

```python
from agent_events import EventBus, Event

bus = EventBus(max_queue_size=1000)

# Subscribe (higher priority = called first)
bus.subscribe("task.complete", handler, priority=10)

# Unsubscribe
bus.unsubscribe("task.complete", handler)

# Synchronous publish — returns number of handlers called
n = bus.publish(Event(type="task.complete", data={}))

# Async publish — returns immediately, queues for later
bus.publish_async(Event(type="task.complete", data={}))
bus.process_queue(max_events=100)

# Inspect
bus.subscriber_count("task.complete")   # → int

# Clear
bus.clear("task.complete")   # specific type
bus.clear()                  # all types
```

### `EventFilter`

```python
from agent_events import EventFilter, Event

# Filter by source
@EventFilter.where(source="agent-1")
def handler(event: Event) -> None: ...

# Filter by data content
@EventFilter.where(data_contains={"status": "done"})
def handler(event: Event) -> None: ...

# Filter by numeric priority field inside event.data
@EventFilter.where(min_priority=5)
def handler(event: Event) -> None: ...

# Composable — all conditions must match (AND)
@EventFilter.where(source="agent-1", data_contains={"type": "result"})
def handler(event: Event) -> None: ...
```

### `EventHistory`

```python
from agent_events import EventHistory, EventBus

history = EventHistory(max_size=500)

# Record events
history.record(event)

# Query (returns list[Event], oldest first)
events = history.query(event_type="task.complete", source="agent-1", limit=10)

# Replay stored events to a bus
history.replay(bus, event_type="task.complete")

# Statistics
s = history.stats()
# {
#   "total_recorded": 42,
#   "current_size":   42,
#   "by_type":        {"task.complete": 30, "task.error": 12},
#   "oldest_timestamp": 1711234567.123,
#   "newest_timestamp": 1711234599.456,
# }
```

---

## Advanced Example — Priority + Async Queue + History

```python
import time
from agent_events import Event, EventBus, EventFilter, EventHistory

bus     = EventBus()
history = EventHistory()

# Critical handler — runs first (priority=10)
@EventFilter.where(min_priority=8)
def critical_handler(event: Event) -> None:
    print(f"[CRITICAL] {event.type} from {event.source}")

# Logging handler — runs last (priority=0, default)
def log_handler(event: Event) -> None:
    history.record(event)

bus.subscribe("alert", critical_handler, priority=10)
bus.subscribe("alert", log_handler,      priority=0)

# Fire a high-priority alert asynchronously
bus.publish_async(Event(
    type   = "alert",
    source = "monitor",
    data   = {"priority": 9, "message": "CPU > 95%"},
))

# Process at a convenient time (e.g., end of main loop iteration)
bus.process_queue()

# Check what happened
print(history.stats())
```

---

## Running Tests

```bash
python -m pytest tests/ -v
# 53 tests, 0 failures
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please read our [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

MIT © Darshankumar Joshi
