import json

from flask import Flask, render_template, url_for, session, request, abort
from werkzeug.utils import redirect

from birmingham_cabinet.api import employee_via_nino
from forms.claimant_contact_details import ClaimantContactDetails
from forms.claimant_wage_details import ClaimantWageDetails
from forms.employment_details import EmploymentDetails
from forms.holiday_pay import HolidayPay
from forms.wages_owed import WagesOwed

app = Flask(__name__)
app.secret_key = 'something_secure_and_secret'
app.debug = True


def nav_links():
    links = [
        ('Start', url_for('start')),
        ('Personal Details', url_for('personal_details')),
        ('Employment Details', url_for('employment_details')),
        ('Wage Details', url_for('wage_details')),
        ('Holiday Pay', url_for('holiday_pay')),
        ('Wages Owed', url_for('wages_owed')),
        ('Summary', url_for('summary')),
    ]
    return links


@app.route('/_status', methods=['GET'])
def status():
    return "everything is ok"


@app.route('/claim-redundancy-payment/', methods=['GET'])
@app.route('/', methods=['GET'])
def claim_redundancy_payment():
    return redirect(url_for('start'))


@app.route('/claim-redundancy-payment/start/')
def start():
    return render_template('start.html', nav_links=nav_links())


@app.route('/claim-redundancy-payment/personal-details/', methods=['GET', 'POST'])
def personal_details():
    existing_form = session.get('user_details')

    if existing_form:
        form = ClaimantContactDetails(**existing_form)
    else:
        form = ClaimantContactDetails()

    if form.validate_on_submit():
        session['user_details'] = form.data
        return redirect(url_for('employee_records', nino=form.nino.data))
    return render_template('user_details.html', form=form, nav_links=nav_links())

@app.route('/claim-redundancy-payment/employee-records/', methods=['GET'])
def employee_records():
    try:
        employee_record = employee_via_nino(request.args['nino'])
        return render_template('employee_record.html', employee_record=employee_record)
    except KeyError:
        return render_template('employee_record.html')


@app.route('/claim-redundancy-payment/employment-details/', methods=['GET', 'POST'])
def employment_details():
    existing_form = session.get('employment_details')

    if existing_form:
        form = EmploymentDetails(**existing_form)
    else:
        form = EmploymentDetails()

    if form.validate_on_submit():
        session['employment_details'] = form.data
        return redirect(url_for('wage_details'))

    return render_template('employment_details.html', form=form, nav_links=nav_links())


@app.route('/claim-redundancy-payment/wages-owed-details/', methods=['GET', 'POST'])
def wages_owed():
    existing_form = session.get('wages_owed')

    if existing_form:
        form = WagesOwed(**existing_form)
    else:
        form = WagesOwed()

    if form.validate_on_submit():
        session['wages_owed'] = form.data
        return redirect(url_for('summary'))

    return render_template('wages_owed.html', form=form, nav_links=nav_links())


@app.route('/claim-redundancy-payment/wage-details/', methods=['GET', 'POST'])
def wage_details():
    existing_form = session.get('wage_details')

    if existing_form:
        form = ClaimantWageDetails(**existing_form)
    else:
        form = ClaimantWageDetails()

    if form.validate_on_submit():
        session['wage_details'] = form.data
        return redirect(url_for('holiday_pay'))

    return render_template('wage_details.html', form=form, nav_links=nav_links())

@app.route('/claim-redundancy-payment/holiday-pay/', methods=['GET', 'POST'])
def holiday_pay():
    existing_form = session.get('holiday_pay')

    if existing_form:
        form = HolidayPay(**existing_form)
    else:
        form = HolidayPay()

    if form.validate_on_submit():
        session['holiday_pay'] = form.data
        return redirect(url_for('wages_owed'))

    return render_template('holiday_pay.html', form=form, nav_links=nav_links())


@app.route('/claim-redundancy-payment/summary/', methods=['GET'])
def summary():
    summary = {
        'claimant_details': session.get('user_details'),
        'employment_details': session.get('employment_details'),
        'wages_owed': session.get('wages_owed')
    }
    summary_json = json.dumps(summary, indent=4)
    return render_template('summary.html', summary=summary_json, nav_links=nav_links())
