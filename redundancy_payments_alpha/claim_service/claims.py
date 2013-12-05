import string
from datetime import date

from claim_service.discrepancies import find_discrepancies_in_claim


def _initials(claimant_information):
    initials = None
    forenames = claimant_information.get('forenames')
    if forenames:
        first_letters = [name[0] for name in forenames.split(' ')]
        initials = string.join(first_letters)
    return initials


def _parse_date_of_birth(date_of_birth_dict):
    ''' this is pretty horrible, it should go away
        once we've sorted out our dates '''
    if date_of_birth_dict:
        day = int(date_of_birth_dict['day'])
        month = int(date_of_birth_dict['month'])
        year = int(date_of_birth_dict['year'])
    else:
        return None
    
    return date(year, month, day)


def summarise_claim(claim):
    claimant_information = claim[0]

    date_of_birth_dict = claimant_information.get('date_of_birth')
    
    claim_summary = {
        'discrepancy': bool(find_discrepancies_in_claim(claim)),
        'surname': claimant_information.get('surname'),
        'initials': (_initials(claimant_information)),
        'nino': claimant_information.get('nino'),
        'date_of_birth': _parse_date_of_birth(date_of_birth_dict),
        'date_submitted': claim[2]
    }
    return claim_summary

