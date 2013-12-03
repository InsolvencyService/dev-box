from datetime import date
import logging
import re
from wtforms import TextField, Form, SelectField, ValidationError
from wtforms.validators import AnyOf, DataRequired
from claimants_user_journey.forms.validators import DateOfBirthValidator, RequiredIfFieldHasValue, convert_string_to_date


class CurrencyField(TextField):
    """This is a subtype of the WTForm Text field which appends
    a pound-sign to the html.

    It does this as a monkey patch to the wtform.
    """
    def __call__(self, **kwargs):
        """See the depths of the __call__ method in Field
        to understand what is going on.
        """
        return "&pound; " + self.widget(self, **kwargs)

def blank_and_number_range_tuples(min, max_plus_one):
    lst = [('','')]
    lst += [(str(x), str(x)) for x in xrange(min, max_plus_one)]
    return lst


class DateForm(Form):

    day = SelectField(choices=blank_and_number_range_tuples(1, 32),
                      validators=[AnyOf(values=[str(x) for x in xrange(1, 32)],
                                        message='Day is a required field')])
    month = SelectField(choices=blank_and_number_range_tuples(1, 13),
                        validators=[AnyOf(values=[str(x) for x in xrange(1, 13)],
                                          message='Month is a required field')])
    year = TextField(validators=[DataRequired('Year is a required field'), ])

    @property
    def date(self):
        d = super(DateForm, self).data
        return "%(day)s/%(month)s/%(year)s" % d

    def validate_day(form, field):
        if not re.match(r'^[0-9]{1,2}[/][0-9]{1,2}[/][0-9]{4}$', form.date, re.IGNORECASE):
             raise ValidationError("Date must be in the format dd/mm/yyyy.")

        range_message = 'Date must be greater than or equal to 1900 and not in the future.'

        try:
            parsed_date = convert_string_to_date(form.date)
        except SyntaxError:
            raise ValidationError(range_message)
        if parsed_date.year < 1900 or parsed_date >= date.today():
            raise ValidationError(range_message)

    @property
    def errors(self):
        _err = []
        for (k,v) in super(DateForm,self).errors.iteritems():
            _err.extend(v)
        return _err

class UnvalidatedDateForm(DateForm):
    day = SelectField(choices=blank_and_number_range_tuples(1, 32))
    month = SelectField(choices=blank_and_number_range_tuples(1, 13))
    year = TextField()

    def validate_day(form, field):
        # Deliberately don't validate
        pass
