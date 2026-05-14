# WIRE — Local Switchboard

## Role
The nervous system of Command & Conquer. WIRE is the central message
router through which all inter-agent communication flows. No agent
speaks to another directly — everything goes through WIRE.

WIRE also maintains the agent registry, tracking every active peon
by name and session ID, and reports agent health back to CC.

## Skills
- Message routing between all agents
- Agent registry management (register/unregister peons on spawn/death)
- Session tracking (NAME#hex8 session IDs)
- Task delivery and acknowledgement
- Health monitoring (knows which agents are active/idle)
- Bidirectional liaison with CC (reports completions, failures, state)

## Context
WIRE sits between CC and all peons. It is purely operational — it does
not make decisions, only routes. Its registry is the single source of
truth for which agents are currently online.

All task objects pass through WIRE. WIRE queues tasks per-agent and
delivers them in order. If an agent is offline, WIRE logs the drop
and notifies CC.

## Usage

```python
from wire.core import Wire

wire = Wire()

# Register a peon when it comes online
wire.register(peon)

# Unregister when it goes offline
wire.unregister(peon)

# Route a task to its assignee
await wire.route(task)

# Send an ad-hoc message between agents
await wire.send("CC", "BOLT", {"type": "ping"})

# Report a task completion back to CC
await wire.report_to_cc(task)

# List all currently registered agents
wire.agents()
# [{"name": "BOLT", "session_id": "BOLT#a3f2b1c4", "active": True}, ...]
```

## Design Notes
WIRE is infrastructure, not an AI. It does not call Claude.
It is the transport layer that makes the multi-agent system coherent.

Every message routed through WIRE carries a task ID (TSK-NNNN-SENDER)
making all traffic fully traceable in Live Feed.
