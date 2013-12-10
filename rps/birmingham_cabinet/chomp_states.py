from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

def is_ready(claim):
    return claim.chomp_claim_lifecycle is None

def is_in_progress(claim):
    return (
        (claim.chomp_claim_lifecycle.in_progress is not None)
        and
        (claim.chomp_claim_lifecycle.done is None)
        )


def is_done(claim):
    return claim.chomp_claim_lifecycle.done is not None

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

def state_of_claim(claim):
    claim_id = claim.claim_id
    for is_in_state, state_name in states.items():
        if is_in_state(claim):
            logger.debug("{claim_id} => {state_name}".format(**locals()))
            return state_name
        else:
            logger.debug("{claim_id} NOT {state_name}".format(**locals()))
