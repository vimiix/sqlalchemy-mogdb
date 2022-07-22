import pytest

from sqlalchemy.dialects.postgresql import (
    psycopg2, psycopg2cffi
)

from sqlalchemy_mogdb import dialect
from rs_sqla_test_utils.utils import make_mock_engine


@pytest.mark.parametrize('name, expected_dialect', [
    ('mogdb', psycopg2.dialect),
    ('mogdb+psycopg2', psycopg2.dialect),
    ('mogdb+psycopg2cffi', psycopg2cffi.dialect),
])
def test_dialect_inherits_from_sqlalchemy_dialect(name, expected_dialect):
    engine = make_mock_engine(name)

    assert isinstance(engine.dialect, expected_dialect)


@pytest.mark.parametrize('name, expected_dialect', [
    ('mogdb', dialect.MogDBDialect),
    ('mogdb+psycopg2', dialect.MogDBDialect_psycopg2),
    ('mogdb+psycopg2cffi', dialect.MogDBDialect_psycopg2cffi),
])
def test_dialect_registered_correct_class(name, expected_dialect):
    engine = make_mock_engine(name)

    assert isinstance(engine.dialect, expected_dialect)


def test_mogdb_dialect_synonym_of_mogdb_dialect_psycopg2():
    assert isinstance(
        dialect.MogDBDialect(),
        dialect.MogDBDialect_psycopg2
    )
