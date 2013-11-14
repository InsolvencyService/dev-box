from hamcrest import assert_that, is_

from birmingham_cabinet.api import (
    add_rp1_form, 
    add_rp14_form,
    add_rp14a_form,
    )
from birmingham_cabinet.models import Claimant, Employer, Employee
from birmingham_cabinet.base import make_session
from datetime import datetime
import json

@when('we add a dictionary containing sample rp1 details')
def step(context):
    context.form = {
        'forenames': 'Donald',
        'surname': 'Duck',
        'title': 'Mr',
        'other': '',
        'address_line_1': '5 street name',
        'address_line_2': 'district name',
        'address_line_3': "", # FIXME: None instead of ""
        'town_or_city': 'Duckburg',
        'postcode': 'A1 2BC',
        'email': 'donald.duck@duckburg.com',
        'telephone_number': '12345 123456',
        'nino': 'AA112233B',
        'date_of_birth': '01/01/1900'
    }
    add_rp1_form(context.form)

@then('the data store should contain a claimant')
def step(context):
    session = make_session()
    try:
        claimant = session.query(Claimant).all()[0]
        date_of_birth = datetime.strptime(
            context.form["date_of_birth"], "%d/%m/%Y").date()
        assert_that(claimant.title, is_(context.form["title"]))
        assert_that(claimant.nino, is_(context.form["nino"]))
        assert_that(claimant.date_of_birth, is_(date_of_birth))
        decode_hstore = {key: json.loads(value)
                           for key, value in claimant.hstore.items()}
        assert_that(decode_hstore, is_(context.form))
    finally:
        session.close()

@when("we add a dictionary containing sample rp14 details")
def step(context):
    context.form = {
        "ip_number": "9314",
        "employer_name": "Mickey Mouse Enterprises",
        "company_number": "010101",
        "date_of_insolvency": "01/01/1900",
        "telephone_number": "12345 123456"
    }
    add_rp14_form(context.form)

@then("the data store should contain an employer")
def step(context):
    session = make_session()
    try:
        employer = session.query(Employer).all() [0]
        date_of_insolvency = datetime.strptime(
            context.form["date_of_insolvency"], "%d/%m/%Y").date()
        assert_that(employer.ip_number, is_(context.form["ip_number"]))
        assert_that(employer.employer_name, is_(context.form["employer_name"]))
        assert_that(employer.company_number, is_(context.form["company_number"]))
        assert_that(employer.date_of_insolvency, is_(date_of_insolvency))
        decode_hstore = {key: json.loads(value)
                         for key, value in employer.hstore.items()}
        assert_that(decode_hstore,
                    is_(context.form))
    finally:
        session.close()

@when("we add a dictionary containing sample rp14a details")
def step(context):
    context.form = {
        #"ip_number": "9314",  TODO: see api.py
        "employee_telephone_number": "0121 123 4567",
        'employee_forenames': 'Donald',
        'employee_surname': 'Duck',
        'employee_title': 'Mr',
        'employee_date_of_birth': '01/01/1900',
        'employee_national_insurance_number': 'AA112233B',
        "employer_name": "Mickey Mouse Enterprises",
    }
    add_rp14a_form(context.form)

@then("the data store should contain an employee")
def step(context):
    session = make_session()
    try:
        employee = session.query(Employee).all() [0]
        assert_that(employee.nino, is_(context.form["employee_national_insurance_number"]))
        decode_hstore = {key: json.loads(value)
                         for key, value in employee.hstore.items()}
        assert_that(decode_hstore, is_(context.form))
    finally:
        session.close()