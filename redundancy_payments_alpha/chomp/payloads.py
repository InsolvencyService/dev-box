import os
from random import randint

from jinja2 import Template, Environment, PackageLoader, StrictUndefined

environment = Environment(
    loader=PackageLoader("chomp", "templates"),
    # FIXME: Turn strictness on once all the fields are being filled
    # undefined=StrictUndefined,
)

def dms_id():
    """This function just returns a random DMS id, while we are not integrating
    with Wisdom
    """
    return str(randint(6000000000, 7000000000))


def acceptdoc(dms_id):
    return environment.get_template("claimant_accept_doc.payload.xml").render(
        {"dms_id": dms_id})


def claimant_information(values_dict):
    """This function takes a dms_id and a json struct and returns a long string
    which is a rp1 request
    """
    return environment.get_template("claimant_submit.payload.xml").render(
        values_dict)


def rp14(json_data):
    """This function takes the json data and returns a long string which is a
    valid rp14 xml request
    """
    return environment.get_template("employer_details.payload.xml").render(
        json_data)


def rp14a(json_data):
    """This function takes the json data and returns a long string which is a
    valid rp14a xml request
    """
    return environment.get_template("employee_details.payload.xml").render(
        json_data)
