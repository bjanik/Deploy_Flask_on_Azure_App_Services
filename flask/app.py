import re
import time

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request
)

from .db import DB
from .mail_sender import send_email

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    email_regex = r'^[\w.]+@[\w]+.([\w]{2,})$'
    email = request.form.get('email')
    
    timing = int(request.form.get('time'))
    prog = re.compile(email_regex)
    if not prog.match(email):
        return "Bad email"
    message = "Email was sucessfully send!"
    try:
        with DB() as db:
            anecdotes = db.get_last_anecdotes(timing)
            send_email(email, anecdotes)
    except Exception as e:
        message = e
    return render_template("feedback.html", message=message)

@app.route("/feedback")
def feedback():
    pass

if __name__ == '__main__':
    load_dotenv()
    app.run('0.0.0.0', port=8000, debug=True)