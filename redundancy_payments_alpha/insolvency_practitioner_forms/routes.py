from pprint import pprint

from flask import Flask, url_for, request, render_template, session, g
from werkzeug.utils import redirect

from forms.employer_details_form import EmployerDetailsForm
from forms.employee_details_form import EmployeeDetailsForm
from birmingham_cabinet.api import add_rp14a_form

app = Flask(__name__)
app.secret_key = 'i_am_a_secret'
app.debug = True

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
    return 'ok'

@app.route('/create-employee-record/employee-details/', methods=['GET','POST'])
def employee_details():
    form = EmployeeDetailsForm()
    if form.validate_on_submit():
        pprint(form["employee_date_of_birth"])
        # this method calls into the datalayer
        g.storage_service(form.data)
        return redirect(url_for('employee_added'))
    print form.errors
    return render_template('employee_details_form.html', form=form)


@app.route('/create-employee-record/employee-added/')
def employee_added():
    return 'ok'


if __name__ == '__main__':
    app.run()

