import re
from flask_wtf import Form
from wtforms import TextField, RadioField
from wtforms.validators import Regexp, DataRequired, AnyOf
from validators import RequiredIfFieldHasValue, CustomDateFieldValidator
from custom_field_types import CurrencyField, CustomDateField


class WagesOwed(Form):

    owed = RadioField(
        'Are you owed any wages?',
        choices=[('Yes','Yes'),('No','No')],
        validators=[DataRequired('Please choose an option'),
                    AnyOf(values=['Yes', 'No'],
                          message='Please choose an option')])

    wage_owed_from = CustomDateField(
        label="From",
        validators=[
            CustomDateFieldValidator(),
            RequiredIfFieldHasValue(
                other_field_name='owed',
                other_field_value='Yes',
                message='')])

    wage_owed_to = CustomDateField(
        label="To",
        validators=[
            CustomDateFieldValidator(start_date_field_name='wage_owed_from'),
            RequiredIfFieldHasValue(
                other_field_name='owed',
                other_field_value='Yes',
                message='')])

    number_of_days_owed = TextField(
        'Number of days for which pay is owed',
        validators=[
            RequiredIfFieldHasValue(
                other_field_name='owed',
                other_field_value='Yes',
                message='Please enter number of days for which pay is owed'),
            Regexp(regex=re.compile(
                '^[0-9]?[0-9]$'),
                   message=("Number of days owed must be numeric "
                            "and a maximum of two digits."))])

    gross_amount_owed = CurrencyField(
        'Gross amount of pay owed',
        validators=[
            RequiredIfFieldHasValue(
                other_field_name='owed',
                other_field_value='Yes',
                message='Please enter the Gross amount of pay owed'),
            Regexp(regex=re.compile('^\d{0,8}(\.\d{0,2})?$'),
                   message='Gross amount owed must be numeric.')])
