"""SessionStart hook: print open idea items parked for the current repo.

Reads hook JSON on stdin (cwd). Silent when headless, outside a repo, or no ideas.
Used by: hooks/hooks.json
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import toolkit_profile as profile
import thoughts


def main():
    if os.environ.get("TOOLKIT_HEADLESS") == "1":
        return
    cwd = json.load(sys.stdin).get("cwd", ".")
    top = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, timeout=3)
    if top.returncode:
        return
    repo = Path(top.stdout.strip()).name
    ideas = thoughts.open_items(Path(profile.get("thoughts_ledger")), repo, "idea")
    if ideas:
        print(f"Parked ideas for {repo}:")
        for x in ideas:
            print(f"- {x['text']} ^{x['id']}")


if __name__ == "__main__":
    main()
