from birmingham_cabinet.api import employee_via_nino, get_claim, add_claim, update_claim
from discrepancies import comparable_values

def find_discrepancies(claim_id):
    claim = get_claim(claim_id)
    return find_discrepancies_in_claim(claim)


def find_discrepancies_in_claim(claim):
    discrepancies = {entry: values
                     for entry, values in comparable_values(claim).iteritems()
                     if values[0] != values[1]}
    return discrepancies


def has_discrepancies(claim_id):
    print find_discrepancies(claim_id)
    return len(find_discrepancies(claim_id)) > 0


def create_claim_2(claimant_information):
    claim_id = None
    nino = claimant_information['nino']
    employee_record = employee_via_nino(nino)
    if employee_record:
        claim_id = add_claim(
            claimant_information,
            employee_record
        )
    return claim_id


def add_details_to_claim(claim_id, claimant_details):
    claim = get_claim(claim_id)
    details = claimant_details
    claim[0].update(details)
    update_claim(claim_id, claimant_information=details)

