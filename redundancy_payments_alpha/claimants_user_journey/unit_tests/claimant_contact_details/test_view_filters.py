# -*- coding: utf-8 -*- 

from hamcrest import assert_that, is_

from claimants_user_journey.view_filters.filters import discrepancy_message


def test_existing_functionality():
    # given
    discrepancy = (u"950", u"340")
    # when
    output = discrepancy_message(discrepancy)
    # then
    print output
    assert_that(output, is_(u"The value you provided was 950 but the insolvency practitioner handling this case suggested 340."))
