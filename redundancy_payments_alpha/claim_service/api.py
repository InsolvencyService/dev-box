

class _Claim(object):
    
    def __init__(self, claimant_information, employee_record):
        self.claimant_information = claimant_information
        self.employee_record = employee_record

    @property
    def discrepancies(self):
        result = {}
        # only compare values which are present in both the claimant and employee details
        for key in set(self.claimant_information.keys()).intersection(self.employee_record.keys()):
            claimant_value = self.claimant_information[key]
            employee_value = self.employee_record[key]
            if claimant_value != employee_value:
                result[key] = (claimant_value, employee_value)

        return result

def create_claim(personal_details):
    if personal_details['nino'] =='AB333333D':
        return _Claim(None, None)
 
    else:
        return None 
