import unittest
from insolvency_practitioner_forms.forms.validators import validators
from wtforms import Form
from wtforms.validators import ValidationError


class FakeField():
    data = 'wibble'


class FakeFieldWithNoData():
    data = None


class FakeForm():
    field_to_validate = FakeField()


class TestDateValidator(unittest.TestCase):
    def test_date_validator_raises_validation_error(self):
        form = FakeForm()
        self.assertRaises(
            ValidationError,
            validators.parses_to_date,
            form,
            form.field_to_validate
        )
    
    def test_date_validator_raises_validation_error_when_field_is_empty(self):
        form = FakeForm()
        form.field_to_validate = FakeFieldWithNoData()
        self.assertRaises(
            ValidationError,
            validators.parses_to_date,
            form,
            form.field_to_validate
        )

