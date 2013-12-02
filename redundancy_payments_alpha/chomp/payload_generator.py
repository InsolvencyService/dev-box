import os
from jinja2 import Template
from random import randint

TEMPLATE_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')

RP1_ACCEPT_DOC_TEMPLATE = "claimant_accept_doc.payload.xml"
RP1_SUBMIT_FORM_TEMPLATE = "claimant_submit.payload.xml"
RP14_TEMPLATE = "employer_details.payload.xml"
RP14A_TEMPLATE = "employee_details.payload.xml"


def read_xml_template_from(filename):
    """This code should read in a xml template from a file,
    """
    with open(os.path.join(TEMPLATE_DIR, filename)) as f:
        template = f.read()
    return template


def generate_dms_id():
    """This function just returns a random DMS id, while we are not integrating
    with Wisdom
    """
    return str(randint(6000000000, 7000000000))


def generate_accept_doc_request(dms_id):
    return generate_payload_with_template({"dms_id": dms_id}, RP1_ACCEPT_DOC_TEMPLATE)


def generate_payload_with_template(values_dict, template_filename):
    """General function which returns a string from a jinja template of the xml
    payload specified in the filename with the values in values_dict passed in.
    """
    xml_template = read_xml_template_from(template_filename)
    template = Template(xml_template)
    return template.render(values_dict)


def generate_claimant_information_submit_request(values_dict):
    """This function takes a dms_id and a json struct and returns a long string
    which is a rp1 request
    """
    return generate_payload_with_template(values_dict,
                                          RP1_SUBMIT_FORM_TEMPLATE)


def generate_rp14_request(json_data):
    """This function takes the json data and returns a long string which is a
    valid rp14 xml request
    """
    xml_template = read_xml_template_from(RP14_TEMPLATE)
    template = Template(xml_template)
    return template.render(json_data)


def generate_rp14a_request(json_data):
    """This function takes the json data and returns a long string which is a
    valid rp14a xml request
    """
    xml_template = read_xml_template_from(RP14A_TEMPLATE)
    template = Template(xml_template)
    return template.render(json_data)
