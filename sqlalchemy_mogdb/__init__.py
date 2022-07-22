from pkg_resources import DistributionNotFound, get_distribution, parse_version

for package in ['psycopg2', 'psycopg2-binary', 'psycopg2cffi']:
    try:
        if get_distribution(package).parsed_version < parse_version('2.5'):
            raise ImportError('Minimum required version for psycopg2 is 2.5')
        break
    except DistributionNotFound:
        pass

__version__ = get_distribution('sqlalchemy-mogdb').version

from sqlalchemy.dialects import registry  # noqa

registry.register(
    "mogdb", "sqlalchemy_mogdb.dialect",
    "MogDBDialect_psycopg2"
)
registry.register(
    "mogdb.psycopg2", "sqlalchemy_mogdb.dialect",
    "MogDBDialect_psycopg2"
)
registry.register(
    'mogdb+psycopg2cffi', 'sqlalchemy_mogdb.dialect',
    'MogDBDialect_psycopg2cffi',
)


