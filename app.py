from flask import Flask,render_template,request,redirect,flash,session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

app = Flask(__name__)


app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
app.config["SECRET_KEY"]="chicken"
debug = DebugToolbarExtension(app)

RESPONSE = "responses"
current = 0

@app.route("/")
def home_page():
    return render_template("home.html",title = survey.title, instructions = survey.instructions)

@app.route("/begin",methods = ["POST"])
def start_survey():
    session[RESPONSE]=[]
    return redirect("/questions/0") 

@app.route(f"/questions/<int:question_number>")
def question(question_number):
    responses = session.get(RESPONSE)
    if responses is None:
        return redirect("/")
    
    if len(responses) == len(survey.questions):
        return redirect("/thankyou")
    
    if len(responses) != question_number:
        flash(f"Invalid Question ID : {question_number}")
        return render_template("question.html", current = len(responses) , question = survey.questions, responses = responses)
    
    return render_template("question.html", current = question_number , question = survey.questions, responses = responses)

@app.route("/answer",methods=["POST"])
def answer():
    global current
    answer = request.form.get("answer")
    responses = session[RESPONSE]
    responses.append(answer)
    session[RESPONSE]=responses
    
    current += 1
    if current >= len(survey.questions):
        # Handle case when all questions are answered
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{current}")
    
@app.route("/thankyou")
def thanks():
    return render_template("thanks.html")
    