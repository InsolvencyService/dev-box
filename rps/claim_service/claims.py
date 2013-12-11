import string
from datetime import date, datetime

from claim_service.discrepancies import find_discrepancies_in_claim


def _initials(claimant_information):
    initials = None
    forenames = claimant_information.get('forenames')
    if forenames:
        first_letters = [name[0] for name in forenames.split(' ')]
        initials = string.join(first_letters)
    return initials


def _parse_date_of_birth(date_of_birth):
    ''' this is pretty horrible, it should go away
        once we've sorted out our dates '''
    if date_of_birth:
        day = int(date_of_birth[0])
        month = int(date_of_birth[1])
        year = int(date_of_birth[2])
    else:
        return None
    
    return date(year, month, day)


def _parse_employment_date(date_string):
    date_from_string = None
    if date_string:
        try:
            date_from_string = datetime.strptime(date_string, '%d/%m/%Y').date()
        except TypeError as e:
            pass

    return date_from_string


def summarise_claim(claim):
    claimant_information = claim[0]
    employee_information = claim[1]

    date_of_birth_dict = claimant_information.get('date_of_birth')
    employment_start = employee_information.get('employee_start_date')
    employment_end = employee_information.get('employee_end_date')
    
    claim_summary = {
        'discrepancy': bool(find_discrepancies_in_claim(claim)),
        'surname': claimant_information.get('surname'),
        'initials': (_initials(claimant_information)),
        'nino': claimant_information.get('nino'),
        'date_of_birth': _parse_date_of_birth(date_of_birth_dict),
        'date_submitted': claim[2],
        'employment_start_date': _parse_employment_date(employment_start),
        'employment_end_date': _parse_employment_date(employment_end)
    }
    return claim_summary

