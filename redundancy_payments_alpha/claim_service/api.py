from birmingham_cabinet.api import employee_via_nino, get_claim, add_claim
from discrepancies import comparable_values

class _Claim(object):
    _mappings = {
        'employee_basic_weekly_pay': 'gross_rate_of_pay'
    }
    
    def __init__(self, claimant_information, employee_record):
        self.claimant_information = claimant_information
        self.employee_record = self._map_employee_record_keys(employee_record)

    def _map_employee_record_keys(self, employee_record):
        # FIXME: this should live in an entity object somewhere else
        keys = set(self._mappings.keys()).intersection(employee_record.keys())

        for key in keys:
            employee_record.update(
                {self._mappings[key]: employee_record[key]}
            )

        return employee_record

    @property
    def discrepancies(self):
        result = {}

        # only compare values which are present in both the claimant and employee details
        for key in set(self.claimant_information.keys()).intersection(self.employee_record.keys()):
            claimant_value = str(self.claimant_information[key])
            employee_value = str(self.employee_record[key])
            if claimant_value != employee_value:
                result[key] = (claimant_value, employee_value)

        return result


def create_claim(personal_details):
    employee_details = employee_via_nino(personal_details["nino"])
    if employee_details == None:
        return None
    else:
        return _Claim(personal_details, employee_details)


def find_discrepancies(claim_id):
    claim = get_claim(claim_id)
    discrepancies = {entry: values for entry, values in comparable_values(claim).iteritems() if values[0] != values[1]} 
    return discrepancies


def create_claim_2(personal_details):
    claim_id = None
    nino = personal_details['nino']
    employee_record = employee_via_nino(nino)
    if employee_record:
        claim_id = add_claim(personal_details, employee_record)
    return claim_id

