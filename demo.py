#!/usr/bin/env python3
"""Command & Conquer — Live Demo

Boots the multi-agent system and showcases:
- WIRE registering agents (GIDY + two anime-named DevWorkers)
- CC dispatching tasks through WIRE
- GIDY using Claude Code to review a real GitHub PR
- Live Feed snapshots of system state
"""
import asyncio

from command_center.core import CommandCenter
from live_feed.monitor import LiveFeed
from peons.giddy.reviewer import Giddy
from wire.core import Wire

REPO = "exelzero/command---conquer"


async def main():
    print("\n=== Command & Conquer — Live Demo ===\n")

    # Boot infrastructure
    wire = Wire()
    cc = CommandCenter(wire)

    # GIDY: permanent GitHub peon
    giddy = Giddy()
    wire.register(giddy)
    await giddy.start()

    # Two DevWorkers from the anime name pool
    w1 = cc.spawn_worker()
    w2 = cc.spawn_worker()
    await wire._registry[w1].start()
    await wire._registry[w2].start()

    # Snapshot: all agents online
    feed = LiveFeed(wire, cc)
    feed.snapshot()

    # CC dispatches a code review to GIDY
    print(f"[CC] Dispatching: review PR #3 on {REPO}\n")
    await cc.dispatch("GIDY", {
        "action": "review_pr",
        "repo": REPO,
        "pr_number": 3,
    })

    # Final state
    feed.snapshot()


if __name__ == "__main__":
    asyncio.run(main())
