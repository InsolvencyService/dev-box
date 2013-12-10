from hamcrest import assert_that, is_
from functools import partial
from helpers import get_value_from_xpath

# sut:
from chomp.payload_generator import generate_rp14_request


def test_claimant_information_json_is_mapped_to_valid_champ_xml():
    """Generator of unit tests for each field we currently support.
    """
    # for these fields
    field_mapping = {
        "company_name": "//rp14:NameOfBusiness",
        "date_of_insolvency": "//rp14:InsolvencyDate",
        "type_of_insolvency": "//rp14:InsolvencyType",
        "insolvency_practitioner_name": "//rp14:PayRecordsContact/rp14:Name",
        "address_line_1": "//rp14:PayRecordsContact/rp14:Address/rp14:Line[1]",
        "address_line_2": "//rp14:PayRecordsContact/rp14:Address/rp14:Line[2]",
        "town_or_city": "//rp14:PayRecordsContact/rp14:Address/rp14:Town",
        "postcode": "//rp14:PayRecordsContact/rp14:Address/rp14:Postcode",
        "email_address": "//rp14:PayRecordsContact/rp14:EmailAddress",
    }
    # test that
    for json_attribute, xpath_location in field_mapping.iteritems():
        generated_test = partial(check_value_is_mapped_into_xml,
                                 json_attribute, xpath_location)
        generated_test.description = '%s is mapped to %s in xml payload' \
                                     % (json_attribute, xpath_location)
        yield generated_test,


def check_value_is_mapped_into_xml(key, xpath_location):
    """Assertions on the xml payload to ensure that the json value has been
    populated as expected
    """
    # given
    values_dict = {key: "test_value"}
    # when
    xml_payload = generate_rp14_request(values_dict)
    # then
    xml_value = get_value_from_xpath(xpath_location, xml_payload)
    assert_that(xml_value, is_(values_dict[key]))
