from birmingham_cabinet.api import get_rp1_form
from payloads import claimant_information

import json

def evaluate_forms():
    claim = get_rp1_form()
    return claimant_information(claim)

