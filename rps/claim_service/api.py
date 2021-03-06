from datetime import datetime, timedelta
from birmingham_cabinet import api as cabinet_api
from claim_service.claims import summarise_claim
from claim_service.discrepancies import find_discrepancies_in_claim


class NoEmployeeException(Exception):
    pass

def _current_time():
    return datetime.now()


def find_discrepancies(claim_id):
    claim = cabinet_api.get_claim(claim_id)
    return find_discrepancies_in_claim(claim)


def has_discrepancies(claim_id):
    return len(find_discrepancies(claim_id)) > 0


def create_claim_2(claimant_information):
    nino = claimant_information['nino']
    employee_record = cabinet_api.employee_via_nino(nino)
    if employee_record:
        claim_id = cabinet_api.add_claim(
            claimant_information,
            employee_record
        )
        return claim_id
    else:
        raise NoEmployeeException(
            "Can't create a claim without first creating an employee")


def add_details_to_claim(claim_id, claimant_details):
    cabinet_api.update_claim(
        claim_id,
        claimant_information=claimant_details
    )


def submit(claim_id):
    cabinet_api.mark_claim_as_submitted(claim_id)


def summarise_claims():
    claims = cabinet_api.get_claims()
    stuff_to_return = []
    for claim in claims:
        stuff_to_return.append(summarise_claim(claim))
    return stuff_to_return


def claims_submitted_in_last_24_hours():
    now = _current_time()
    a_day = timedelta(days=1)
    yesterday = now - a_day

    return cabinet_api.get_claims_submitted_between(
        start=yesterday,
        end=now
    )

