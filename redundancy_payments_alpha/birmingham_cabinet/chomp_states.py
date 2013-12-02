from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

def is_ready(claim):
    return claim.chomp_claim_lifecycle is None

def is_in_progress(claim):
    return claim.chomp_claim_lifecycle.in_progress is not None

def is_done(claim):
    pass

def is_failed(claim):
    pass

def is_suspicious(claim):
    pass

states = OrderedDict([
    (is_ready, "Ready"),
    (is_in_progress, "In Progress"),
    (is_done, "Done"),
    (is_failed, "Failed"),
    (is_suspicious, "Suspicious"),
])

def status_of_claim(claim):
    for is_in_state, state_name in states.items():
        if is_in_state(claim):
            claim_id = claim.claim_id
            return state_name
