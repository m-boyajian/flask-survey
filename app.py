from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSE_LIST = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "mumstheword"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_survey():
    """show the survey homepage"""

    return render_template('show_survey.html', survey=survey)


@app.route("/begin", methods=["POST"])
def begin_survey():
    """clear session responses"""

    session[RESPONSE_LIST]= []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """saves response and prompts next question"""

    """gets the response choice"""
    choice=request.form['answer']
    
    """adds the response choice to the session"""
    responses = session.get(RESPONSE_LIST)
    responses.append(choice)
    session[RESPONSE_LIST] = responses

    if (len(responses) == len(survey.questions)):
        """redirects to thank you page"""
        return redirect("/completed")
    
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):

    responses = session.get(RESPONSE_LIST)
    
    if (responses is None):

        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        """If accessing questions page too soon"""
        return redirect("/completed")

    if (len(responses) != qid):
        """If attempt to access questions out of order"""
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid] 

    return render_template("questions.html", question_num=qid, question=question)


@app.route("/completed")
def show_complete():
    """survey complete, brings to completed page"""
    return render_template("completed.html")
    
   


