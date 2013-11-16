import unittest

from nose.plugins.attrib import attr
from hamcrest import assert_that, is_

from birmingham_cabinet.api import add_claim, get_claim, truncate_all_tables, update_claim
from birmingham_cabinet.models import Claim

@attr("integration")
class TestClaim(unittest.TestCase):

    def tearDown(self):
        truncate_all_tables()

    def test_creating_a_claim(self):
        claim_id = 1
        claim_data = {
            'claim_id': claim_id,
            'foo': 'bar'
        }
        add_claim(claim_data)
        claim = get_claim(claim_id)
        assert_that(claim['foo'], is_('bar'))

    def test_creating_multiple_claims(self):        
        claim_1_data = {
            'claim_id': 1,
            'foo': 'bar'
        }
        claim_2_data = {
            'claim_id': 2,
            'foo': 'zap'
        }
        claim_3_data = {
            'claim_id': 3,
            'foo': 'pow'
        }
        add_claim(claim_1_data)
        add_claim(claim_2_data)
        add_claim(claim_3_data)

        claim = get_claim(3)
        assert_that(claim['foo'], is_('pow'))

    def test_updating_a_claim(self):
        claim_data = {
            'claim_id': 1,
            'foo': 'bar'
        }

        updated_claim_data = {
            'claim_id': 1,
            'foo': 'mongoose',
            'zap': 'pow'
        }

        add_claim(claim_data)
        update_claim(updated_claim_data)

        claim = get_claim(1)
        assert_that(claim['zap'], is_('pow'))
        assert_that(claim['foo'], is_('mongoose'))

