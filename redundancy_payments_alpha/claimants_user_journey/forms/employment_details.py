from flask_wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, Length, AnyOf
from claimants_user_journey.forms.validators import FutureDateValidator


class EmploymentDetails(Form):
    job_title = TextField('Job Title', validators=[Length(max=30)])
    category_of_worker = SelectField('Category of Worker',
                                     choices=[
                                         ('Employed', 'Employed'),
                                         ('Labour-only Sub-contractor', 'Labour-only Sub-contractor'),
                                         ('Agency Worker', 'Agency Worker'),
									     ('Fixed-term contracts worker', 'Fixed-term contracts worker'),
                                         ('Director or Shareholder', 'Director or Shareholder'),
                                         ('Freelance worker', 'Freelance worker'),
                                         ('Casual worker', 'Casual worker'),
                                         ('Home worker', 'Home worker'),
                                         ('', '')
                                     ],
                                     default='',
                                     validators=[AnyOf(values=[
                                         'Employed',
                                         'Labour-only Sub-contractor',
                                         'Agency Worker',
                                         'Fixed-term contracts work',
                                         'Director or Shareholder',
                                         'Freelance worker',
                                         'Casual worker',
                                         'Home worker',
                                     ],
                                     message='Please choose a Category of Worker')])
    start_date = TextField('When did you start working for this employer?',
                           validators=[DataRequired('Please enter the date you started working for this employer'),
                                       FutureDateValidator(format_message="Start date must be in the format dd/mm/yyyy.",
                                                           future_message='Start date cannot be in the future.')])
    end_date = TextField('When did your employment end?',
                           validators=[DataRequired('Please enter the date you stopped working for this employer'),
                                       FutureDateValidator(format_message="End date must be in the format dd/mm/yyyy.",
                                                           future_message='End date cannot be in the future.')])
