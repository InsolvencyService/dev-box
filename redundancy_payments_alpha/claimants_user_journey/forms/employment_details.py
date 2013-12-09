import re
from datetime import date
from flask_wtf import Form
from wtforms import TextField, RadioField, Field
from wtforms.validators import Length, ValidationError
from wtforms.widgets import HTMLString
from claimants_user_journey.forms.validators import convert_string_to_date


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
            html = ['<label>Date Of Birth</label>']
            html.append("<select id=\"%s-day\" name=\"%s\">" % (field.id, field.name))
            #Day drop down list
            for x in xrange(0, 32):
                html.append("<option value=\"%i\">%i</option>" % (x, x))
            html.append('</select>')

            #Month drop down list
            html.append("<select id=\"%s-month\" name=\"%s\">" % (field.id, field.name))
            for x in xrange(0, 13):
                html.append("<option value=\"%i\">%i</option>" % (x, x))
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


class EmploymentDetails(Form):
    job_title = TextField('Job Title', validators=[Length(max=30)])
    _worker_type_options = [
        'Employed',
        'Labour-only Sub-contractor',
        'Agency Worker',
        'Fixed-term contracts worker',
        'Director or Shareholder',
        'Freelance worker',
        'Casual worker',
        'Home worker'
    ]
    type_of_worker = RadioField(
        'What type of worker are you?',
        choices = [
            ('employed', '<strong>Employed</strong></br>You are employed under a contract of employment'),
            ('labour-only sub-contractor', '<strong>Labour-only Sub-contractor</strong></br>You are self employed and pay tax and national insurance on that basis'),
            ('agency worker', '<strong>Agency Worker</strong></br>You are working for the client of an agency'),
            ('fixed term contract', '<strong>Fixed Term Contract</strong></br>Your contract is for a specific period of time i.e. it has an end date'),
            ('director or shareholder', '<strong>Director or Shareholder</strong></br>You are an office holder of the company'),
            ('freelance', '<strong>Freelance</strong></br>You work for yourself and the business is a client'),
            ('casual worker', '<strong>Casual Worker</strong></br>You work for the employer as and when required'),
            ('home worker', '<strong>Home Worker</strong></br>You work from home but attend an office for meetings')
        ],
    )
    start_date = CustomDateField(label="When did you start working for this employer?")
    end_date = CustomDateField(label="When did your employment end?")

    def validate_start_date(form, field):
        try:
            parsed_date = date(int(field.data[2]), int(field.data[1]), int(field.data[0]))
        except (SyntaxError, ValueError):
            raise ValidationError('Date must be in the format dd/mm/yyyy.')

        if parsed_date.year < 1900 or parsed_date >= date.today():
            raise ValidationError('Date must be greater than or equal to 1900 and not in the future.')

    def validate_end_date(form, field):
        try:
            parsed_date = date(int(field.data[2]), int(field.data[1]), int(field.data[0]))
        except (SyntaxError, ValueError):
            raise ValidationError('Date must be in the format dd/mm/yyyy.')

        if parsed_date.year < 1900 or parsed_date >= date.today():
            raise ValidationError('Date must be greater than or equal to 1900 and not in the future.')

        if not form.start_date.errors:
            parsed_start_date = date(int(form.start_date.data[2]), int(form.start_date.data[1]), int(form.start_date.data[0]))

            if parsed_start_date > parsed_date:
                raise ValidationError('The end date cannot be before the start date')
