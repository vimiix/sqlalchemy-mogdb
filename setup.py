from setuptools import setup

readme = open('README.rst').read()

setup(
    name='sqlalchemy-mogdb',
    version='0.1.1',
    description='Enmotech MogDB Dialect for SQLAlchemy',
    long_description_content_type='text/x-rst',
    long_description=readme,
    author='enmotech',
    maintainer='Vimiix',
    maintainer_email='i@vimiix.com',
    license="MIT",
    url='https://github.com/vimiix/sqlalchemy-mogdb',
    packages=['sqlalchemy_mogdb'],
    python_requires='>=3.4',
    keywords='Enmotech MogDB',
    install_requires=[
        # requires sqlalchemy.sql.base.DialectKWArgs.dialect_options, new in
        # version 0.9.2
        'SQLAlchemy>=0.9.2,<2.0.0',
        'packaging',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'mogdb = sqlalchemy_mogdb.dialect:MogDBDialect_psycopg2',
            'mogdb.psycopg2 = sqlalchemy_mogdb.dialect:MogDBDialect_psycopg2',
            'mogdb.psycopg2cffi = sqlalchemy_mogdb.dialect:MogDBDialect_psycopg2cffi',
        ]
    },
)
