from datetime import datetime


class LiveFeed:
    def __init__(self, wire, cc):
        self.wire = wire
        self.cc = cc

    def snapshot(self):
        agents = self.wire.agents()
        tasks = self.cc.all_tasks()
        now = datetime.utcnow().strftime("%H:%M:%S UTC")

        print(f"\n{'='*48}")
        print(f"  LIVE FEED — {now}")
        print(f"{'='*48}")

        print(f"\n  AGENTS ({len(agents)})")
        for a in agents:
            status = "ACTIVE" if a["active"] else "IDLE"
            print(f"    [{status}] {a['session_id']}")

        print(f"\n  TASKS ({len(tasks)})")
        for t in tasks:
            print(f"    {t['id']} | {t['assignee']} | {t['status']}")

        print(f"\n{'='*48}\n")
