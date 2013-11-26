import re
from flask_wtf import Form
from wtforms import TextField, SelectField, StringField, ValidationError, FormField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.validators import DataRequired, Length, Email, AnyOf, Regexp, Optional
from claimants_user_journey.forms.validators import DateOfBirthValidator


def blank_and_number_range_tuples(min, max_plus_one):
    lst = [('','')]
    lst += [(str(x), str(x)) for x in xrange(min, max_plus_one)]
    return lst

class DateForm(Form):
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(DateForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

    day = SelectField(choices=blank_and_number_range_tuples(1, 32),
                      validators=[AnyOf(values=[str(x) for x in xrange(1, 32)],
                                        message='Day is a required field')])
    month = SelectField(choices=blank_and_number_range_tuples(1, 13),
                        validators=[AnyOf(values=[str(x) for x in xrange(1, 13)],
                                          message='Month is a required field')])
    year = TextField(validators=[DataRequired('Please enter your Year of Birth'), ])

class ClaimantContactDetails(Form):
    forenames = TextField('First name(s)', validators=[DataRequired('Please enter your first name'), Length(max=60)])
    surname = TextField('Last name', validators=[DataRequired('Please enter your last name'), Length(max=60)])
    title = SelectField('Title',
                        choices=[
                            ('Mr', 'Mr'),
                            ('Mrs', 'Mrs'),
                            ('Miss', 'Miss'),
                            ('Ms', 'Ms'),
                            ('Dr', 'Dr'),
                            ('Other', 'Other'),
                            ('', '')
                        ],
                        default='',
                        validators=[AnyOf(values=[
                            'Mr',
                            'Mrs',
                            'Miss',
                            'Ms',
                            'Dr',
                            'Other'
                        ],
                        message='Please choose a title.')])
    other = TextField('Other', validators=[Length(max=15)])

    def validate_other(form, field):
        claimants_title = form._fields.get('title')
        if claimants_title.data == 'Other' and not field.data:
            raise ValidationError("Field is required if 'Other' is selected.")

    building_number = StringField('Building Number', validators=[DataRequired('Please enter your Building Number'), Length(max=30)])
    street = TextField('Street', validators=[DataRequired('Please enter your Street'), Length(max=30)])
    district = TextField('District', validators=[DataRequired('Please enter your District'), Length(max=30)])
    town_or_city = TextField('Town or City', validators=[DataRequired('Please enter your Town or City'), Length(max=30)])
    county = TextField('County', validators=[DataRequired('Please enter your County'), Length(max=30)])
    postcode = TextField('Post Code', validators=[DataRequired('Please enter your Post Code'), Length(max=10)])
    email = EmailField('Email Address', validators=[DataRequired('Please enter your Email Address'), Length(max=320), Email()])
    telephone_number = TelField('Telephone Number', validators=[DataRequired('Please enter your Telephone Number')])
    nino = TextField('National Insurance Number',
                     validators=[DataRequired('Please enter your National Insurance Number'),
                                 Regexp(regex=re.compile('^[a-zA-Z]{2}[0-9]{6}[a-zA-Z]{1}$'),
                                        message="National Insurance Number must be two letters followed by six digits and a further letter (e.g. 'AB123456C').")])
    date_of_birth = FormField(DateForm)
