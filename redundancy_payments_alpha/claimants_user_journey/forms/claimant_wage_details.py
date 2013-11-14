import re
from flask_wtf import Form
from wtforms import TextField, SelectField, RadioField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, AnyOf, Regexp, NumberRange


class ClaimantWageDetails(Form):
    gross_rate_of_pay = TextField('Gross rate of pay (before Tax and NI)', validators=[DataRequired(), Regexp(regex=re.compile('^\d{0,8}(\.\d{0,2})?$'),
                                        message="Gross rate of pay must be a number e.g 100.25.")])

    frequency_of_payment = SelectField('How often do you get paid?',
                    choices=[
                        ('Week', 'Week')
                    ],
                    default='',
                    validators=[AnyOf(values=[
                        'Week'
                    ])])

    number_of_hours_worked = TextField('Number of hours you normally work', validators=[DataRequired(), Regexp(regex=re.compile('^\d{0,2}(\.\d{0,2})?$'),
                                        message="Number of hours you normally work must be a number e.g 40.25.")])

    frequency_of_work = SelectField('every',
                    choices=[
                        ('Hour', 'Hour'),
                        ('Day', 'Day'),
                        ('Week', 'Week'),
                        ('Month', 'Month'),
                        ('Year', 'Year'),
                        ('', '')
                    ],
                    default='',
                    validators=[DataRequired(), AnyOf(values=[
                        'Hour',
                        'Day',
                        'Week',
                        'Month',
                        'Year'
                    ])])

    bonus_or_commission = RadioField('Did your pay include any bonus or commission ?',
                                     choices=[
                                         ('Yes', 'Yes'),
                                         ('No', 'No')
                                     ],
                                     validators=[DataRequired(), AnyOf(values=[
                                         'Yes',
                                         'No'
                                     ])])
    overtime = RadioField('Did you work overtime as a part of your contract ?',
                                     choices=[
                                         ('Yes', 'Yes'),
                                         ('No', 'No')
                                     ],
                                     validators=[DataRequired(), AnyOf(values=[
                                         'Yes',
                                         'No'
                                     ])])
    normal_days_of_work = IntegerField('How many days you normally work each week', validators=[DataRequired(), NumberRange(0,7)])

