from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/yes/<uniqid>")
def rsvp_yes(uniqid):
    return uniqid


if __name__ == '__main__':
    app.run(debug=True)
