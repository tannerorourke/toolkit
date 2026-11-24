"""PreToolUse hook for Bash: hold each read-only agent between its floor and the ceiling.

Floor: what the role needs to do its job. Every read-only role reads git history inside the
working directory and lists and searches files ('ls', 'grep', 'git ls-files', 'git grep'); the
verifier also runs the project's test commands, with paths and a few reporting flags, and this
plugin's scripts. Extension: the profile's 'agent_bash_allow' adds command prefixes per role.
Ceiling: anything else, any floor flag that runs a program or writes a file, any character the
shell would act on, and any command that fails to parse is denied. Inside single quotes nothing
is acted on, so a pattern there may hold any character. Writers pass untouched.
Wired in hooks/hooks.json with matcher Bash; reads the event on stdin.
  python3 scripts/verifier_bash.py < event.json
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

import toolkit_profile

READ_ONLY = {"executor:verifier", "executor:surveyor", "executor:critic"}
SCRIPTS = Path(__file__).resolve().parent
# -- operators, substitutions, bash braces, zsh parens, comments, tildes, and globs (zsh
# -- extendedglob adds '^', '#', '~'), any of which can turn one word into another or a flag
UNQUOTED = set(";&|`$<>(){}*?[]\\^#~")
IN_DOUBLE = set("$`\\")
GIT_FLOOR = {"status", "diff", "log", "show", "ls-files", "grep"}
# -- each writes a file or runs a configured program
GIT_DENY = ("--output", "--ext-diff", "--exec-path")
# -- 'git grep -O' runs a pager on the matches; git accepts '--op' for '--open-files-in-pager'
GIT_GREP_PAGER = re.compile(r"-[^-]*O|--op")
SEARCH_FLOOR = {"ls", "grep"}
# -- Claude Code runs 'grep' as ugrep; these are the flags its own wrapper keeps from ugrep,
# -- since they run a filter, pager, or viewer, or read or write a config
GREP_DENY = ("--filter", "--pager", "--view", "--format-open", "--config", "--save-config",
             "---")
# -- each runner has more ways to write or import than a deny list can name, so a test command
# -- takes paths and these flags alone; anything else goes through 'agent_bash_allow'
TEST_FLAGS = {"-q", "-qq", "-v", "-vv", "-x", "-s", "--quiet", "--verbose", "--exitfirst",
              "--lf", "--last-failed", "--ff", "--failed-first", "--no-header", "--tb=short",
              "--tb=long", "--tb=line", "--tb=no", "--statistics"}
TEST_VALUE_FLAGS = {"-k", "-m"}
# -- make's words are targets and npm forwards its words to the project's runner
NO_PATHS = {"make", "npm"}


# -- the checks below read the shlex split, so any expansion bash or zsh would make is denied;
# -- zsh expands '=word' to a program's path, and shlex splits on '\r' where the shell does not
def shell_acts(cmd: str) -> bool:
    if any(ord(ch) < 32 and ch != "\t" for ch in cmd):
        return True
    quote, prev = "", " "
    for ch in cmd:
        if quote == "'":
            quote = "" if ch == "'" else quote
        elif quote == '"':
            if ch in IN_DOUBLE:
                return True
            quote = "" if ch == '"' else quote
        elif ch in "'\"":
            quote = ch
        elif ch in UNQUOTED or (ch == "=" and prev in " \t"):
            return True
        prev = ch
    return bool(quote)


def matched(args: list[str], prefixes: list[str]) -> int:
    # -- the prefixes come from the user's profile; a bare string or an empty entry would allow all
    if not isinstance(prefixes, list):
        raise ValueError("command prefixes must be a list")
    return max((len(p) for p in map(shlex.split, prefixes) if p and args[:len(p)] == p),
               default=0)


def inside(path: str, cwd: Path) -> bool:
    return (cwd / path).resolve().is_relative_to(cwd.resolve())


# -- '-C' stays inside the working directory: another repository's config can name programs
def git_floor(args: list[str], cwd: Path) -> bool:
    args = args[1:]
    while args[:1] == ["--no-pager"] or (args[:1] == ["-C"] and len(args) > 1):
        if args[0] == "-C" and not inside(args[1], cwd):
            return False
        args = args[2:] if args[0] == "-C" else args[1:]
    if not args or args[0] not in GIT_FLOOR:
        return False
    flags = args[1:]
    if args[0] == "grep" and any(GIT_GREP_PAGER.match(a) for a in flags):
        return False
    return not any(a.startswith(GIT_DENY) for a in flags)


def search_floor(args: list[str]) -> bool:
    return args[0] in SEARCH_FLOOR and not (
        args[0] == "grep" and any(a.startswith(GREP_DENY) for a in args[1:]))


def test_path(arg: str, cwd: Path) -> bool:
    return not arg.startswith("-") and (cwd / arg.split("::")[0]).exists()


def test_command(args: list[str], prefixes: list[str], cwd: Path) -> bool:
    n = matched(args, prefixes)
    if not n:
        return False
    # -- ruff's other subcommands format, clean, or serve
    if args[0] == "ruff":
        if args[1:2] != ["check"]:
            return False
        n = max(n, 2)
    rest = iter(args[n:])
    for arg in rest:
        if arg in TEST_VALUE_FLAGS:
            if next(rest, None) is None:
                return False
        elif arg not in TEST_FLAGS and (args[0] in NO_PATHS or not test_path(arg, cwd)):
            return False
    return True


def plugin_script(args: list[str], cwd: Path) -> bool:
    if len(args) < 2 or re.fullmatch(r"python3?", args[0]) is None or args[1].startswith("-"):
        return False
    path = (cwd / args[1]).resolve()
    return path.suffix == ".py" and path.is_file() and path.is_relative_to(SCRIPTS)


def allowed(role: str, cmd: str, profile: dict, cwd: Path) -> bool:
    if shell_acts(cmd):
        return False
    args = shlex.split(cmd)
    if not args:
        return False
    if (args[0] == "git" and git_floor(args, cwd)) or search_floor(args):
        return True
    if role == "verifier" and (test_command(args, profile["test_commands"], cwd)
                               or plugin_script(args, cwd)):
        return True
    return matched(args, profile["agent_bash_allow"].get(role, [])) > 0


def main() -> None:
    agent = role = "unknown"
    # -- fail closed: a hook that crashes lets the command run
    try:
        event = json.load(sys.stdin)
        agent = event.get("agent_type")
        if agent not in READ_ONLY:
            return
        role = agent.split(":")[1]
        cwd = Path(event.get("cwd") or os.getcwd())
        command = event.get("tool_input", {}).get("command", "")
        if allowed(role, command, toolkit_profile.load(), cwd):
            return
    except (Exception, SystemExit):
        pass
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"{agent} may run only its floor (read-only git inside the"
        " working directory, ls, grep"
        + (", the profile's test_commands with paths and reporting flags, this plugin's scripts"
           if role == "verifier" else "")
        + ") and the profile's agent_bash_allow entries for its role, with no flag that runs a"
        " program or writes a file, and no shell metacharacter or glob outside single quotes",
    }}))


if __name__ == "__main__":
    main()
