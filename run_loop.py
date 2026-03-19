#!/usr/bin/env python3
"""
Wrapper script that runs fastloop_trader.py in a loop for Railway deployment.
The original script is designed for single-run (cron-style), so this wrapper
keeps the process alive by re-running it at a configurable interval.
"""

import subprocess
import sys
import os
import time

INTERVAL = int(os.environ.get("LOOP_INTERVAL_SECONDS", "300"))  # default 5 min

print(f"[run_loop] Starting FastLoop trader loop (interval: {INTERVAL}s)", flush=True)

while True:
    try:
        result = subprocess.run(
            [sys.executable, "fastloop_trader.py", "--live", "--quiet"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=120,
        )
        if result.returncode != 0:
            print(f"[run_loop] fastloop_trader.py exited with code {result.returncode}", flush=True)
    except subprocess.TimeoutExpired:
        print("[run_loop] fastloop_trader.py timed out (120s), moving on", flush=True)
    except Exception as e:
        print(f"[run_loop] Error: {e}", flush=True)

    print(f"[run_loop] Sleeping {INTERVAL}s until next cycle...", flush=True)
    time.sleep(INTERVAL)
