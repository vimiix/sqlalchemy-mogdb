import os
import copy
import contextlib
import itertools
import uuid
import functools
import time

try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

import requests
import pytest
import sqlalchemy as sa


from rs_sqla_test_utils import db
from rs_sqla_test_utils.utils import make_mock_engine


_unicode = type(u'')


def database_name_generator():
    template = 'testdb_{uuid}_{count}'
    db_uuid = _unicode(uuid.uuid1()).replace('-', '')
    for i in itertools.count():
        yield template.format(
            uuid=db_uuid,
            count=i,
        )


database_name = functools.partial(next, database_name_generator())


class DatabaseTool(object):
    """
    Abstracts the creation and destruction of migrated databases.
    """

    def __init__(self):
        self.engine = self.engine_definition.engine()

    @contextlib.contextmanager
    def _database(self):
        db_name = database_name()
        with self.engine.connect() as conn:
            conn.execute('COMMIT')  # Can't create databases in a transaction
            conn.execute('CREATE DATABASE {db_name}'.format(db_name=db_name))

        dburl = copy.deepcopy(self.engine.url)
        try:
            dburl.database = db_name
        except AttributeError:
            dburl = dburl.set(database=db_name)

        try:
            yield db.EngineDefinition(
                db_connect_url=dburl,
                connect_args=self.engine_definition.connect_args,
            )
        finally:
            with self.engine.connect() as conn:
                conn.execute('COMMIT')  # Can't drop databases in a transaction
                conn.execute('DROP DATABASE {db_name}'.format(db_name=db_name))

    @contextlib.contextmanager
    def migrated_database(self):
        """
        Test fixture for testing real commits/rollbacks.

        Creates and migrates a fresh database for every test.
        """
        with self._database() as engine_definition:
            engine = engine_definition.engine()
            try:
                self.migrate(engine)
                yield {
                    'definition': engine_definition,
                    'engine': engine,
                }
            finally:
                engine.dispose()


def pytest_addoption(parser):
    """
    Pytest option to define which dbdrivers to run the test suite with.

    """
    parser.addoption("--dbdriver", action="append")


class DriverParameterizedTests:
    """
    Helper class for generating fixture params using pytest config opts.

    """
    DEFAULT_DRIVERS = ['psycopg2', 'psycopg2cffi']
    mogdb_dialect_flavors = None

    @classmethod
    def set_drivers(cls,  _drivers):
        DriverParameterizedTests.mogdb_dialect_flavors = [
            'mogdb+{}'.format(x) for x in _drivers
        ]


def pytest_generate_tests(metafunc):

    if 'mogdb_dialect_flavor' in metafunc.fixturenames:
        if DriverParameterizedTests.mogdb_dialect_flavors is None:
            dbdrivers = metafunc.config.getoption(
                "--dbdriver", default=DriverParameterizedTests.DEFAULT_DRIVERS
            )
            DriverParameterizedTests.set_drivers(dbdrivers)

        metafunc.parametrize(
            'mogdb_dialect_flavor',
            DriverParameterizedTests.mogdb_dialect_flavors,
            ids=DriverParameterizedTests.mogdb_dialect_flavors,
            scope="session")


@pytest.yield_fixture(scope='function')
def _mogdb_engine_and_definition(_mogdb_database_tool):
    with _mogdb_database_tool.migrated_database() as database:
        yield database


@pytest.fixture(scope='function')
def mogdb_engine(_mogdb_engine_and_definition):
    """
    A mogdb engine for a freshly migrated database.
    """
    return _mogdb_engine_and_definition['engine']


@pytest.fixture(scope='function')
def mogdb_engine_definition(_mogdb_engine_and_definition):
    """
    A mogdb engine definition for a freshly migrated database.
    """
    return _mogdb_engine_and_definition['definition']


@pytest.yield_fixture(scope='session')
def _session_scoped_mogdb_engine(_mogdb_database_tool):
    """
    Private fixture to maintain a db for the entire test session.
    """
    with _mogdb_database_tool.migrated_database() as egs:
        yield egs['engine']


@pytest.yield_fixture(scope='function')
def mogdb_session(_session_scoped_mogdb_engine):
    """
    A mogdb session that rolls back all operations.

    The engine and db is maintained for the entire test session for efficiency.
    """
    conn = _session_scoped_mogdb_engine.connect()
    tx = conn.begin()

    MogDBSession = sa.orm.sessionmaker()
    session = MogDBSession(bind=conn)
    try:
        yield session
    finally:
        session.close()
        tx.rollback()
        conn.close()


@pytest.fixture(scope='session')
def stub_mogdb_engine(mogdb_dialect_flavor):
    yield make_mock_engine(mogdb_dialect_flavor)


@pytest.fixture(scope='session')
def stub_mogdb_dialect(stub_mogdb_engine):
    yield stub_mogdb_engine.dialect
