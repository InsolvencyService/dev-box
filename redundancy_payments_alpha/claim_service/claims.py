import string
from claim_service.discrepancies import find_discrepancies_in_claim


def _initials(claimant_information):
    initials = None
    forenames = claimant_information.get('forenames')
    if forenames:
        first_letters = [name[0] for name in forenames.split(' ')]
        initials = string.join(first_letters)
    return initials


def summarise_claim(claim):
    claimant_information = claim[0]
    claim_summary = {
        'discrepancy': bool(find_discrepancies_in_claim(claim)),
        'surname': claimant_information.get('surname'),
        'initials': (_initials(claimant_information)),
        'nino': claimant_information.get('nino'),
        'date_of_birth': claimant_information.get('date_of_birth'),
        'date_submitted': claim[2]
    }
    return claim_summary
