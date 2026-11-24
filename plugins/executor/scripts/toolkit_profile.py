"""Resolve the executor profile: real copy overlaid on the shipped example.

Used by: sibling scripts (import toolkit_profile as profile; profile.get('traces_dir')) and the CLI
  python3 toolkit_profile.py [key]
Real copy: ~/.claude/toolkit/profile.json, or the path in env var TOOLKIT_PROFILE (must exist).
"""
import json
import os
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parent.parent / "profile.example.json"
DEFAULT = "~/.claude/toolkit/profile.json"


def _expand(value):
    # -- strings are paths; lists expand element-wise
    if isinstance(value, list):
        return [_expand(v) for v in value]
    return os.path.expandvars(os.path.expanduser(value)) if isinstance(value, str) else value


def load() -> dict:
    profile = json.loads(EXAMPLE.read_text())
    override = os.environ.get("TOOLKIT_PROFILE")
    real = Path(os.path.expanduser(override or DEFAULT))
    # -- a named profile must exist; only the default may be absent
    if override and not real.is_file():
        sys.exit(f"TOOLKIT_PROFILE not found: {real}")
    if real.is_file():
        profile.update(json.loads(real.read_text()))
    return {k: _expand(v) for k, v in profile.items()}


def get(key):
    return load()[key]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps(load(), indent=2))
    elif sys.argv[1] in load():
        print(get(sys.argv[1]))
    else:
        print(f"unknown profile key: {sys.argv[1]}", file=sys.stderr)
        sys.exit(2)
