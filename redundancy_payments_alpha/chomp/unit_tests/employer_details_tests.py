from hamcrest import assert_that, is_, has_item, none
import json
from functools import partial
from xml.dom.minidom import parseString
import xpath

# sut:
from ..chomp import generate_rp14_request

def test_claimant_information_json_is_mapped_to_valid_champ_xml():
    """Generator of unit tests for each field we currently support.
    """
    # for these fields
    field_mapping = {
        "company_name" : "//rp14:NameOfBusiness",
        "date_of_insolvency" : "//rp14:InsolvencyDate",
        "type_of_insolvency" : "//rp14:InsolvencyType",
        "insolvency_practitioner_name" : "//rp14:PayRecordsContact/rp14:Name",
        "address_line_1": "//rp14:PayRecordsContact/rp14:Address/rp14:Line[1]",
        "address_line_2": "//rp14:PayRecordsContact/rp14:Address/rp14:Line[2]",
        "town_or_city" : "//rp14:PayRecordsContact/rp14:Address/rp14:Town" ,
        "postcode": "//rp14:PayRecordsContact/rp14:Address/rp14:Postcode" ,
        "email_address" : "//rp14:PayRecordsContact/rp14:EmailAddress",
    }
    # test that
    for json_attribute, xpath_location in field_mapping.iteritems():
        generated_test = partial(check_value_is_mapped_into_xml, json_attribute, xpath_location)
        generated_test.description = '%s is mapped to %s in xml payload' % (json_attribute, xpath_location)
        yield generated_test,


def get_value_from_xpath(xml_doc, xpath_sel):
    """This is a test helper method which gets an attribute name and returns its
    value from an xml fragment using xpath.
    """
    # http://stackoverflow.com/questions/5572247/how-to-find-xml-elements-via-xpath-in-python-in-a-namespace-agnostic-way
    xml_dom = parseString(xml_doc)
    try:
        return xpath.findvalues(xpath_sel, xml_dom)[0]
    except IndexError:
        return None


def check_value_is_mapped_into_xml(json_attribute, xpath_location ):
    """Assertions on the xml payload to ensure that the json value has been populated
    as expected
    """
    # given
    values_dict = {}
    values_dict[json_attribute] = "test_value"
    # when
    xml_payload = generate_rp14_request(values_dict)
    xml_value = get_value_from_xpath(xml_payload, xpath_location)
    # then
    assert_that(xml_value, not none() )
    assert_that(xml_value, is_(values_dict[json_attribute]))



