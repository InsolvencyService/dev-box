from flask import Flask, redirect
from werkzeug.exceptions import NotImplemented

from birmingham_cabinet import api as brum_cab

app = Flask(__name__)

@app.route("/chomp/next", methods=["POST"])
def next():
    claim_id = brum_cab.get_next_claim_not_processed_by_chomp()
    return redirect("/chomp/{claim_id}/".format(**locals()), 303)

@app.route("/chomp/<id_>/", methods=["GET", "POST"])
def claim(id_):
    raise NotImplemented()

@app.route("/chomp/<id_>/status", methods=["GET"])
def status(id_):
    return brum_cab.get_chomp_status_of_claim(id_)

@app.route("/chomp/<id_>/acceptdoc", methods=["GET"])
def acceptdoc(id_):
    raise NotImplemented()

@app.route("/chomp/<id_>/rp1", methods=["GET"])
def rp1(id_):
    raise NotImplemented()

@app.route("/chomp/<id_>/rp14a", methods=["GET"])
def rp14a(id_):
    raise NotImplemented()
