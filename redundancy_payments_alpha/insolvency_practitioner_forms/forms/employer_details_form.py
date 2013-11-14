import time
from flask_wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, AnyOf
from validators.validators import parses_to_date

class EmployerDetailsForm(Form):
    company_name  = TextField('Name of Employer', validators=[DataRequired(), Length(max=60)])
    company_number  = TextField('Company Registration Number (if known)', validators=[Length(max=10)])
    nature_of_business  = TextField('Nature of Business', validators=[DataRequired(), Length(max=60)])
    date_of_insolvency  = TextField('Date of Insolvency', validators=[DataRequired(), parses_to_date])
    type_of_insolvency  = SelectField(
        'Type of Insolvency',
        default='',
        choices=[
            ('',''),
            ('creditors_voluntary_liquidation', 'Creditors Voluntary Liquidation (CVL)'),
            ('compulsory_liquidation', 'Compulsory Liquidation (WUO)'),
            ('company_voluntary_arrangement', 'Company Voluntary Arrangement (CVA)'),
            ('administration', 'Administration'),
            ('administrative_receivership', 'Administrative Receivership'),
            ('bankruptcy', 'Bankruptcy'),
            ('individual_voluntary_arrangements', 'Individual Voluntary Arrangements (IVA)'),
            ('members_voluntary_liquidation', 'Members Voluntary Liquidation (MVL)'),
            ('dro', 'DRO'),
            ('employer_deceased_judicial_factor', 'Employer Deceased - Judicial Factor'),
            ('employer_deceased_estate_insolvent', 'Employer Deceased - Estate Insolvent'),
            ('individual_voluntary_arrangements', 'Individual Voluntary Arrangements (IVA)'),
            ('sequestrian', 'Sequestrian')
        ],
        validators=[AnyOf([
            'creditors_voluntary_liquidation',
            'compulsory_liquidation',
            'company_voluntary_arrangement',
            'administration',
            'administrative_receivership',
            'bankruptcy',
            'individual_voluntary_arrangements',
            'members_voluntary_liquidation',
            'dro',
            'employer_deceased_judicial_factor',
            'employer_deceased_estate_insolvent',
            'individual_voluntary_arrangements',
            'sequestrian'
        ], message="Please choose a type of insolvency.")]
    )
    insolvency_practitioner_name  = TextField('Insolvency Practitioner Name', validators=[DataRequired(), Length(max=30)])
    insolvency_practitioner_registration  = TextField('Insolvency Practitioner Registration', validators=[DataRequired(), Length(max=15)])
    insolvency_practitioner_firm  = TextField('Insolvency Practitioner Firm', validators=[DataRequired(), Length(max=30)])
    address_line_1  = TextField('Address Line 1', validators=[DataRequired(), Length(max=7)])
    address_line_2  = TextField('Address Line 2', validators=[DataRequired(), Length(max=22)])
    address_line_3  = TextField('Address Line 3', validators=[Length(max=30)])
    town_or_city  = TextField('Town or City', validators=[DataRequired(), Length(max=30)])
    postcode  = TextField('Postcode', validators=[DataRequired(), Length(max=8)])
    country  = TextField('Country', validators=[DataRequired(), Length(max=30)])
    email_address  = TextField('Email Address', validators=[DataRequired(), Length(max=60)])
    telephone_number  = TextField('Telephone Number', validators=[DataRequired(), Length(max=40)])

    def validate_company_number(self, field):
        if field.data:
            try:
                int(field.data)
            except ValueError as e:
                raise ValueError('Company number must be a number.')

    def validate_insolvency_practitioner_registration(self, field):
        if field.data:
            try:
                int(field.data)
            except ValueError as e:
                raise ValueError('Insolvency Practitioner Registration must be a number.')

