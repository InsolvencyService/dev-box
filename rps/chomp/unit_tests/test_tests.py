from hamcrest import assert_that, is_


def test_law_of_excluded_middle():
    """Test the longstanding Aristotelian axiom.
    """
    assert_that(True, is_(True))
