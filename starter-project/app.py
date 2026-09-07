"""Small synthetic job-list CLI used by the Kiro IDE workshop."""

import argparse
import json
from pathlib import Path

ALLOWED_STATUSES = frozenset({"open", "closed"})
STORAGE_FORMAT = "json"
FILTER_OPTION = "--status"
DATA_FILE = Path(__file__).parent / "data" / "jobs.json"


def load_jobs(path: Path = DATA_FILE) -> list[dict[str, str]]:
    jobs = json.loads(path.read_text(encoding="utf-8"))["jobs"]
    for job in jobs:
        if job["status"] not in ALLOWED_STATUSES:
            raise ValueError(f"Unsupported status: {job['status']}")
    return jobs


def filter_jobs(jobs: list[dict[str, str]], status: str | None = None) -> list[dict[str, str]]:
    return [job for job in jobs if status is None or job["status"] == status]


def main() -> int:
    parser = argparse.ArgumentParser(description="List synthetic jobs")
    parser.add_argument(FILTER_OPTION, choices=sorted(ALLOWED_STATUSES))
    args = parser.parse_args()
    for job in filter_jobs(load_jobs(), args.status):
        print(f"{job['job_id']}\t{job['title']}\t{job['location']}\t{job['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
