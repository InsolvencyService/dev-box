import re
from flask_wtf import Form
from wtforms import TextField, RadioField
from wtforms.validators import Regexp
from validators import RequiredIfFieldHasValue


class WagesOwed(Form):

    owed = RadioField('Are you owed any wages?',  choices=[('No','No'),('Yes','Yes')])

    wage_owed_from = TextField('From',
                           validators=[RequiredIfFieldHasValue(other_field_name='owed', other_field_value='Yes'),
                                       Regexp(regex=re.compile('^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$'),
                                        message='Date must be in the format dd/mm/yyyy.')])
    wage_owed_to = TextField('To',
                           validators=[RequiredIfFieldHasValue(other_field_name='owed', other_field_value='Yes'),
                                       Regexp(regex=re.compile('^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$'),
                                        message='Date must be in the format dd/mm/yyyy.')])

    number_of_days_owed = TextField('Number of days for which pay is owed',
                           validators=[RequiredIfFieldHasValue(other_field_name='owed', other_field_value='Yes'),
                                       Regexp(regex=re.compile('^[0-9]?[0-9]$'), message='Number of days owed must be numeric.')])

    gross_amount_owed = TextField('Gross amount of pay owed',
                           validators=[RequiredIfFieldHasValue(other_field_name='owed', other_field_value='Yes'),
                                       Regexp(regex=re.compile('^\d{0,8}(\.\d{0,2})?$'),
                                         message='Gross amount owed must be numeric.')])

    failed_payment_from = TextField('From',
                           validators=[Regexp(regex=re.compile('^([0-9]{2}[/][0-9]{2}[/][0-9]{4})?$'),
                                        message='Date must be in the format dd/mm/yyyy.')])

    failed_payment_to = TextField('To',
                           validators=[Regexp(regex=re.compile('^([0-9]{2}[/][0-9]{2}[/][0-9]{4})?$'),
                                        message='Date must be in the format dd/mm/yyyy.')])


    net_amount = TextField('Net Amount of bounced cheque or failed payment',
                           validators=[Regexp(regex=re.compile('^(\d{0,8}(\.\d{0,2})?$)?$'),
                                         message='Net amount must be numeric.')])