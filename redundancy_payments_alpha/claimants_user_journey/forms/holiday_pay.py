import re
from flask_wtf import Form
from wtforms import TextField, RadioField
from wtforms.validators import DataRequired, AnyOf, Regexp, Length
from employment_details import FutureDateValidator
from claimants_user_journey.forms.validators import RequiredIfFieldHasValue


class HolidayPay(Form):
    holiday_owed = RadioField('Are you owed any holiday pay?',choices=[
                                         ('Yes', 'Yes'),
                                         ('No', 'No')
                                     ],
                                     validators=[DataRequired(), AnyOf(values=[
                                         'Yes',
                                         'No'
                                     ])])
    holiday_start_date = TextField('What was the start date of your holiday year?',
                                   validators=[
                                       RequiredIfFieldHasValue(other_field_name='holiday_owed', other_field_value='Yes',
                                                               message='Holiday Year Start Date has not been completed.'),
                                       FutureDateValidator(format_message="Start date must be in the format dd/mm/yyyy.",
                                                           future_message='Start date cannot be in the future.')])
    number_of_holiday_days_entitled = TextField('How many days holiday per year (including bank holidays) were you entitled to?',
                                                validators=[RequiredIfFieldHasValue(other_field_name='holiday_owed', other_field_value='Yes',
                                                               message='Holiday entitlement has not been completed.'),
                                                              Regexp(regex=re.compile('^[0-9]?[0-9]$'), message='Number of holiday days entitled must be numeric and a maximum of two digits.')])


    days_carried_over = TextField('If you were allowed to carry forward untaken holiday entitlement from your previous holiday year, how many days did you carry forward this year?',
                                                validators=[RequiredIfFieldHasValue(other_field_name='holiday_owed', other_field_value='Yes',
                                                               message='Days carried over has not been completed.'),
                                                             Regexp(regex=re.compile('^[0-9]?[0-9]$'), message='Number of holiday days carried over must be numeric and a maximum of two digits.')])
    days_taken = TextField('How many days have you taken this year (including bank holidays)?',
                                                validators=[RequiredIfFieldHasValue(other_field_name='holiday_owed', other_field_value='Yes',
                                                               message='Days taken mandatory fields has not been completed.'),
                                                             Regexp(regex=re.compile('^[0-9]?[0-9]$'), message='Number of holiday days taken must be numeric and a maximum of two digits.')])
    days_owed = TextField('How many days are you still owed (including bank holidays) up to your termination date?',
                                                validators=[RequiredIfFieldHasValue(other_field_name='holiday_owed', other_field_value='Yes',
                                                               message='Days owed mandatory fields has not been completed.'),
                                                             Regexp(regex=re.compile('^[0-9]?[0-9]$'), message='Number of holiday days owed must be numeric and a maximum of two digits.')])
    holiday_taken_from = TextField('From')
    holiday_taken_to = TextField('To')
    number_of_days_pay_owed = TextField('Number of days for which pay is owed',
                                       validators=[Regexp(regex=re.compile('^([0-9]?[0-9])?$'), message='Number of days pay owed must be numeric and a maximum of two digits.')])
