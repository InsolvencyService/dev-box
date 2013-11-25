from birmingham_cabinet.api import get_rp1_form
from payload_generator import generate_claimant_information_submit_request

import json

def evaluate_forms():
    claim = get_rp1_form()
    return generate_claimant_information_submit_request(claim)

