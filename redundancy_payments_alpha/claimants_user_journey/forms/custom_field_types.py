from datetime import date
import logging
import re
from wtforms import TextField, Form, SelectField, ValidationError, Field
from wtforms.validators import AnyOf, DataRequired
from wtforms.widgets.core import HTMLString
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


class CustomDateWidget(object):
    def __init__(self, error_class=u'has_errors'):
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field and field.data:
            kwargs.setdefault('id', field.id)

            #Day drop down list
            html = ["<select id=\"%s-day\" name=\"%s\">" % (field.id, field.name)]
            for x in xrange(0, 32):
                if x == 0:
                    val = ""
                else:
                    val = str(x)

                if val == field.data[0]:
                    html.append("<option value=\"%s\" selected>%s</option>" % (val, val))
                else:
                    html.append("<option value=\"%s\">%s</option>" % (val, val))
            html.append('</select>')

            #Month drop down list
            html.append("<select id=\"%s-month\" name=\"%s\">" % (field.id, field.name))
            for x in xrange(0, 13):
                if x == 0:
                    val = ""
                else:
                    val = str(x)

                if val == field.data[1]:
                    html.append("<option value=\"%s\" selected>%s</option>" % (val, val))
                else:
                    html.append("<option value=\"%s\">%s</option>" % (val, val))
            html.append('</select>')

            #Year text field
            html.append("<input id=\"%s-year\" name=\"%s\" type=\"text\" value=\"%s\">" % (field.id, field.name, field.data[2]))
        else:
            html = ["<select id=\"%s-day\" name=\"%s\">" % (field.id, field.name)]
            #Day drop down list
            for x in xrange(0, 32):
                if x == 0:
                    val = ""
                else:
                    val = str(x)

                html.append("<option value=\"%s\">%s</option>" % (val, val))
            html.append('</select>')

            #Month drop down list
            html.append("<select id=\"%s-month\" name=\"%s\">" % (field.id, field.name))
            for x in xrange(0, 13):
                if x == 0:
                    val = ""
                else:
                    val = str(x)

                html.append("<option value=\"%s\">%s</option>" % (val, val))
            html.append('</select>')

            html.append("<input id=\"%s-year\" name=\"%s\" type=\"text\" value=\"\">" % (field.id, field.name))

        return HTMLString(''.join(html))


class CustomDateField(Field):
    widget = CustomDateWidget()

    def _value(self):
        if self.data:
            return self.data
        else:
            return ['','','']

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist
        else:
            self.data = ['', '', '']
