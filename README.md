# Command & Conquer

A multi-agent AI orchestration system built in Python. CC commands, WIRE routes, peons execute.

---

## Architecture

```
┌──────────────────────────────────────────┐
│            COMMAND CENTER (CC)            │
│   strategy · task creation · oversight   │
└──────────────────┬───────────────────────┘
                   │ ↕ bidirectional
┌──────────────────▼───────────────────────┐
│                  WIRE                    │
│   switchboard · agent registry · router  │
│   routes all inter-agent messages        │
│   tracks sessions · delivers tasks       │
└────┬──────────┬──────────┬───────────────┘
     │          │          │
  ┌──▼──┐    ┌──▼──┐    ┌──▼──┐
  │BOLT │    │WREN │    │GIDY │
  │dev  │    │dev  │    │ PR  │
  └─────┘    └─────┘    └──┬──┘
                           │
                       GitHub API
                  (PRs · reviews · revisions)
                           │
                    ┌──────▼──────┐
                    │  Live Feed  │
                    │  monitor    │
                    └─────────────┘
```

---

## Agents

| Name | Type | Role |
|------|------|------|
| **CC** | Command Center | Master orchestrator — creates tasks, assigns peons, monitors outcomes |
| **WIRE** | Switchboard | Local message router — all agent comms flow through here |
| **GIDY** | GitHub Peon | PR creation, reviews, revision requests, approvals |
| **BOLT, WREN...** | DevWorker Peons | Persistent parallel workers — powered by Claude |

---

## Peon System

### Naming
DevWorker peons are assigned 4-letter anime names from a shared pool:

```
GOJO  DEKU  BAKU  TOGA  DABI  HAWK  TOGE  YUJI
DOMA  ZENI  RENG  NEZU  ASTA  YUNO  NERO  TANJ
KIRI  IIDA  GOKU  ZORO  NAMI  LEVI  EREN  YMIR
REVY  HIEI  MAKA  SOUL  FAYE  RIZA
```

### Session IDs
Each peon gets a unique session ID on spawn:
```
BOLT#a3f2b1c4
WREN#99de3102
```
If a peon dies and respawns, it gets a fresh session ID.

### Task IDs
All tasks carry a unique, human-readable ID:
```
TSK-{sequence:04d}-{creator}
```
Examples:
- `TSK-0001-CC` — task 1, created by Command Center
- `TSK-0042-BOLT` — task 42, created by BOLT
- `TSK-0043-GIDY` — task 43, created by Giddy

---

## Project Structure

```
command-and-conquer/
├── command_center/
│   ├── core.py         # CC — orchestrator, spawner, task dispatcher
│   └── AGENT.md        # CC role, skills, context, system prompt
├── wire/
│   ├── core.py         # WIRE — switchboard, registry, message router
│   └── AGENT.md        # WIRE role, skills, context
├── live_feed/
│   └── monitor.py      # Human-readable snapshot of agents + tasks
├── peons/
│   ├── base_peon.py    # Abstract base: name, session ID, Claude runner
│   ├── devworker/
│   │   ├── worker.py   # Persistent parallel worker peon
│   │   └── AGENT.md    # DevWorker role, skills, system prompt
│   └── giddy/
│       ├── reviewer.py # GitHub peon — PRs, reviews, revisions
│       └── AGENT.md    # GIDY role, skills, system prompt
├── shared/
│   ├── naming.py        # Anime name pool + assignment
│   ├── session.py       # Session ID generation
│   ├── task.py          # Task model: ID, status, creator, assignee
│   └── claude_runner.py # Runs Claude Code CLI via subprocess (no API key needed)
├── config/
│   └── .env.example
├── demo.py              # Boots the full system and dispatches a live PR review
└── requirements.txt
```

---

## Setup

```bash
# Clone and enter
git clone https://github.com/exelzero/command---conquer.git
cd command---conquer

# Create virtualenv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example config/.env
# Fill in GITHUB_TOKEN and GITHUB_REPO in config/.env
# No Anthropic API key needed — Claude Code CLI is the AI runtime
```

---

## Quick Start

```bash
python demo.py
```

`demo.py` boots the full system — registers GIDY, spawns two anime-named DevWorkers, takes a Live Feed snapshot, dispatches a real PR review to GIDY, and snapshots again when done.

---

## How Tasks Flow

```
1. CC creates task → TSK-0001-CC assigned to BOLT
2. CC → WIRE: route TSK-0001-CC to BOLT
3. WIRE delivers to BOLT's queue
4. BOLT picks up task, calls Claude, executes work
5. BOLT reports completion → WIRE → CC
6. CC updates task status, assigns next task
```

---

## Contributing

Each feature lives on its own branch and goes through a PR reviewed by GIDY.

Branch naming:
- `feat/` — new features
- `fix/` — bug fixes
- `docs/` — documentation

Commit format:
```
TSK-NNNN-AGENT: short description
```
