from flask import Flask,render_template,request,redirect,flash

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)

responses = []

@app.route("/")
def home_page():
    return render_template("home.html",title = satisfaction_survey.title, instructions = satisfaction_survey.instructions)

    