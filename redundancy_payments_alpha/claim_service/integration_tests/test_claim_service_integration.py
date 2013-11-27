import unittest
from decimal import Decimal

from nose.plugins.attrib import attr
from hamcrest import assert_that, has_entry, has_length, has_item, is_not, is_

import claim_service.api as api
from birmingham_cabinet.api import add_rp14a_form, truncate_all_tables, claims_against_company, add_claim


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
        assert_that(discrepancies, has_entry('gross_rate_of_pay', ('11.0', '300.5')))

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

    def test_retrieving_claims_by_company_id(self):
        claimant_data_1 = {'foo': 'bar'}
        employee_record_1 = {'employer_id': 1}

        add_claim(claimant_data_1, employee_record_1)
        claim = claims_against_company(1)

        assert_that(claim[0][0], has_entry("foo", "bar"))

    def test_summarise_claims(self):
        claimant_data_1 = {'foo': 'bar', 'nino': 'XX223344X'}
        employee_record_1 = {'employer_id': 1}

        claim_id = add_claim(claimant_data_1, employee_record_1)
        api.submit(claim_id)

        claims_summary = api.summarise_claims()

        assert_that(claims_summary, has_length(1))
        assert_that(claims_summary[0], has_entry('nino', 'XX223344X'))
        assert_that(claims_summary[0], has_entry('date_submitted', is_not(None)))
        assert_that(claims_summary[0], has_entry('discrepancy', is_(False)))

    def test_sumarise_claims_with_discrepancies(self):
        claimant_data_1 = {'nino': 'XX223344X', 'gross_rate_of_pay': 100}
        employee_record_1 = {'employer_id': 1, 'employee_basic_weekly_pay': 200}

        claim_id = add_claim(claimant_data_1, employee_record_1)

        claims_summary = api.summarise_claims()

        assert_that(claims_summary, has_length(1))
        assert_that(claims_summary[0], has_entry('discrepancy', is_(True)))
