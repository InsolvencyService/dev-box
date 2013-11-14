from datetime import datetime
import unittest

from nose.plugins.attrib import attr
from hamcrest import is_, assert_that, not_none

from birmingham_cabinet.api import (
    add_rp14a_form,
    employee_via_nino,
    truncate_all_tables,
    )
from birmingham_cabinet.models import Employee

@attr("integration")
class TestEmployee(unittest.TestCase):

    def tearDown(self):
        truncate_all_tables()

    def test_employee_via_nino(self):
        nino = "AB123456C"
        employee_dict = {
            "employee_national_insurance_number": nino,
            "employee_date_of_birth": "2012/1/1",
            "employee_title": "Mr",
            "employee_forenames": "Donald Duck",
            "employee_surname": "Quack",
            "employer_name": "McDuck Enterprises"
        }
        add_rp14a_form(employee_dict)
        employee = employee_via_nino(nino)
        assert_that(employee, is_(employee_dict))
