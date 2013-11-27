import json

from flask import Flask, render_template, url_for, session, request, send_file
from werkzeug.utils import redirect

import claim_service.api as claim_service
from claimants_user_journey.view_filters.filters import setup_filters
from forms.claimant_contact_details import ClaimantContactDetails
from forms.claimant_wage_details import ClaimantWageDetails
from forms.employment_details import EmploymentDetails
from forms.holiday_pay import HolidayPay
from forms.wages_owed import WagesOwed

app = Flask(__name__)
app.secret_key = 'something_secure_and_secret'
setup_filters(app)


def nav_links():
    links = [
        ('Employment Details', url_for('employment_details')),
        ('Wage Details', url_for('wage_details')),
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
    return render_template('start.html', hide_nav=True, inner_id='start-page')


@app.route('/claim-redundancy-payment/personal-details/', methods=['GET', 'POST'])
def personal_details():
    existing_form = session.get('user_details')

    if existing_form:
        form = ClaimantContactDetails(**existing_form)
    else:
        form = ClaimantContactDetails()

    if form.validate_on_submit():
        session['user_details'] = form.data
        session['user_details']['nino'] = form.data['nino'].upper()

        claim_id = claim_service.create_claim_2(session['user_details'])
        if claim_id:
            session['claim_id'] = claim_id
            return redirect(url_for('employment_details'))
        else:
            return redirect(url_for('call_your_ip'))
    return render_template('user_details.html', form=form, hide_nav=True, inner_id='personal-details')


@app.route('/claim-redundancy-payment/call-your-ip/', methods=['GET'])
def call_your_ip():
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
        claim_id = session.get('claim_id')
        if claim_id:
            claim_service.add_details_to_claim(claim_id, form.data)
            discrepancies = claim_service.find_discrepancies(claim_id)
            if len(discrepancies):
                return redirect(url_for('arrears_pay_discrepancies'))
        return redirect(url_for('summary'))

    return render_template('wages_owed.html', form=form, nav_links=nav_links(),
            discrepancies={})

@app.route('/claim-redundancy-payment/wages-owed-details/discrepancies/', methods=['GET','POST'])
def arrears_pay_discrepancies():
    existing_form = session.get('wages_owed')

    if existing_form:
        form = WagesOwed(**existing_form)
    else:
        form = WagesOwed()

    print request.method
    
    claim_id = session.get('claim_id')
    if form.validate_on_submit():
        session['wages_owed'] = form.data
        if claim_id:
            claim_service.add_details_to_claim(claim_id, form.data)
        return redirect(url_for('summary'))
    elif request.method == 'POST' and not form.validate():
        session['wages_owed'] = form.data
        return redirect(url_for('wages_owed', data=form.data), code=307)

    discrepancies = {}
    if claim_id:
        discrepancies = claim_service.find_discrepancies(claim_id)
    return render_template('wages_owed.html', form=form, nav_links=nav_links(), discrepancies=discrepancies)

 
@app.route('/claim-redundancy-payment/wage-details/', methods=['GET', 'POST'])
def wage_details():
    existing_form = session.get('wage_details')

    if existing_form:
        form = ClaimantWageDetails(**existing_form)
    else:
        form = ClaimantWageDetails()

    if form.validate_on_submit():
        session['wage_details'] = form.data
        claim_id = session.get('claim_id')
        if claim_id:
            claim_service.add_details_to_claim(claim_id, form.data)
            discrepancies = claim_service.find_discrepancies(claim_id)
            if len(discrepancies):
                return redirect(url_for('wage_details_discrepancies'))
        return redirect(url_for('wages_owed'))

    return render_template('wage_details.html', form=form, nav_links=nav_links(),
            discrepancies={})


@app.route('/claim-redundancy-payment/wage-details/discrepancies/', methods=['GET','POST'])
def wage_details_discrepancies():
    existing_form = session.get('wage_details')
    if existing_form:
        form = ClaimantWageDetails(**existing_form)
    else:
        form = ClaimantWageDetails()

    claim_id = session.get('claim_id')

    if form.validate_on_submit():
        session['wage_details'] = form.data
        if claim_id:
            claim_service.add_details_to_claim(claim_id, form.data)
        return redirect(url_for('wages_owed'))
    elif request.method == 'POST' and not form.validate():
        session['wage_details'] = form.data
        return redirect(url_for('wage_details', data=form.data), code=307)

    discrepancies = {}
    if claim_id:
        discrepancies = claim_service.find_discrepancies(claim_id)
    return render_template('wage_details.html', form=form, nav_links=nav_links(),
        discrepancies=discrepancies)


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
    discrepancies = {}

    claim_id = session.get('claim_id')
    if claim_id:
        discrepancies = claim_service.find_discrepancies(claim_id)

    return render_template('summary.html', discrepancies=discrepancies, nav_links=nav_links())

@app.route('/robots.txt')
def robots_txt():
    return send_file('static/robots.txt')
