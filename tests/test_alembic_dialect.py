from alembic.ddl.base import RenameTable, ColumnComment
from alembic import migration

from sqlalchemy_mogdb import dialect


def test_configure_migration_context():
    context = migration.MigrationContext.configure(
        url='mogdb+psycopg2://mydb'
    )
    assert isinstance(context.impl, dialect.MogDBImpl)
