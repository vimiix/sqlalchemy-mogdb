import sqlalchemy as sa
from pkg_resources import resource_filename
from sqlalchemy_mogdb.dialect import (
    MogDBDialect,
)


CERT_PATH = resource_filename("sqlalchemy_mogdb", "mogdb-ca-bundle.crt")


def test_ssl_args(mogdb_dialect_flavor):
    engine = sa.create_engine('{}://test'.format(mogdb_dialect_flavor))
    dialect = engine.dialect
    url = engine.url

    cargs, cparams = dialect.create_connect_args(url)

    assert cargs == []
    assert cparams.pop('host') == 'test'
    assert cparams.pop('sslmode') == 'verify-full'
    if isinstance(dialect, MogDBDialect):
        assert cparams.pop('sslrootcert') == CERT_PATH
    assert cparams == {}
