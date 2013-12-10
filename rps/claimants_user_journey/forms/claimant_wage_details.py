import re
from flask_wtf import Form
from wtforms import StringField, SelectField, RadioField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, AnyOf, Regexp, Length
from custom_field_types import CurrencyField


class ClaimantWageDetails(Form):
    gross_rate_of_pay = CurrencyField(
        'Gross rate of pay per week (before Tax and NI, excluding overtime)',
         validators=[DataRequired('Please enter your gross rate of pay per week'),
              Regexp(regex=re.compile(
                  '^\d{0,8}(\.\d{0,2})?$'),
                  message="Gross rate of pay must be a number e.g 100.25.")])

    day_of_payment = SelectField('What day of the week did you get paid?',
                                 choices=[
                                     ('Monday', 'Monday'),
                                     ('Tuesday', 'Tuesday'),
                                     ('Wednesday', 'Wednesday'),
                                     ('Thursday', 'Thursday'),
                                     ('Friday', 'Friday'),
                                     ('Saturday', 'Saturday'),
                                     ('Sunday', 'Sunday'),
                                 ],
                                 default='Saturday')

    number_of_hours_worked = StringField(
        'Number of hours you normally worked per week',
        validators=[DataRequired('Please enter the number of hours you '
                                 'normally worked per week'),
                    Regexp(regex=re.compile('^\d{0,2}(\.\d{0,2})?$'),
                           message="Number of hours you normally worked per week must be "
                                   "a number "
                                   "e.g 40.25.")])

    overtime = RadioField('Did you work overtime as a part of your contract ?',
                          choices=[
                              ('Yes', 'Yes'),
                              ('No', 'No')
                          ],
                          validators=[DataRequired('Please choose an option'),
                                      AnyOf(values=[
                                          'Yes',
                                          'No'
                                      ])])

    hours_of_overtime = StringField('How many hours overtime did you normally work?')

    def validate_hours_of_overtime(form, field):
        overtime_worked = form._fields.get('overtime')
        if overtime_worked.data == 'Yes' and not field.data:
           raise ValidationError("Please enter the number of hours overtime you normally work")

    frequency_of_overtime = SelectField('every',
                                        choices=[
                                            ('Week', 'Week'),
                                            ('Month', 'Month'),
                                            ('Year', 'Year'),
                                            ('', '')
                                        ],
                                        default='',
                                        validators=[AnyOf(values=[
                                            'Week',
                                            'Month',
                                            'Year',
                                            ''
                                        ])])

    normal_days_of_work = SelectField(
        'How many days did you normally work each week?',
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('', '')
        ],
        default='',
        validators=[AnyOf(values=[
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7'
        ],
                          message='Please choose how many days you normally '
                                  'work each week')])

    bonus_or_commission = RadioField(
        'Did your pay include any bonus or commission ?',
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired('Please choose an option'), AnyOf(values=[
            'Yes',
            'No'
        ])])

    bonus_details = TextAreaField(
        'Give details of the amount and type of bonus '
        'or commission earned, and when it was paid')

