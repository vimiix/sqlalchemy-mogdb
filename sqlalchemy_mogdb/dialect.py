import imp
import re

from packaging.version import Version
import pkg_resources
import sqlalchemy as sa

from .mogdb import base
from .mogdb import psycopg2
from .mogdb.array import All
from .mogdb.array import Any
from .mogdb.array import ARRAY
from .mogdb.array import array
from .mogdb.base import BIGINT
from .mogdb.base import BIT
from .mogdb.base import BOOLEAN
from .mogdb.base import BYTEA
from .mogdb.base import CHAR
from .mogdb.base import CIDR
from .mogdb.base import CreateEnumType
from .mogdb.base import DATE
from .mogdb.base import DOUBLE_PRECISION
from .mogdb.base import DropEnumType
from .mogdb.base import ENUM
from .mogdb.base import FLOAT
from .mogdb.base import INET
from .mogdb.base import INTEGER
from .mogdb.base import INTERVAL
from .mogdb.base import MACADDR
from .mogdb.base import MONEY
from .mogdb.base import NUMERIC
from .mogdb.base import OID
from .mogdb.base import REAL
from .mogdb.base import REGCLASS
from .mogdb.base import SMALLINT
from .mogdb.base import TEXT
from .mogdb.base import TIME
from .mogdb.base import TIMESTAMP
from .mogdb.base import TSVECTOR
from .mogdb.base import UUID
from .mogdb.base import VARCHAR
from .mogdb.dml import Insert
from .mogdb.dml import insert
from .mogdb.ext import aggregate_order_by
from .mogdb.ext import array_agg
from .mogdb.ext import ExcludeConstraint
from .mogdb.hstore import HSTORE
from .mogdb.hstore import hstore
from .mogdb.json import JSON
from .mogdb.json import JSONB
from .mogdb.ranges import DATERANGE
from .mogdb.ranges import INT4RANGE
from .mogdb.ranges import INT8RANGE
from .mogdb.ranges import NUMRANGE
from .mogdb.ranges import TSRANGE
from .mogdb.ranges import TSTZRANGE
from sqlalchemy.util import compat
from .mogdb.psycopg2 import PGDialect_psycopg2
from .mogdb.psycopg2cffi import PGDialect_psycopg2cffi
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.ext.compiler import compiles

from .mogdb import DOUBLE_PRECISION

import importlib


sa_version = Version(sa.__version__)

try:
    import alembic
except ImportError:
    pass
else:
    from alembic.ddl import postgresql

    from alembic.ddl.base import RenameTable
    compiles(RenameTable, 'mogdb')(postgresql.visit_rename_table)

    if Version(alembic.__version__) >= Version('1.0.6'):
        from alembic.ddl.base import ColumnComment
        compiles(ColumnComment, 'mogdb')(postgresql.visit_column_comment)

    class MogDBImpl(postgresql.PostgresqlImpl):
        __dialect__ = 'mogdb'

if compat.py3k:
    from . import asyncpg  # noqa

base.dialect = psycopg2.dialect


# "Each dialect provides the full set of typenames supported by that backend
# with its __all__ collection
# https://docs.sqlalchemy.org/en/13/core/type_basics.html#vendor-specific-types
__all__ = (
    "INTEGER",
    "BIGINT",
    "SMALLINT",
    "VARCHAR",
    "CHAR",
    "TEXT",
    "NUMERIC",
    "FLOAT",
    "REAL",
    "INET",
    "CIDR",
    "UUID",
    "BIT",
    "MACADDR",
    "MONEY",
    "OID",
    "REGCLASS",
    "DOUBLE_PRECISION",
    "TIMESTAMP",
    "TIME",
    "DATE",
    "BYTEA",
    "BOOLEAN",
    "INTERVAL",
    "ARRAY",
    "ENUM",
    "dialect",
    "array",
    "HSTORE",
    "hstore",
    "INT4RANGE",
    "INT8RANGE",
    "NUMRANGE",
    "DATERANGE",
    "TSVECTOR",
    "TSRANGE",
    "TSTZRANGE",
    "JSON",
    "JSONB",
    "Any",
    "All",
    "DropEnumType",
    "CreateEnumType",
    "ExcludeConstraint",
    "aggregate_order_by",
    "array_agg",
    "insert",
    "Insert",

    'MogDBDialect', 'MogDBDialect_psycopg2',
    'MogDBDialect_psycopg2cffi',
)

class Psycopg2MogDBDialectMixin(DefaultDialect):
    """
    Define behavior specific to ``psycopg2``.

    Most public methods are overrides of the underlying interfaces defined in
    :class:`~sqlalchemy.engine.interfaces.Dialect` and
    :class:`~sqlalchemy.engine.Inspector`.
    """
    def create_connect_args(self, *args, **kwargs):
        """
        Build DB-API compatible connection arguments.

        Overrides interface
        :meth:`~sqlalchemy.engine.interfaces.Dialect.create_connect_args`.
        """
        default_args = {
            'sslmode': 'verify-full',
            'sslrootcert': pkg_resources.resource_filename(
                __name__,
                'mogdb-ca-bundle.crt'
            ),
        }
        cargs, cparams = (
            super(Psycopg2MogDBDialectMixin, self).create_connect_args(
                *args, **kwargs
            )
        )
        default_args.update(cparams)
        return cargs, default_args

    @classmethod
    def dbapi(cls):
        try:
            return importlib.import_module(cls.driver)
        except ImportError:
            raise ImportError(
                'No module named {}'.format(cls.driver)
            )


class MogDBDialect_psycopg2(
    Psycopg2MogDBDialectMixin, PGDialect_psycopg2
):
    pass


# Add MogDBDialect synonym for backwards compatibility.
MogDBDialect = MogDBDialect_psycopg2


class MogDBDialect_psycopg2cffi(
    Psycopg2MogDBDialectMixin, PGDialect_psycopg2cffi
):
    pass
