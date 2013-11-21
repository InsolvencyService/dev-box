import unittest

from nose.plugins.attrib import attr
from hamcrest import assert_that, is_, has_length

from birmingham_cabinet.api import add_claim, get_claim, truncate_all_tables, update_claim, claims_against_company
from birmingham_cabinet.models import Claim

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
        claimant_data = {'foo': 'bar'}
        employee_record = {'foo': 'baz'}

        updated_claimant_data = {
            'foo': 'mongoose',
            'zap': 'pow'
        }

        claim_id = add_claim(claimant_data, employee_record)

        claim = get_claim(claim_id)

        assert_that(claim[0]['foo'], is_('bar'))
        assert_that(claim[1]['foo'], is_('baz'))

        update_claim(claim_id, claimant_information=updated_claimant_data)

        updated_claim = get_claim(claim_id)
        assert_that(updated_claim[0]['zap'], is_('pow'))
        assert_that(updated_claim[0]['foo'], is_('mongoose'))
        assert_that(updated_claim[1]['foo'], is_('baz'))

