from flask import current_app
from flask_migrate import stamp, upgrade
from alembic.migration import MigrationContext
from sqlalchemy import create_engine

from app.utils.db_mgmt import database_allowed

import os


def upgrade_migration():
    upgrade()
    return True


def stamp_migration():
    directory = os.path.join(os.path.dirname(current_app.root_path), "migrations")
    stamp(directory=directory)


def current_revision():
    engine = create_engine(database_allowed())
    conn = engine.connect()
    context = MigrationContext.configure(conn)
    current_rev = context.get_current_revision()
    return current_rev
