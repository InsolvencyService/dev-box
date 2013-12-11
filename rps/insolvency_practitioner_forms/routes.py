from pprint import pprint

from flask import Flask, url_for, request, render_template, session, g, send_file
from werkzeug.utils import redirect

from forms.employer_details_form import EmployerDetailsForm
from forms.employee_details_form import EmployeeDetailsForm
from birmingham_cabinet.api import add_rp14a_form
from notification_service import api as notification_api
from claim_service import api as claims_api
from filters.filters import setup_filters

app = Flask(__name__)
app.secret_key = 'i_am_a_secret'

setup_filters(app)


def get_storage_service():
    """This is a separate method so it can be mocked
    """
    return add_rp14a_form

@app.before_request
def before_request():
    g.storage_service = get_storage_service()

@app.route('/create-insolvency-case/employer-details/', methods=['GET', 'POST'])
def employer_details():
    form = EmployerDetailsForm()
    if form.validate_on_submit():
        return redirect(url_for('case_created'))
    else:
        return render_template('insolvency_case_form.html', form=form)


@app.route('/create-insolvency-case/case-created/', methods=['GET'])
def case_created():
    return render_template('case_submitted_ok.html')

@app.route('/create-employee-record/employee-details/', methods=['GET','POST'])
def employee_details():
    form = EmployeeDetailsForm()
    if form.validate_on_submit():
        pprint(form["employee_date_of_birth"])
        # this method calls into the datalayer
        g.storage_service(form.data)
        return redirect(url_for('employee_added'))
    return render_template('employee_details_form.html', form=form)


@app.route('/create-employee-record/employee-added/')
def employee_added():
    return render_template('employee_submitted_ok.html')

@app.route('/_tasks/send-notifications/', methods=['POST'])
def send_notifications():
    claims = claims_api.claims_submitted_in_last_24_hours()
    summary_message = '%d claims in the last 24 hours' % len(claims)
    notification_api.send_email('fakeip@not-an-address.com', 'Fake Subject',
                                'Mr Phony', summary_message)
    return 'ok'

@app.route('/robots.txt')
def robots_txt():
    return send_file('static/robots.txt')


@app.route('/ip-dashboard/claims/')
def claim_dashboard():
    return render_template('claim_dashboard.html', claim_summaries=claims_api.summarise_claims())

if __name__ == '__main__':
    app.run()

