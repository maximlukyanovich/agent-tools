"""The wait block of `reference/commands.md`, run against a stub.

`create-pr` runs this block before a merge, and a wrong one reports checks
green that are not. So the test takes it from the text itself and runs it,
with `gh` replaced by scripted answers.
"""

import json
import os
import re
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

TEXT = Path(
    os.environ.get(
        "CI_WAIT_TEXT",
        Path(__file__).resolve().parent.parent / "reference/commands.md",
    )
)

STUB = """#!/bin/bash
n=$(cat "$STUB_DIR/reads")
echo $((n + 1)) > "$STUB_DIR/reads"
last=$(cat "$STUB_DIR/last")
[ "$n" -gt "$last" ] && n=$last
cat "$STUB_DIR/$n.out"
cat "$STUB_DIR/$n.err" >&2
exit "$(cat "$STUB_DIR/$n.code")"
"""


def block():
    section = TEXT.read_text().split("## Waiting for checks", 1)[1]
    return re.search(r"```bash\n(.*?)```", section, re.S).group(1)


def run(answers, limit=5):
    """Runs the block; `answers` are (stdout, stderr, exit code), the last repeating."""
    with tempfile.TemporaryDirectory() as folder:
        stub_dir = Path(folder)
        stub = stub_dir / "gh"
        stub.write_text(STUB)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
        (stub_dir / "reads").write_text("0")
        (stub_dir / "last").write_text(str(len(answers) - 1))
        for index, (out, err, code) in enumerate(answers):
            (stub_dir / f"{index}.out").write_text(out)
            (stub_dir / f"{index}.err").write_text(err)
            (stub_dir / f"{index}.code").write_text(str(code))
        env = {
            **os.environ,
            "PATH": f"{stub_dir}:{os.environ['PATH']}",
            "STUB_DIR": str(stub_dir),
            "PR": "7",
            "LIMIT": str(limit),
            "POLL": "0.01",
        }
        result = subprocess.run(
            ["bash", "-c", block()], env=env, capture_output=True, text=True, timeout=30
        )
        return result, int((stub_dir / "reads").read_text())


def checks(*buckets):
    return json.dumps([{"name": f"c{i}", "bucket": b} for i, b in enumerate(buckets)]), "", 0


NO_CHECKS = ("", "no checks reported on the 'x' branch\n", 1)


class GitHub(unittest.TestCase):
    def wait(self, *answers, limit=5):
        return run(list(answers), limit)

    def test_passed_and_skipped_checks_are_green(self):
        result, reads = self.wait(checks("pass", "skipping"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("success", 0))
        self.assertEqual(reads, 1)

    def test_all_checks_skipped_is_not_green(self):
        result, _ = self.wait(checks("skipping", "skipping"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("skipped", 1))

    def test_no_checks_yet_keeps_waiting(self):
        result, reads = self.wait(NO_CHECKS, checks("pass"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("success", 0))
        self.assertEqual(reads, 2)

    def test_an_empty_list_is_not_green(self):
        result, reads = self.wait(checks(), checks("pass"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("success", 0))
        self.assertEqual(reads, 2)

    def test_a_pending_check_keeps_waiting(self):
        result, reads = self.wait(checks("pass", "pending"), checks("pass", "pass"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("success", 0))
        self.assertEqual(reads, 2)

    def test_a_failed_check_stops_at_once(self):
        result, reads = self.wait(checks("fail", "pending"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("failed", 1))
        self.assertEqual(reads, 1)

    def test_a_canceled_check_is_not_green(self):
        result, _ = self.wait(checks("pass", "cancel"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("canceled", 1))

    def test_an_error_ends_the_wait_and_stays_visible(self):
        result, reads = self.wait(("", "HTTP 502\n", 1), checks("pass"))
        self.assertEqual((result.stdout.strip(), result.returncode), ("status not read", 1))
        self.assertIn("HTTP 502", result.stderr)
        self.assertEqual(reads, 1)

    def test_a_limit_that_runs_out_is_no_result(self):
        result, _ = self.wait(checks("pending"), limit=1)
        self.assertEqual((result.stdout.strip(), result.returncode), ("no result", 1))


if __name__ == "__main__":
    unittest.main()
