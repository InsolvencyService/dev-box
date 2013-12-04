from datetime import datetime
import unittest
from mock import patch

from nose.plugins.attrib import attr
from hamcrest import assert_that, is_, has_length, has_entry, none, not_none

from birmingham_cabinet.api import (
    add_claim,
    get_claim,
    truncate_all_tables,
    update_claim,
    get_claims,
    mark_claim_as_submitted,
    get_claims_submitted_between, get_next_claim_not_processed_by_chomp)


@attr("integration")
class TestClaim(unittest.TestCase):

    def tearDown(self):
        truncate_all_tables()

    def test_creating_a_claim(self):
        claimant_information = {
            'foo': 'bar'
        }

        employee_record = {
            'foo': 'zap'
        }

        claim_id = add_claim(claimant_information, employee_record)
        claim = get_claim(claim_id)
        assert_that(claim[0]['foo'], is_('bar'))
        assert_that(claim[1]['foo'], is_('zap'))

    def test_creating_multiple_claims(self):
        claimant_1_data = {'foo': 'bar'}
        claimant_2_data = {'foo': 'zap'}
        claimant_3_data = {'foo': 'pow'}
        employee_record_1 = {'x': '1'}
        employee_record_2 = {'x': '2'}
        employee_record_3 = {'x': '3'}
        add_claim(claimant_1_data, employee_record_1)
        add_claim(claimant_2_data, employee_record_2)

        claim_3_id = add_claim(claimant_3_data, employee_record_3)

        claim = get_claim(claim_3_id)
        assert_that(claim[0]['foo'], is_('pow'))
        assert_that(claim[1]['x'], is_('3'))

    def test_updating_a_claim(self):
        claimant_data = {'foo': 'bar', 'unchanged': 'grep'}
        employee_record = {'foo': 'baz'}

        updated_claimant_data = {
            'foo': 'mongoose',
            'zap': 'pow'
        }

        claim_id = add_claim(claimant_data, employee_record)

        claim = get_claim(claim_id)

        assert_that(claim[0]['foo'], is_('bar'))
        assert_that(claim[0]['unchanged'], is_('grep'))
        assert_that(claim[1]['foo'], is_('baz'))

        update_claim(claim_id, claimant_information=updated_claimant_data)

        updated_claim = get_claim(claim_id)
        assert_that(updated_claim[0]['zap'], is_('pow'))
        assert_that(updated_claim[0]['foo'], is_('mongoose'))
        assert_that(updated_claim[0]['unchanged'], is_('grep'))
        assert_that(updated_claim[1]['foo'], is_('baz'))

    def test_retrieving_claims(self):
        claimant_1_data = {'foo': 'bar'}
        claimant_2_data = {'foo': 'zap'}
        claimant_3_data = {'foo': 'pow'}
        employee_record_1 = {'x': '1'}
        employee_record_2 = {'x': '2'}
        employee_record_3 = {'x': '3'}
        add_claim(claimant_1_data, employee_record_1)
        add_claim(claimant_2_data, employee_record_2)
        add_claim(claimant_3_data, employee_record_3)

        claims = get_claims()
        assert_that(claims, has_length(3))
        assert_that(claims[0][0], has_entry('foo', is_('bar')))

    @patch('birmingham_cabinet.api._current_time')
    def test_submitting_claim(self, mock_time):
        mock_time.return_value = datetime(1990, 1, 1, 1)
        claimant_data = {'foo': 'bar'}
        employee_record = {'x': '1'}

        claim_id = add_claim(claimant_data, employee_record)

        mark_claim_as_submitted(claim_id)

        claim = get_claim(claim_id)
        assert_that(claim[2], is_(datetime(1990, 1, 1, 1)))

    @patch('birmingham_cabinet.api._current_time')
    def test_getting_submitted_claims_since_a_given_time(self, mock_time):
        mock_time.return_value = datetime(1990, 1, 1, 1)
        claimant_1_data = {'foo': 'bar'}
        employee_record_1 = {'x': '1'}
        claim_id = add_claim(claimant_1_data, employee_record_1)
        mark_claim_as_submitted(claim_id)

        claims = get_claims_submitted_between(
            start=datetime(1990, 1, 1),
            end=datetime(1990, 1, 2)
        )

        assert_that(claims, has_length(1))
        assert_that(claims[0][2], is_(datetime(1990, 1, 1, 1)))

    def test_should_return_next_unprocessed_claim(self):
        add_claim({}, {})
        claim = get_next_claim_not_processed_by_chomp()

        assert_that(claim, is_(not_none()))

    def test_should_return_none_if_no_unprocessed_claims(self):
        add_claim({}, {})
        get_next_claim_not_processed_by_chomp()
        claim = get_next_claim_not_processed_by_chomp()

        assert_that(claim, is_(None))
