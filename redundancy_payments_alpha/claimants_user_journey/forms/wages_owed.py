import re
from flask_wtf import Form
from wtforms import TextField, SelectField, DecimalField, IntegerField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, AnyOf, Regexp


class WagesOwed(Form):

    owed = RadioField('Are you owed any wages?',  choices=[('N','No'),('Y','Yes')])

    wage_owed_from = TextField('From',
                           validators=[DataRequired(),
                                       Regexp(regex=re.compile('^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$'),
                                        message='Date must be in the format dd/mm/yyyy.')])
    wage_owed_to = TextField('To',
                           validators=[DataRequired(),
                                       Regexp(regex=re.compile('^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$'),
                                        message='Date must be in the format dd/mm/yyyy.')])

    number_of_days_owed = TextField('Number of days for which pay is owed',
                           validators=[DataRequired(),
                                       Regexp(regex=re.compile('^[0-9]?[0-9]$'), message='Number of days owed must be numeric.')])

    gross_amount_owed = TextField('Gross amount of pay owed',
                           validators=[DataRequired(),
                                       Regexp(regex=re.compile('^[0-9]+(\.[0-9][0-9]?)$'),
                                         message='Gross amount owed must be numeric.')])
