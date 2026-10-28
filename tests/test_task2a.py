import os, tempfile, sqlite3
from tests.test_runner import TestRunner
from app import create_app
from app.database import get_database

scratch_dir = tempfile.mkdtemp()
runner = TestRunner("task2a")
app = create_app({
    "TESTING": True,
    "DATABASE": os.path.join(scratch_dir, "test_timetable.database"),
    })

plain_app = create_app()
# T2.1a to d: test_config overrides the defaults
runner.check("T2.1a", "test app has TESTING set", app.config["TESTING"], True)
runner.check("T2.1b", "plain app has TESTING off", plain_app.config["TESTING"], False)
runner.check("T2.1c", "override replaced the database path", app.config["DATABASE"] != plain_app.config["DATABASE"], True)
runner.check("T2.1d", "plain path ends with the file name", plain_app.config["DATABASE"].endswith("timetable.database"), True)

# T2.2: one connection per context
with app.app_context():
    first = get_database()
    second = get_database()
    runner.check("T2.2", "two calls return the same object", first is second, True)

# T2.3: connection is closed after the context ends
connection = None
with app.app_context():
    connection = get_database()
runner.check_raises("T2.3", "closed connection refuses queries", lambda: connection.execute("SELECT 1"), sqlite3.ProgrammingError)

# T2.4: foreign keys are on
with app.app_context():
    value = get_database().execute("PRAGMA foreign_keys").fetchone()[0]
    runner.check("T2.4", "foreign_keys reports 1", value, 1)

runner.summary()
runner.save_csv(os.path.join("tests", "results", "task2_rebuild.csv"))

