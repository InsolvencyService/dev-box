import unittest
from decimal import Decimal
from datetime import date

import simplejson as json
from hamcrest import assert_that, is_

from birmingham_cabinet.customized_json import encode_special_types, decode_special_types

class TestJsonEncoder(unittest.TestCase):

    def test_date_encoding(self):
        dt = date(2013, 2, 28)
        expected_json = json.dumps({
            "something": {
                "__date__": True,
                "iso_format": dt.isoformat()
            }})
        actual_json = json.dumps({"something": dt}, default=encode_special_types)
        assert_that(actual_json, is_(expected_json))

    def test_date_decoding(self):
        dt = date(2013, 2, 28)
        expected_dict = {"something": dt}
        actual_dict = json.loads(
            '{"something": {"__date__": true, "iso_format": "2013-2-28"}}',
            object_hook=decode_special_types
        )
        assert_that(actual_dict, is_(expected_dict))

    def test_date_encoding_and_decoding(self):
        dict_with_date = { "something": date(2013, 2, 5) }
        json_with_date = '{"something": {"__date__": true, "iso_format": "2013-02-05"}}'
        assert_that(
            json.loads(
                json.dumps(
                    dict_with_date,
                    default=encode_special_types
                ),
                object_hook=decode_special_types
            ),
            is_(dict_with_date)
        )
        assert_that(
            json.dumps(
                json.loads(
                    json_with_date,
                    object_hook=decode_special_types
                ),
                default=encode_special_types
            ),
            is_(json_with_date)
        )
