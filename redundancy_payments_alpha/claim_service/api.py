from birmingham_cabinet import api as cabinet_api
from discrepancies import comparable_values


def find_discrepancies(claim_id):
    claim = cabinet_api.get_claim(claim_id)
    return find_discrepancies_in_claim(claim)


def find_discrepancies_in_claim(claim):
    discrepancies = {entry: values
                     for entry, values in comparable_values(claim).iteritems()
                     if values[0] != values[1]}
    return discrepancies


def has_discrepancies(claim_id):
    return len(find_discrepancies(claim_id)) > 0


def create_claim_2(claimant_information):
    claim_id = None
    nino = claimant_information['nino']
    employee_record = cabinet_api.employee_via_nino(nino)
    if employee_record:
        claim_id = cabinet_api.add_claim(
            claimant_information,
            employee_record
        )
    return claim_id


def add_details_to_claim(claim_id, claimant_details):
    claim = cabinet_api.get_claim(claim_id)
    details = claimant_details
    claim[0].update(details)
    cabinet_api.update_claim(claim_id, claimant_information=details)


def submit(claim_id):
    cabinet_api.submit_claim(claim_id)


def summarise_claims():
    return None
