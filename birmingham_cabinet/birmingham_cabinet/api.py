from birmingham_cabinet.models import Claimant, Employer
from birmingham_cabinet.base import make_session

def add_rp1_form(dictionary):
    session = make_session()
    try:
        claimant = Claimant()
        claimant.nino = dictionary["nino"]
        claimant.date_of_birth = dictionary["date_of_birth"]
        claimant.title = dictionary["title"]
        claimant.forenames = dictionary["forenames"]
        claimant.surname = dictionary["surname"]
        claimant.hstore = dictionary
        session.add(claimant)
        session.commit()
    finally:
        session.close()

def add_rp14_form(dictionary):
    session = make_session()
    try:
        employer = Employer()
        employer.employer_name = dictionary["employer_name"]
        employer.company_number = dictionary["company_number"]
        employer.date_of_insolvency = dictionary["date_of_insolvency"]
        employer.hstore = dictionary
        session.add(employer)
        session.commit()
    finally:
        session.close()