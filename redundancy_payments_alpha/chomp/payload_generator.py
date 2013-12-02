import os
from jinja2 import Template, Environment, PackageLoader, StrictUndefined
from random import randint

environment = Environment(
    loader=PackageLoader("chomp", "templates"),
    # undefined=StrictUndefined,
)

def generate_dms_id():
    """This function just returns a random DMS id, while we are not integrating
    with Wisdom
    """
    return str(randint(6000000000, 7000000000))


def generate_accept_doc_request(dms_id):
    return environment.get_template("claimant_accept_doc.payload.xml").render(
        {"dms_id": dms_id})


def generate_claimant_information_submit_request(values_dict):
    """This function takes a dms_id and a json struct and returns a long string
    which is a rp1 request
    """
    return environment.get_template("claimant_submit.payload.xml").render(
        values_dict)


def generate_rp14_request(json_data):
    """This function takes the json data and returns a long string which is a
    valid rp14 xml request
    """
    return environment.get_template("employer_details.payload.xml").render(
        json_data)


def generate_rp14a_request(json_data):
    """This function takes the json data and returns a long string which is a
    valid rp14a xml request
    """
    return environment.get_template("employee_details.payload.xml").render(
        json_data)
