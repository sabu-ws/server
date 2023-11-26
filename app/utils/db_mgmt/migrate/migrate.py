from flask import current_app
from flask_migrate import stamp, upgrade, current
from alembic.migration import MigrationContext
from alembic.config import Config
from alembic import command as alembic_cmd
from sqlalchemy import create_engine

from app.utils.db_mgmt import database_allowed

import os
from pathlib import Path
import re

def check_migration():
	if current_revision() in available_revision():
		return True
	else:
		return False
	return revisions

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
	print(context.get_current_heads())
	return current_rev

def available_revision():
	revisions = []
	directory = Path(os.path.dirname(current_app.root_path), "migrations", "versions")
	for f in directory.glob("*.py"):
		with f.open() as migration:
			revision = re.search(r"revision = '(.*?)'", migration.read()).group(1)
			revisions.append(revision)
	return revisions

def history_migration():
	alembic_cfg = Config(os.path.join(os.path.dirname(current_app.root_path), "migrations","alembic.ini"))
	a = alembic_cmd.check(alembic_cfg)
	return a