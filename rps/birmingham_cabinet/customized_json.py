from datetime import date, datetime

import simplejson as json


def json_encode(dictionary):
    return {key: json.dumps(value, default=encode_special_types)
            for key, value in dictionary.items()}


def json_decode(dictionary):
    return {key: json.loads(value, object_hook=decode_special_types)
            for key, value in dictionary.items()}


def encode_special_types(obj):
    if isinstance(obj, date):
        return {
            "__date__": True,
            "iso_format": obj.isoformat()
        }
    else:
        raise TypeError


def decode_special_types(obj):
    iso_format = "%Y-%m-%d"
    if "__date__" in obj:
        return datetime.strptime(obj["iso_format"], iso_format).date()
    else:
        return obj
