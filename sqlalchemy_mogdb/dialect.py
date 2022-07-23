# mogdb/dialect.py

from packaging.version import Version
import pkg_resources
import sqlalchemy as sa

from . import base
from . import psycopg2
from .psycopg2 import PGDialect_psycopg2
from .psycopg2cffi import PGDialect_psycopg2cffi
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.ext.compiler import compiles

import importlib


sa_version = Version(sa.__version__)

try:
    from alembic.ddl import postgresql
except ImportError:
    pass
else:
    @compiles(postgresql.PostgresqlColumnType, "mogdb")
    def visit_column_type(*args, **kwargs):
        return postgresql.visit_column_type(*args, **kwargs)

    class MogDBImpl(postgresql.PostgresqlImpl):
        __dialect__ = 'mogdb'

base.dialect = psycopg2.dialect


__all__ = (
    'MogDBDialect', 'MogDBDialect_psycopg2',
    'MogDBDialect_psycopg2cffi',
)


class MogDBDialect_psycopg2(PGDialect_psycopg2):
    supports_statement_cache = True
    pass


# Add MogDBDialect synonym for backwards compatibility.
MogDBDialect = PGDialect_psycopg2


class MogDBDialect_psycopg2cffi(PGDialect_psycopg2cffi):
    pass
