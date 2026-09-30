"""Create GitHub issues from tools/test-cases.json.

Each issue looks exactly like one filled in through the "Test case" form
(.github/ISSUE_TEMPLATE/test-case.yml). Issues that already exist (same ID in
the title) are skipped, so the script can be run again safely.

Requires the GitHub CLI: https://cli.github.com, then `gh auth login`.

Usage:
    python tools/create_test_case_issues.py --dry-run          # preview only
    python tools/create_test_case_issues.py                    # create all
    python tools/create_test_case_issues.py --priority P1      # only smoke
    python tools/create_test_case_issues.py --project "Test cases"
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

DATA = Path(__file__).parent / "test-cases.json"

LABELS = {
    "test-case": ("0E8A16", "A manual or automated check"),
    "p1": ("B60205", "Critical, smoke"),
    "p2": ("FBCA04", "Regression"),
    "p3": ("C2E0C6", "Edge cases"),
    "automated": ("5319E7", "Covered by an automated test"),
}
MODULE_COLOR = "1D76DB"
NO_RESPONSE = "_No response_"


def gh(*args: str, repo: str | None) -> str:
    cmd = ["gh", *args]
    if repo:
        cmd += ["--repo", repo]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        sys.exit(f"gh failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout


def module_label(module: str) -> str:
    return "module:" + module.lower().replace(" ", "-")


def render_body(case: dict) -> str:
    """The same markdown GitHub produces when the issue form is submitted."""
    steps = "\n".join(f"{n}. {s}" for n, s in enumerate(case["steps"], 1))
    sections = [
        ("Module", case["module"]),
        ("Priority", case["priority"]),
        ("Type", case["type"]),
        ("Preconditions", case["preconditions"]),
        ("Test data", case["data"]),
        ("Steps", steps),
        ("Expected result", case["expected"]),
        ("Requirement", case["requirement"]),
        ("Automation", case["automation"]),
        ("Automated test", case["autotest"]),
    ]
    parts = []
    for heading, value in sections:
        value = (
            value.strip() if value and value.strip() not in ("", "—") else NO_RESPONSE
        )
        parts.append(f"### {heading}\n\n{value}")
    return "\n\n".join(parts) + "\n"


def labels_for(case: dict) -> list[str]:
    labels = ["test-case", case["priority"].lower(), module_label(case["module"])]
    if case["automation"] != "Manual":
        labels.append("automated")
    return labels


def ensure_labels(cases: list[dict], repo: str | None) -> None:
    wanted = dict(LABELS)
    for case in cases:
        wanted[module_label(case["module"])] = (
            MODULE_COLOR,
            f"Module: {case['module']}",
        )
    for name, (color, description) in wanted.items():
        gh(
            "label",
            "create",
            name,
            "--color",
            color,
            "--description",
            description,
            "--force",
            repo=repo,
        )


def existing_ids(repo: str | None) -> set[str]:
    raw = gh(
        "issue",
        "list",
        "--label",
        "test-case",
        "--state",
        "all",
        "--limit",
        "1000",
        "--json",
        "title",
        repo=repo,
    )
    ids = set()
    for issue in json.loads(raw):
        title = issue["title"]
        if title.startswith("[") and "]" in title:
            ids.add(title[1 : title.index("]")])
    return ids


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", help="owner/name; defaults to the current repo")
    parser.add_argument("--priority", choices=["P1", "P2", "P3"])
    parser.add_argument("--project", help='project title, e.g. "Test cases"')
    parser.add_argument("--dry-run", action="store_true", help="print, create nothing")
    args = parser.parse_args()

    cases = json.loads(DATA.read_text(encoding="utf-8"))
    if args.priority:
        cases = [c for c in cases if c["priority"] == args.priority]

    if args.dry_run:
        for case in cases:
            print(f"=== [{case['id']}] {case['title']}")
            print(f"labels: {', '.join(labels_for(case))}\n")
            print(render_body(case))
        print(f"{len(cases)} issues would be created.")
        return

    ensure_labels(cases, args.repo)
    done = existing_ids(args.repo)
    created = skipped = 0
    for case in cases:
        if case["id"] in done:
            skipped += 1
            continue
        cmd = [
            "issue",
            "create",
            "--title",
            f"[{case['id']}] {case['title']}",
            "--body",
            render_body(case),
        ]
        for label in labels_for(case):
            cmd += ["--label", label]
        if args.project:
            cmd += ["--project", args.project]
        url = gh(*cmd, repo=args.repo).strip()
        print(f"[{case['id']}] {url}")
        created += 1
        time.sleep(1)  # stay well below GitHub's secondary rate limit
    print(f"Created: {created}, already existed: {skipped}")


if __name__ == "__main__":
    main()
