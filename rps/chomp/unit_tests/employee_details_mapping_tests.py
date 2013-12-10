from hamcrest import assert_that, is_
from functools import partial
from helpers import get_value_from_xpath

# sut:
from chomp.payload_generator import generate_rp14a_request


def test_claimant_information_json_is_mapped_to_valid_champ_xml():
    """Generator of unit tests for each field we currently support.
    """
    # for these fields
    field_mapping = {

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
    xml_payload = generate_rp14a_request(values_dict)
    # then
    xml_value = get_value_from_xpath(xpath_location, xml_payload)
    assert_that(xml_value, is_(values_dict[key]))
