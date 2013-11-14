import re

from flask_wtf import Form
from wtforms import TextField, SelectField, DecimalField, DateField
from wtforms.validators import ValidationError, Length, AnyOf, DataRequired, InputRequired

from validators.validators import parses_to_date


class EmployeeDetailsForm(Form):
    employer_name = TextField('Employer Name', validators=[Length(max=60), DataRequired()])
    employee_title = SelectField(
        label='Title',
        default = '',
        choices = [
            ('Mr', 'Mr'),
            ('Mrs', 'Mrs'),
            ('Miss', 'Miss'),
            ('Ms', 'Ms'),
            ('Other', 'Other'),
            ('', '')
        ],
        validators=[AnyOf(['Mr', 'Mrs', 'Miss', 'Ms', 'Other'])]
    )
    employee_title_other = TextField('Title if other', validators=[Length(max=15)])

    def validate_employee_title_other(self, field):
        if not field.data and self.employee_title.data == 'Other':
            raise ValidationError('A title must be provided if other is selected.')

    employee_forenames = TextField('Forenames', validators=[Length(max=40), DataRequired()])
    employee_surname = TextField('Surname', validators=[Length(max=60), DataRequired()])
    employee_national_insurance_class = TextField('National insurance class')

    def validate_employee_national_insurance_class(self, field):
        if field.data and not re.match("^[A-Za-z]{1}$", field.data):
            raise ValidationError('National insurance class must be a single letter.')

    employee_national_insurance_number = TextField('National insurance number', validators=[DataRequired()])

    def validate_employee_national_insurance_number(self, field):
        if field.data and not re.match('^[A-Za-z]{2}[0-9]{6}[A-Za-z]{0,1}$', field.data):
            raise ValidationError('National insurance number should be two letters followed by six numbers and an optional letter')

    employee_date_of_birth = DateField('Date of birth', format='%d/%m/%Y', validators=[InputRequired()])
    employee_start_date = DateField('Start date', format='%d/%m/%Y', validators=[InputRequired()])
    employee_date_of_notice = DateField('Date notice was given', format='%d/%m/%Y', validators=[InputRequired()])
    employee_end_date = DateField('End date', format='%d/%m/%Y', validators=[InputRequired()])
    employee_basic_weekly_pay = DecimalField('Basic weekly pay', validators=[DataRequired()])
    employee_weekly_pay_day = SelectField(
        'If paid weekly on which day of week?',
        default='',
        choices = [
            ('', ''),
            ('sunday', 'Sunday'),
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday')
        ]
    )
    employee_owed_wages_from = DateField('Employee owed wages from', format='%d/%m/%Y', validators=[InputRequired()])
    employee_owed_wages_to = DateField('Employee owed wages to', format='%d/%m/%Y', validators=[InputRequired()])
    employee_owed_wages_in_arrears = TextField('Owed wages in arrears', validators=[DataRequired()])
    employee_owed_wages_in_arrears_type = SelectField(
        'Arrears of pay type',
        default = '',
        choices = [
            ('',''),
            ('attatchment_of_earnings','attachment of earnings'),
            ('wages','wages'),
            ('overtime','overtime'),
            ('unpaid_checque','unpaid cheque'),
            ('commission','commission')
        ]
    )
    employee_holiday_year_start_date = DateField('Holiday year start date', format='%d/%m/%Y', validators=[InputRequired()])
    employee_holiday_owed = DecimalField('Number of days holiday owed', validators=[DataRequired()])
    employee_unpaid_holiday_from = DateField('Unpaid holiday from', format='%d/%m/%Y', validators=[InputRequired()])
    employee_unpaid_holiday_to = DateField('Unpaid holiday to', format='%d/%m/%Y', validators=[InputRequired()])
