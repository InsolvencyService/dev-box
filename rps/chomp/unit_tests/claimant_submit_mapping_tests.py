from hamcrest import assert_that, is_
from functools import partial
from helpers import get_value_from_xpath

# sut:
from chomp.payload_generator import generate_claimant_information_submit_request


def test_claimant_information_json_is_mapped_to_valid_champ_xml():
    """Generator of unit tests for each field we currently support.
    """
    # for these fields
    field_mapping = {
        "town_or_city": "//rp1:Claimant/rp1:Address/rp1:Town",
        "street": "//rp1:Claimant/rp1:Address/rp1:Line[2]",
        "forenames": "//rp1:Claimant/rp1:Name/rp1:Forename",
        "title": "//rp1:Claimant/rp1:Name/rp1:Title",
        "telephone_number": "//rp1:Claimant/rp1:PhoneNumber",
        "building_number": "//rp1:Claimant/rp1:Address/rp1:Line[1]",
        "date_of_birth": "//rp1:Claimant/rp1:DateOfBirth",
        "postcode": "//rp1:Claimant/rp1:Address/rp1:Postcode",
        "surname": "//rp1:Claimant/rp1:Name/rp1:Surname",
        "nino": "//rp1:Claimant/rp1:NINO"
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
    xml_payload = generate_claimant_information_submit_request(values_dict)
    # then
    xml_value = get_value_from_xpath(xpath_location, xml_payload)
    assert_that(xml_value, is_(values_dict[key]))
