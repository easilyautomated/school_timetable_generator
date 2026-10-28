import csv
from datetime import datetime

class TestRunner:
    """A simple test runner that records results and counts attempts.
    It provides methods to check equality, check for raised exceptions, log bugs, summarize results, and save results to a CSV file.
    This class is designed to facilitate testing by providing a structured way to record and analyse the test outcomes."""

    def __init__(self, suite_name):
        """Set up the empty storage for one suite of tests."""
        self.suite_name = suite_name
        self.results = []
        self.attempt_counts = {}
        self.bug_log = []

    def check(self, test_id, description, actual, expected):
        """Compare actual with expected and record the outcome."""
        if expected == actual:
            passed = True
        else:
            passed = False
        if test_id in self.attempt_counts:
            self.attempt_counts[test_id] += 1
        else:
            self.attempt_counts[test_id] = 1

        result = {
            "id": test_id,
            "description": description,
            "actual": actual,
            "expected": expected,
            "passed": passed,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        if passed:
            print(f"{test_id}: PASS")
        else:
            print(f"{test_id}: FAIL")

    def check_raises(self, test_id, description, func, exception_type):
        """Pass only if calling func() raises exception_type."""
        try:
            func()
        except exception_type:
            self.check(test_id, description, "raised", "raised")
        else:
            # reuse check() so don't need to repeat the recording code
            self.check(test_id, description, "did not raise", "raised")


    def log_bug(self, test_id, cause, fix):
        """Store a bug record with a timestamp."""
        self.bug_log.append({
            "test_id": test_id,
            "cause": cause,
            "fix": fix,
            "timestamp": datetime.now().isoformat()
        })

    def summary(self):
        """Print a small table and return (passed, failed). """
        counts = {"passed": 0, "failed": 0}
        for result in self.results:
            if result["passed"]:
                counts["passed"] += 1
            else:
                counts["failed"] += 1

        print(f"Summary for {self.suite_name}:")
        print(f"  Passed: {counts['passed']}")
        print(f"  Failed: {counts['failed']}")
        return counts["passed"], counts["failed"]

    def save_csv(self, path):
        """Write all results to a CSV file at path. Provides feedback if the file cannot be written and handles any OSError that may occur during the file writing process."""
        try:
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "description", "actual", "expected", "passed", "timestamp"])
                writer.writeheader()
                writer.writerows(self.results)
        except OSError as e:
            print(f"Error: Could not write to file {path} because of {e}.")