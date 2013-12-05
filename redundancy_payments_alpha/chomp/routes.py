from flask import Flask, redirect, request, Response
from werkzeug.exceptions import NotImplemented

from birmingham_cabinet import api as brum_cab
from chomp import payloads

app = Flask(__name__)

@app.route("/chomp/next", methods=["GET"])
def next():
    claim_id = brum_cab.get_next_claim_not_processed_by_chomp()
    if claim_id is None:
        return "", 204
    else:
        next_url = "/chomp/{claim_id}/".format(**locals())
        client = request.remote_addr
        app.logger.info("Redirecting {client} to {next_url}".format(
            **locals()))
        return redirect(next_url, 303)


@app.route("/chomp/<id_>/", methods=["GET", "POST"])
def claim(id_):
    claim = brum_cab.get_claim


@app.route("/chomp/<id_>/state", methods=["GET"])
def state(id_):
    return brum_cab.chomp_state_of_claim(id_)


@app.route("/chomp/<id_>/state", methods=["POST"])
def set_state(id_):
    state = request.data
    if state == "Done":
        brum_cab.chomp_claim_done(id_)
        return state, 200


@app.route("/chomp/<id_>/acceptdoc", methods=["GET"])
def acceptdoc(id_):
    dms_id = payloads.dms_id()
    acceptdoc = payloads.acceptdoc(dms_id)
    app.logger.info("Generated an acceptdoc for {id_}".format(**locals()))
    return Response(acceptdoc, mimetype="text/xml")


@app.route("/chomp/<id_>/rp1", methods=["GET"])
def rp1(id_):
    rp1_document = payloads.claimant_information({})
    app.logger.info("Generated rp1 for {id_}".format(**locals()))
    return Response(rp1_document, mimetype="text/xml")


@app.route("/chomp/<id_>/rp14", methods=["GET"])
def rp14(id_):
    rp14_document = payloads.rp14({})
    app.logger.info("Generated rp14 for {id_}".format(**locals()))
    return Response(rp14_document, mimetype="text/xml")


@app.route("/chomp/<id_>/rp14a", methods=["GET"])
def rp14a(id_):
    rp14a_document = payloads.rp14a({})
    app.logger.info("Generated rp14a for {id_}".format(**locals()))
    return Response(rp14a_document, mimetype="text/xml")
