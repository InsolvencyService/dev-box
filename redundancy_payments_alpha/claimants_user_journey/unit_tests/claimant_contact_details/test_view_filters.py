# -*- coding: utf-8 -*- 

from hamcrest import assert_that, is_

from claimants_user_journey.view_filters.filters import discrepancy_message, summary_message


def test_discrepancy_message_filter_with_numbers():
    # given
    discrepancy = (u"950", u"340")
    # when
    output = discrepancy_message(discrepancy)
    # then
    assert_that(output, is_(u"The value you provided was 950 but the insolvency practitioner handling this case suggested 340."))


def test_summary_message_filter_with_numbers():
    # given
    discrepancy = (u"950", u"340")
    # when
    output = summary_message(discrepancy)
    # then
    assert_that(output, is_(u"The Insolvency Practitioner has suggested 950. Your payment will be calculated using the lower figure of 950"))
