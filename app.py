from flask import Flask,render_template,request,redirect,flash

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
app.config["SECRET_KEY"]="chicken"
debug = DebugToolbarExtension(app)

responses = []
current = 0

@app.route("/")
def home_page():
    return render_template("home.html",title = satisfaction_survey.title, instructions = satisfaction_survey.instructions)

@app.route(f"/questions/<int:question_number>")
def question(question_number):
    return render_template("question.html", current = question_number , question = satisfaction_survey.questions, responses = responses)

@app.route("/answer")
def answer():
    global current
    answer = request.args["answer"]
    responses.append(answer)
    current += 1
    if current >= len(satisfaction_survey.questions):
        # Handle case when all questions are answered
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{current}")
    
@app.route("/thankyou")
def thanks():
    return render_template("thanks.html")
    