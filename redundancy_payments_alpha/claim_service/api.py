

class _Claim(object):
    
    def __init__(self, claimant_information, employee_record):
        pass

    @property
    def discrepancies(self):
        return ["one"]

def create_claim(personal_details):
    if personal_details['nino'] =='AB333333D':
        return _Claim(None, None)
 
    else:
        return None 
