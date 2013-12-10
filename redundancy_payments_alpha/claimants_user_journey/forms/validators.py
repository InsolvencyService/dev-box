import re
from datetime import date
from wtforms.validators import Regexp, ValidationError, StopValidation, DataRequired


def convert_string_to_date(date_string):
    split_string = date_string.split('/')
    if type(split_string) != list or len(split_string) != 3:
        raise SyntaxError('Was expecting dd/MM/yyyy.')
    return date(int(split_string[2]), int(split_string[1]), int(split_string[0]))


class FutureDateValidator(Regexp):
    """
    Validates a date of birth text field.

    :param format_message:
        The message to use if the input is not in the expected format ('dd/MM/yyyy').
    :param future_message:
        The message to display if the date is in the future.
    """
    #
    def __init__(self, format_message, future_message):
        self.future_message = future_message
        super(FutureDateValidator, self).__init__(r'^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$', re.IGNORECASE, format_message)

    def __call__(self, form, field):
        message = self.message
        super(FutureDateValidator, self).__call__(form, field, message)
        extracted_date = convert_string_to_date(field.data)
        if self.future_message is None:
            self.future_message = 'Date cannot be in the future'

        if extracted_date > date.today():
            raise ValidationError(self.future_message)


class DateOfBirthValidator(Regexp):
    """
    Validates a date of birth text field.

    :param format_message:
        The message to use if the input is not in the expected format ('dd/MM/yyyy').
    :param range_message:
        The message to display if the date is not between Today and 1/1/1900.
    """
    #
    #message gets set to the value of format_message, to save messing around with the super class
    def __init__(self, format_message = None, range_message = None):
        self.format_message = format_message
        self.range_message = range_message
        super(DateOfBirthValidator, self).__init__(r'^[0-9]{1,2}[/][0-9]{1,2}[/][0-9]{4}$', re.IGNORECASE, format_message)

    def __call__(self, form, field):
        #Handle the regex/format part using the super class
        message = self.message
        super(DateOfBirthValidator, self).__call__(form, field, message)

        range_message = self.range_message
        if range_message == None:
            range_message = 'Date must be greater than or equal to 1900 and not in the future.'

        try:
            parsed_date = convert_string_to_date(field.data)
        except SyntaxError:
            raise ValidationError(range_message)
        if parsed_date.year < 1900 or parsed_date >= date.today():
            raise ValidationError(range_message)


class RequiredIfFieldHasValue(DataRequired):
    """
    Validator which makes a field required if another field has the specified value

    :param other_field_name:
        The name of the field to check for the value.
    :param other_field_value:
        The value to check for.
    """
    #
    def __init__(self, other_field_name, other_field_value, *args, **kwargs):
        self.other_field_name = other_field_name
        self.other_field_value = other_field_value
        super(RequiredIfFieldHasValue, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data == self.other_field_value:
            super(RequiredIfFieldHasValue, self).__call__(form, field)
        else:
            #If it gets this far then the field is optional
            field.errors[:] = []
            raise StopValidation()


class CustomDateFieldValidator(Regexp):
    """
    Validates the start date and end date custom date fields.

    """
    #
    def __init__(self, message=None, future_message=None, start_date_field_name=None):
        if message:
            self.message = message
        else:
            self.message = 'Date must be in the format dd/mm/yyyy.'

        if future_message:
            self.future_message = future_message
        else:
            self.future_message = 'Date must be greater than or equal to 1900 and not in the future.'

        self.start_date_field_name = start_date_field_name

    def __call__(self, form, field):
        try:
            parsed_date = date(int(field.data[2]), int(field.data[1]), int(field.data[0]))
        except (SyntaxError, ValueError):
            raise ValidationError(self.message)

        if parsed_date.year < 1900 or parsed_date >= date.today():
            raise ValidationError(self.future_message)

        if self.start_date_field_name:
            start_date_field = form._fields.get(self.start_date_field_name)
            if not start_date_field.errors:
                parsed_start_date = date(int(start_date_field.data[2]), int(start_date_field.data[1]), int(start_date_field.data[0]))

                if parsed_start_date > parsed_date:
                    raise ValidationError('The end date cannot be before the start date')
