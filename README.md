<div align="center">

<img src="assets/agent-events-hero.png" alt="agent-events — Vedic Arsenal by Darshankumar Joshi" width="100%" />

# ⚡ agent-events

<h3><em>लीला</em></h3>

> *Leela — the divine play of events*

**Event bus and pub/sub system for multi-agent coordination — priority handlers, async queue, event filtering, history replay. Zero dependencies.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=flat-square)](https://github.com/darshjme/agent-events)
[![Tests](https://img.shields.io/badge/Tests-Passing-success?style=flat-square)](https://github.com/darshjme/agent-events/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Vedic Arsenal](https://img.shields.io/badge/Vedic%20Arsenal-100%20libs-purple?style=flat-square)](https://github.com/darshjme/arsenal)

*Part of the [**Vedic Arsenal**](https://github.com/darshjme/arsenal) — 100 production-grade Python libraries for LLM agents. Zero dependencies. Battle-tested.*

</div>

---

## Overview

`agent-events` implements **event bus and pub/sub system for multi-agent coordination — priority handlers, async queue, event filtering, history replay. zero dependencies.**

Inspired by the Vedic principle of *लीला* (Leela), this library brings the ancient wisdom of structured discipline to modern LLM agent engineering.

No external dependencies. Pure Python 3.8+. Drop it in anywhere.

## Installation

```bash
pip install agent-events
```

Or clone directly:
```bash
git clone https://github.com/darshjme/agent-events.git
cd agent-events
pip install -e .
```

## How It Works

```mermaid
flowchart LR
    A[Publisher] --> B[Event Bus]
    B --> C[Handler 1]
    B --> D[Handler 2]
    B --> E[Handler 3]
    B --> F[History Replay]
    C & D & E --> G[Ack]
    style B fill:#f59e0b,color:#000
```

## Quick Start

```python
from events import *

# Initialize
# See examples/ for full usage patterns
```

## Why `agent-events`?

Production LLM systems fail in predictable ways. `agent-events` solves the **events** failure mode with:

- **Zero dependencies** — no version conflicts, no bloat
- **Battle-tested patterns** — extracted from real production systems
- **Type-safe** — full type hints, mypy-compatible
- **Minimal surface area** — one job, done well
- **Composable** — works with any LLM framework (LangChain, LlamaIndex, raw OpenAI, etc.)

## The Vedic Arsenal

`agent-events` is part of **[darshjme/arsenal](https://github.com/darshjme/arsenal)** — a collection of 100 focused Python libraries for LLM agent infrastructure.

Each library solves exactly one problem. Together they form a complete stack.

```
pip install agent-events  # this library
# Browse all 100: https://github.com/darshjme/arsenal
```

## Contributing

Found a bug? Have an improvement?

1. Fork the repo
2. Create a feature branch (`git checkout -b fix/your-fix`)
3. Add tests
4. Open a PR

All contributions welcome. Keep it zero-dependency.

## License

MIT — use freely, build freely.

---

<div align="center">

**Built with ⚡ by [Darshankumar Joshi](https://github.com/darshjme)** · [@thedarshanjoshi](https://twitter.com/thedarshanjoshi)

*"कर्मण्येवाधिकारस्ते मा फलेषु कदाचन"*
*Your right is to action alone, never to the fruits thereof.*

[Arsenal](https://github.com/darshjme/arsenal) · [GitHub](https://github.com/darshjme) · [Twitter](https://twitter.com/thedarshanjoshi)

</div>
