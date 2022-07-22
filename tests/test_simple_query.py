from rs_sqla_test_utils import models


def test_simple_query(mogdb_session):
    mogdb_session.add(models.Basic(name='Freda'))
    assert mogdb_session.query(models.Basic.name).first().name == 'Freda'
