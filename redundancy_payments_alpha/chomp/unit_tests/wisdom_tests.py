from hamcrest import assert_that, is_, greater_than_or_equal_to

# sut:
from chomp.payloads import dms_id


def test_generated_dms_id_should_not_conflict_with_production_ones():
    """Wisdom already generates DMS ids upto 9 digits long and therefore we
    need to generate ids which are longer.
    """
    # when
    id = dms_id()
    # then
    assert_that(type(id), is_(type(str)))
    assert_that(len(id), greater_than_or_equal_to(10))
