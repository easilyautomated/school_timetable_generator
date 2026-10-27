import os, tempfile, sqlite3
from app import create_app

scratch_dir = tempfile.mkdtemp()
app = create_app({
    "TESTING": True,
    "DATABASE": os.path.join(scratch_dir, "test_timetable.database"),
    })

plain_app = create_app()

# T2.1a: the test app should have TESTING set to True
if app.config["TESTING"] == True:
    print("T2.1a: PASS")
else:
    print("T2.1a: FAIL - got", app.config["TESTING"])

# T2.1b: the plain app should have TESTING set to False
if plain_app.config["TESTING"] == False:
    print("T2.1b: PASS")
else:
    print("T2.1b: FAIL - got", plain_app.config["TESTING"])

# T2.1c: the override must have replaced the default database path
if app.config["DATABASE"] != plain_app.config["DATABASE"]:
    print("T2.1c: PASS")
else:
    print("T2.1c: FAIL - both apps use the same database path")

# T2.1d: the plain app's default path must still end with the file name
if plain_app.config["DATABASE"].endswith("timetable.database"):
    print("T2.1d: PASS")
else:
    print("T2.1d: FAIL - got", plain_app.config["DATABASE"])


# T2.2: two calls to get_database() in one context should give back the same connection object
from app.database import get_database
with app.app_context():
    first = get_database()
    second = get_database()
    if first is second:
        print("T2.2: PASS - same connection reused")
    else:
        print("T2.2: FAIL - two different connections were opened")

# T2.3: after the context ends, the connection should be closed
connection = None
with app.app_context():
    connection = get_database()

# the with block has ended, so teardown has run
try:
    connection.execute("SELECT 1")
except sqlite3.ProgrammingError:
    print("T2.3: PASS - connection was closed")
else:
    print("T2.3: FAIL - connection still worked after the context ended")

# T2.4: PRAGMA foreign_keys should report 1 on a fresh connection
with app.app_context():
    result = get_database().execute("PRAGMA foreign_keys").fetchone()
    value = result[0]
    if value == 1:
        print("T2.4: PASS - foreign keys are ON, value is", value)
    else:
        print("T2.4: FAIL - got", value)