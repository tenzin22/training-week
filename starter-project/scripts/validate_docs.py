#!/usr/bin/env python3
"""Check three documentation contracts against the current implementation."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import ALLOWED_STATUSES, FILTER_OPTION, STORAGE_FORMAT  # noqa: E402


def validate() -> list[str]:
    docs = PROJECT_ROOT / "docs"
    requirements = (docs / "requirements.md").read_text(encoding="utf-8")
    architecture = (docs / "architecture.md").read_text(encoding="utf-8")
    operations = (docs / "operations.md").read_text(encoding="utf-8")

    issues: list[str] = []
    status_line = next((line for line in requirements.splitlines() if line.startswith("- `status`:")), "")
    missing = [status for status in sorted(ALLOWED_STATUSES) if f"`{status}`" not in status_line]
    extra = [status for status in ("paused",) if f"`{status}`" in status_line and status not in ALLOWED_STATUSES]
    if missing or extra:
        issues.append(f"docs/requirements.md: status list differs from code (missing={missing}, extra={extra})")

    storage_line = next(
        (line for line in architecture.splitlines() if line.startswith("- `storage_format`:")),
        "",
    )
    if f"`{STORAGE_FORMAT}`" not in storage_line:
        issues.append("docs/architecture.md: storage format must identify JSON used by app.py")

    filter_line = next(
        (line for line in operations.splitlines() if line.startswith("- `filter_option`:")),
        "",
    )
    if f"`{FILTER_OPTION}`" not in filter_line:
        issues.append("docs/operations.md: filter option must be --status")

    return issues


def main() -> int:
    issues = validate()
    if issues:
        print(
            f"Documentation validation found {len(issues)} known issue(s):",
            file=sys.stderr,
        )
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("Documentation validation passed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
