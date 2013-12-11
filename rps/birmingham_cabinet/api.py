import contextlib
from datetime import datetime
import logging
from traceback import format_exc

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import func

from models import (
    ChompClaimLifecycle,
    Claim,
    Claimant,
    Employee,
    Employer,
)
from base import make_session, Base, local_unix_socket_engine
from customized_json import json_encode, json_decode
from birmingham_cabinet import chomp_states

logger = logging.getLogger(__name__)

def truncate_all_tables():
    with contextlib.closing(local_unix_socket_engine.connect()) as conn:
        trans = conn.begin()
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute("truncate table {table_name} cascade;".format(
                table_name=table.name))
        trans.commit()


def _multiple_results_hack(query):
    """In many parts of the code there should be only one
    """
    try:
        return query.one()
    except MultipleResultsFound as e:
        logger.warning("_multiple_results_hack caught MultipleResultsFound "
                       "for query: " + str(query) + "\n")
        logger.warning(format_exc())
        return query.first()


def employee_via_nino(nino):
    nino = nino.upper()
    with contextlib.closing(make_session()) as session:
        try:
            employee = _multiple_results_hack(
                session.query(Employee).filter(
                    Employee.nino == nino).one())
            return json_decode(employee.hstore)
        except NoResultFound:
            pass


def get_rp1_form():
    with contextlib.closing(make_session()) as session:
        claimant = _multiple_results_hack(
            session.query(Claimant).one())
        return json_decode(claimant.hstore)


def add_rp1_form(dictionary):
    with contextlib.closing(make_session()) as session:
        claimant = Claimant()
        claimant.nino = dictionary["nino"].upper()
        claimant.date_of_birth = dictionary["date_of_birth"]
        claimant.title = dictionary["title"]
        claimant.forenames = dictionary["forenames"]
        claimant.surname = dictionary["surname"]
        claimant.hstore = json_encode(dictionary)
        session.add(claimant)
        session.commit()


def add_rp14_form(dictionary):
    with contextlib.closing(make_session()) as session:
        employer = Employer()
        employer.ip_number = dictionary["ip_number"]
        employer.employer_name = dictionary["employer_name"]
        employer.company_number = dictionary["company_number"]
        employer.date_of_insolvency = dictionary["date_of_insolvency"]
        employer.hstore = json_encode(dictionary)
        session.add(employer)
        session.commit()


def add_rp14a_form(dictionary):
    with contextlib.closing(make_session()) as session:
        employee = Employee()
        employee.nino = dictionary["employee_national_insurance_number"].upper()
        employee.date_of_birth = dictionary["employee_date_of_birth"]
        employee.title = dictionary["employee_title"]
        employee.forenames = dictionary["employee_forenames"]
        employee.surname = dictionary["employee_surname"]
        # TODO: should we collect this on the form?
        employee.ip_number = "12345"
        employee.employer_name = dictionary["employer_name"]
        #TODO: Remove hack around decimals in JSON
        for decimal_key in ["employee_owed_wages_in_arrears",
                            "employee_holiday_owed",
                            "employee_basic_weekly_pay"]:
            if decimal_key in dictionary:
                dictionary[decimal_key] = str(dictionary[decimal_key])
        employee.hstore = json_encode(dictionary)
        session.add(employee)
        session.commit()


def add_claim(claimant_information, employee_record):
    with contextlib.closing(make_session()) as session:
        claim = Claim()
        claim.employer_id = employee_record.get('employer_id', None)
        claim.claimant_information = json_encode(claimant_information)
        claim.employee_record = json_encode(employee_record)
        session.add(claim)
        session.commit()
        return claim.claim_id


def get_claim(claim_id):
    with contextlib.closing(make_session()) as session:
        claim = _multiple_results_hack(
            session.query(Claim).filter(Claim.claim_id == claim_id).one())
        return (json_decode(claim.claimant_information),
                json_decode(claim.employee_record), claim.submitted_at)


def update_claim(claim_id, claimant_information=None, employee_record=None):
    with contextlib.closing(make_session()) as session:
        claim = _multiple_results_hack(
            session.query(Claim).filter(Claim.claim_id == claim_id).one())
        if claimant_information:
            updated_claimant_info = dict(
                json_decode(claim.claimant_information),
                **claimant_information
            )
            claim.claimant_information = json_encode(updated_claimant_info)
        if employee_record:
            updated_employee_record = dict(
                json_decode(claim.employee_record),
                **employee_record
            )
            claim.employee_record = json_encode(updated_employee_record)
        session.commit()


def claims_against_company(employer_id):
    with contextlib.closing(make_session()) as session:
        claims = session.query(Claim)\
            .filter(Claim.employer_id == employer_id).all()
        return [(json_decode(claim.claimant_information),
                 json_decode(claim.employee_record))
                for claim in claims]


def _current_time():
    return datetime.now()


def mark_claim_as_submitted(claim_id):
    with contextlib.closing(make_session()) as session:
        claim = _multiple_results_hack(
            session.query(Claim).filter(Claim.claim_id == claim_id).one())
        claim.submitted_at = _current_time()
        session.commit()


def get_claims_submitted_between(start, end):
    with contextlib.closing(make_session()) as session:
        claims = session.query(Claim).filter(Claim.submitted_at is not None)\
            .filter(Claim.submitted_at > start)\
            .filter(Claim.submitted_at < end).all()

        return [(claim.claimant_information,
                 claim.employee_record,
                 claim.submitted_at) for claim in claims]


def get_claims():
    with contextlib.closing(make_session()) as session:
        claims = session.query(Claim).all()

        return [(json_decode(claim.claimant_information),
                 json_decode(claim.employee_record),
                 claim.submitted_at) for claim in claims]


def get_next_claim_not_processed_by_chomp():
    with contextlib.closing(make_session()) as session:
        try:
            unprocessed_claim = _multiple_results_hack(
                session.query(Claim).filter(
                    Claim.chomp_claim_lifecycle == None).one())
            lifecycle = ChompClaimLifecycle()
            lifecycle.claim_id = unprocessed_claim.claim_id
            lifecycle.in_progress = datetime.now()
            session.add(lifecycle)
            session.commit()
            logger.info("Claim {claim_id} state changed to In Progress".format(
                claim_id=unprocessed_claim.claim_id))
            return unprocessed_claim.claim_id
        except NoResultFound:
            pass


def chomp_state_of_claim(claim_id):
    with contextlib.closing(make_session()) as session:
        claim = _multiple_results_hack(
            session.query(Claim).filter(
                Claim.claim_id == claim_id).one())
        return chomp_states.state_of_claim(claim)


def chomp_claim_done(claim_id):
    with contextlib.closing(make_session()) as session:
        claim = _multiple_results_hack(
            session.query(Claim).filter(
                Claim.claim_id == claim_id).one())
        claim.chomp_claim_lifecycle.done = datetime.now()
        session.commit()

