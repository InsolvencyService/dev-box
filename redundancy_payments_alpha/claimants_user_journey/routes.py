from flask import Flask, render_template
from forms.claimant_contact_details import ClaimantContactDetails

app = Flask(__name__)
app.secret_key = 'something_secure_and_secret'
app.debug = True

@app.route('/_status', methods=['GET'])
def status():
    return "everything is ok"


@app.route('/claimant-contact-details', methods=['GET', 'POST'])
def claimant_contact_details():
    form = ClaimantContactDetails()
    if form.validate_on_submit():
        return 'winner!'
    return render_template('user_details.html', form=form)
