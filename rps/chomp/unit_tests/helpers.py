from xml.dom.minidom import parseString
from xpath import findvalues, XPathTypeError


def get_value_from_xpath(xpath_sel, xml_doc):
    """This is a test helper method which gets an attribute name and returns
    its value from an xml fragment using xpath.
    """
    xml_dom = parseString(xml_doc)
    try:
        return findvalues(xpath_sel, xml_dom)[0]
    except IndexError:
        raise Exception("%s not found in xml_document" % xpath_sel)
    except XPathTypeError:
        raise Exception("Invalid Xpath syntax")
