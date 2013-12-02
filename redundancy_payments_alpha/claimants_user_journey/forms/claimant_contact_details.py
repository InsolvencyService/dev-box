import collections
import re
from flask_wtf import Form
from wtforms import TextField, SelectField, StringField, ValidationError, FormField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.validators import DataRequired, Length, Email, AnyOf, Regexp, Optional
from claimants_user_journey.forms.custom_field_types import DateForm
from claimants_user_journey.forms.validators import DateOfBirthValidator


class ClaimantContactDetails(Form):
    @property
    def errors(self):
        errs = super(ClaimantContactDetails, self).errors

        items = []
        for key, value in errs.items():
            key
            if isinstance(value, collections.MutableMapping):
                items.extend(value.items())
            else:
                items.append((key, value))
        return dict(items)

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