from flask import Flask
from flask import request
from flask import render_template
import requests

import json
import logging
import os

app = Flask(__name__)


MAILCHIMP_API_KEY = os.environ["MAILCHIMP_API_KEY"]
MAILCHIMP_LIST_ID = os.environ["MAILCHIMP_LIST_ID"]

MAILCHIMP_LIST_URL = "https://us16.api.mailchimp.com/3.0/lists/" + MAILCHIMP_LIST_ID


def get_member_by_uniqid(uniqid):
    query = {
        "unique_email_id": uniqid
    }

    r = requests.get(MAILCHIMP_LIST_URL + "/members",
            auth=("rsvp", MAILCHIMP_API_KEY),
            params=query)
    r.raise_for_status()

    j = r.json()
    return j["members"][0]["id"]


def update_rsvp(member_id, rsvp):
    payload = {
        "merge_fields": {
            "RSVPSTATUS": rsvp
        }
    }

    r = requests.patch(MAILCHIMP_LIST_URL + "/members/" + member_id,
            auth=("rsvp", MAILCHIMP_API_KEY),
            json=payload)
    r.raise_for_status()


@app.route("/yes/<uniqid>")
def rsvp_yes(uniqid):
    logging.info("YES for uniqid: " + uniqid)

    member_id = get_member_by_uniqid(uniqid)

    update_rsvp(member_id, "Yes")

    return render_template("yes.html")


@app.route("/no/<uniqid>")
def rsvp_no(uniqid):
    logging.info("NO for uniqid: " + uniqid)

    member_id = get_member_by_uniqid(uniqid)

    update_rsvp(member_id, "No")

    return render_template("no.html")


if __name__ == '__main__':
    app.run(debug=True)
