import os, csv, tempfile
from tests.test_runner import TestRunner

# T2B.1: check(5, 5) should record passed = True
runner = TestRunner("t2b1")
runner.check("x", "5 equals 5", 5, 5)
if runner.results[0]["passed"] == True:
    print("T2B.1: PASS")
else:
    print("T2B.1: FAIL - got", runner.results[0]["passed"])

# T2B.2: check(5, 6) should record passed = False
runner = TestRunner("t2b2")
runner.check("x", "5 vs 6", 5, 6)
if runner.results[0]["passed"] == False:
    print("T2B.2: PASS")
else:
    print("T2B.2: FAIL - got", runner.results[0]["passed"])

# T2B.3: same test ID run twice should give an attempt count of 2
runner = TestRunner("t2b3")
runner.check("x", "first run", 1, 1)
runner.check("x", "second run", 1, 1)
if runner.attempt_counts["x"] == 2:
    print("T2B.3: PASS")
else:
    print("T2B.3: FAIL - got", runner.attempt_counts["x"])

# T2B.4: check_raises should record a True when int("x") raises ValueError
runner = TestRunner("t2b4")
runner.check_raises("x", "bad int", lambda: int("x"), ValueError)
if runner.results[0]["passed"] == True:
    print("T2B.4: PASS")
else:
    print("T2B.4: FAIL - got", runner.results[0]["passed"])

# T2B.5: after 3 checks, the CSV should have 4 rows including the header
runner = TestRunner("t2b5")
runner.check("a", "first", 1, 1)
runner.check("b", "second", 2, 2)
runner.check("c", "third", 3, 3)
path = os.path.join(tempfile.mkdtemp(), "results.csv")
runner.save_csv(path)
with open(path, newline="") as f:
    rows = list(csv.reader(f))
if len(rows) == 4 and "timestamp" in rows[0]:
    print("T2B.5: PASS - rows:", len(rows))
else:
    print("T2B.5: FAIL - got", len(rows), "rows; header:", rows[0])

# T2B.6: save_csv to a missing folder should print a message and not crash
runner = TestRunner("t2b6")
runner.check("a", "something to save", 1, 1)
try:
    runner.save_csv(os.path.join("no_such_folder", "results.csv"))
except Exception as e:
    print("T2B.6: FAIL - it crashed with", repr(e))
else:
    print("T2B.6: PASS - no crash (message above is the evidence)")