import sqlite3, click
from flask import current_app, g
from flask.cli import with_appcontext

def get_database():
    """ Connects to the SQLite database so multiple functions during the same request reuse one connection rather than opening several
    Returns the database connection object for use in other functions.
    Raises a RuntimeError if the connection fails, logging the specific error for debugging purposes.
    """
    try:
        # Checks if the database connection is already established in the current request context.
        if "database" not in g:
            g.database = sqlite3.connect(current_app.config["DATABASE"])
            g.database.row_factory = sqlite3.Row
            # Enforces foreign key constraints.
            g.database.execute("PRAGMA foreign_keys = ON")

        return g.database
    except sqlite3.Error as e:
        # Logs the error and raises an exception if the database connection fails.
        current_app.logger.error(f"Database connection has failed: {e}")
        raise RuntimeError("Database connection has failed") from e

def close_database(e=None):
    """Closes the database connection at the end of the request if it was established.
    Logs any errors that occur during the process of closing the database to help with debugging and maintenance.
    """
    try:
        database = g.pop("database", None)
        if database is not None:
            database.close()
    except sqlite3.Error as e:
        current_app.logger.error(f"An error occurred while closing the database: {e}")

def init_database():
    """ Initializes the database by executing the schema.sql script.
    Raises a RuntimeError if the initialization fails, logging the specific error for debugging purposes.
    Raises a FileNotFoundError if the schema.sql file is not found, logging the specific error for debugging purposes.
     """
    try:
        database = get_database()
        with current_app.open_resource("schema.sql") as f:
            database.executescript(f.read().decode("utf8"))
    except sqlite3.Error as e:
        current_app.logger.error(f"Database initialization has failed: {e}")
        raise RuntimeError("Database initialization has failed") from e
    except FileNotFoundError as e:
        current_app.logger.error(f"The schema file was not found: {e}")
        raise FileNotFoundError("The schema file was not found") from e

# A command line to initialise the database.
@click.command("init-database")
@with_appcontext
def init_database_command():
    """Initializes the database by calling the init_database function and provides feedback to the user."""
    init_database()
    click.echo("Database has been initialised.")