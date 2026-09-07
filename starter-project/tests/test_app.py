import json
import tempfile
import unittest
from pathlib import Path

import app


class JobListTest(unittest.TestCase):
    def test_loads_three_synthetic_jobs(self) -> None:
        self.assertEqual(3, len(app.load_jobs()))

    def test_filters_open_jobs(self) -> None:
        jobs = app.filter_jobs(app.load_jobs(), "open")
        self.assertEqual(["JOB-001", "JOB-003"], [job["job_id"] for job in jobs])

    def test_rejects_unknown_status(self) -> None:
        payload = {"jobs": [{"job_id": "JOB-X", "title": "Synthetic", "location": "Example", "status": "paused"}]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "jobs.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unsupported status: paused"):
                app.load_jobs(path)


if __name__ == "__main__":
    unittest.main()
