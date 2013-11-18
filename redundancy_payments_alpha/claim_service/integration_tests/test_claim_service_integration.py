import unittest
from decimal import Decimal

from nose.plugins.attrib import attr
from hamcrest import assert_that, has_entry

import claim_service.api as api
from birmingham_cabinet.api import add_rp14a_form, truncate_all_tables

@attr("integration")
class TestClaimServiceIntegration(unittest.TestCase):
    def setUp(self):
        add_rp14a_form(
            {
                'employee_national_insurance_number': 'XX223344X',
                'employee_date_of_birth': '01/01/1990',
                'employee_title': 'Mr',
                'employee_surname': 'SURNAME',
                'employee_forenames': 'FORENAMES',
                'employer_name': 'Widgets Inc',
                'employee_basic_weekly_pay': Decimal('300.5')
            }
        ) 

    def tearDown(self):
        truncate_all_tables()

    def test_creating_updating_and_finding_discrepancies_on_a_claim(self):
        personal_details = {
            'nino': 'XX223344X'
        }
        claimant_details = {
            'gross_rate_of_pay': '11.0'
        }
        
        claim_id = api.create_claim_2(personal_details)
        api.add_details_to_claim(claim_id, claimant_details)
        discrepancies = api.find_discrepancies(claim_id)
        assert_that(discrepancies, has_entry('gross_rate_of_pay', ('11.0','300.5')))
    
    def test_updating_claim_information(self):
        personal_details = {'nino': 'XX223344X'}
        claimant_details = {'gross_rate_of_pay': '11.0'}
        claimant_details_updated = {
            'gross_rate_of_pay': '12.0',
        }
        
        claim_id = api.create_claim_2(personal_details)
        api.add_details_to_claim(claim_id, claimant_details)

        assert_that(api.find_discrepancies(claim_id),
            has_entry('gross_rate_of_pay', ('11.0', '300.5')))

        api.add_details_to_claim(claim_id, claimant_details_updated)

        assert_that(api.find_discrepancies(claim_id),
            has_entry('gross_rate_of_pay', ('12.0', '300.5')))

