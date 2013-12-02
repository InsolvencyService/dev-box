from flask_wtf import Form
from wtforms import TextField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, AnyOf
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
            ('director or shareholder', '<strong>Director or Shareholder</strong></br>You are an office holder of the company'),
            ('freelance', '<strong>Freelance</strong></br>You work for yourself and the business is a client'),
            ('casual worker', '<strong>Casual Worker</strong></br>You work for the employer as and when required'),
            ('home worker', '<strong>Home Worker</strong></br>You work from home but attend an office for meetings')
        ],
    )
    start_date = TextField('When did you start working for this employer?',
                           validators=[DataRequired('Please enter the date you started working for this employer'),
                                       FutureDateValidator(format_message="Start date must be in the format dd/mm/yyyy.",
                                                           future_message='Start date cannot be in the future.')])
    end_date = TextField('When did your employment end?',
                           validators=[DataRequired('Please enter the date you stopped working for this employer'),
                                       FutureDateValidator(format_message="End date must be in the format dd/mm/yyyy.",
                                                           future_message='End date cannot be in the future.')])

