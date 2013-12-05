from flask_wtf import Form
from wtforms import TextField, SelectField, RadioField, FormField
from wtforms.validators import DataRequired, Length, AnyOf, ValidationError
from claimants_user_journey.forms.custom_field_types import DateForm
from claimants_user_journey.forms.validators import FutureDateValidator


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
    start_date = FormField(DateForm, label="When did you start working for this employer?")
    end_date = FormField(DateForm, label="When did your employment end?")

    def validate(self):
        if not super(EmploymentDetails, self).validate():
            return False

        if self.start_date > self.end_date:
            errors = []
            errors.append("The end date cannot be before the start date")

            self._errors = {'whole_form' : errors}
            return False

        return True
