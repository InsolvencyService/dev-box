from flask_wtf import Form
from wtforms import DecimalField, SelectField
from wtforms.validators import DataRequired

class WageAmount(Form):
    gross_pay = DecimalField('How much did you earn for each period before paying any tax or deductions? (ie your gross income)', validators=[DataRequired()])
    period = SelectField(
        'How often were you paid?', 
        choices=[('week','Weekly'), ('year', 'Yearly')],
        validators=[DataRequired()]
    ) 

