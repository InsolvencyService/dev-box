from birmingham_cabinet.api import employee_via_nino

class _Claim(object):
    
    def __init__(self, claimant_information, employee_record):
        self.claimant_information = claimant_information
        self.employee_record = employee_record

    @property
    def discrepancies(self):
        result = {}
        # FIXME: this should live in an entity object somewhere else
        if 'gross_rate_of_pay' in self.claimant_information.keys():
            self.employee_record.update({'gross_rate_of_pay': self.employee_record['employee_basic_weekly_pay']})

        # only compare values which are present in both the claimant and employee details
        for key in set(self.claimant_information.keys()).intersection(self.employee_record.keys()):
            claimant_value = self.claimant_information[key]
            employee_value = self.employee_record[key]
            if claimant_value != employee_value:
                result[key] = (claimant_value, employee_value)

        return result

def create_claim(personal_details):
    employee_details = employee_via_nino(personal_details["nino"])
    if employee_details == None:
        return None
    else:
        return _Claim(personal_details, employee_details)
 
