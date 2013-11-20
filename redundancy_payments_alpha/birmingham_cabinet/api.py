import contextlib
import simplejson as json
from datetime import date, datetime

from sqlalchemy.orm.exc import NoResultFound

from models import Claim, Claimant, Employer, Employee
from base import make_session, Base, local_unix_socket_engine
from customized_json import encode_dict, decode_dict


def truncate_all_tables():
    with contextlib.closing(local_unix_socket_engine.connect()) as conn:
        trans = conn.begin()
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute("truncate table {table_name}".format(table_name=table.name))
        trans.commit()

def employee_via_nino(nino):
    with contextlib.closing(make_session()) as session:
        try:
            employee = session.query(Employee).filter(Employee.nino == nino).one()
            return decode_dict(employee.hstore)
        except NoResultFound:
            pass

def get_rp1_form():
    with contextlib.closing(make_session()) as session:
        claimant = session.query(Claimant).one()
        return decode_dict(claimant.hstore)

def add_rp1_form(dictionary):
    with contextlib.closing(make_session()) as session:
        claimant = Claimant()
        claimant.nino = dictionary["nino"]
        claimant.date_of_birth = dictionary["date_of_birth"]
        claimant.title = dictionary["title"]
        claimant.forenames = dictionary["forenames"]
        claimant.surname = dictionary["surname"]
        claimant.hstore = encode_dict(dictionary)
        session.add(claimant)
        session.commit()


def add_rp14_form(dictionary):
    with contextlib.closing(make_session()) as session:
        employer = Employer()
        employer.ip_number = dictionary["ip_number"]
        employer.employer_name = dictionary["employer_name"]
        employer.company_number = dictionary["company_number"]
        employer.date_of_insolvency = dictionary["date_of_insolvency"]
        employer.hstore = encode_dict(dictionary)
        session.add(employer)
        session.commit()


def add_rp14a_form(dictionary):
    with contextlib.closing(make_session()) as session:
        employee = Employee()
        employee.nino = dictionary["employee_national_insurance_number"]
        employee.date_of_birth = dictionary["employee_date_of_birth"]
        employee.title = dictionary["employee_title"]
        employee.forenames = dictionary["employee_forenames"]
        employee.surname =  dictionary["employee_surname"]
        employee.ip_number = "12345" #TODO: should we collect this on the form?
        employee.employer_name = dictionary["employer_name"]
        #TODO: Remove hack around decimals in JSON
        for decimal_key in ["employee_owed_wages_in_arrears", "employee_holiday_owed", "employee_basic_weekly_pay"]:
            if decimal_key in dictionary:
                dictionary[decimal_key] = str(dictionary[decimal_key])
        employee.hstore = encode_dict(dictionary)
        session.add(employee)
        session.commit()


def add_claim(claimant_information, employee_record):
    with contextlib.closing(make_session()) as session:
        claim = Claim()
        claim.claimant_information = encode_dict(claimant_information)
        claim.employee_record = encode_dict(employee_record)
        session.add(claim)
        session.commit()
        return claim.claim_id


def get_claim(claim_id):
    with contextlib.closing(make_session()) as session:
        claim = session.query(Claim).filter(Claim.claim_id==claim_id).one()
        return (decode_dict(claim.claimant_information),
                decode_dict(claim.employee_record))


def update_claim(claim_id, claimant_information=None, employee_record=None):
    with contextlib.closing(make_session()) as session:
        claim = session.query(Claim).filter(Claim.claim_id==claim_id).one()
        if claimant_information:
            claim.claimant_information = encode_dict(claimant_information)
        if employee_record:
            claim.employee_record = encode_dict(employee_record)
        session.commit()


def claims_against_company(company_id):
    pass
