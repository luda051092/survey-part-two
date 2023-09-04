from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *
from sessionhandler import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "coffee-cake"

debug = DebugToolbarExtension(app)

# responses = []

@app.route("/")
def show_index():
    """Survey start page"""

    survey = get_current_survey_key()

    set_current_survey(survey)

    return render_template("index.html", survey=surveys[survey])


@app.route("/", methods=["POST"])
def start_survey():
    """Start survey; redirect to beginning questions"""

    return redirect("/questions/0")

@app.route("/surveys")
def show_surveys():
    return render_template("surveys.html" , surveys = surveys)


@app.route("/questions/<int:question_index>")
def show_question(question_index):
    """show question page"""
    current_survey = get_current_survey()


    current_responses = get_current_responses()

    if question_index != len(current_responses):
        flash("Take the survey in order please. Thank you.")
        return redirect(f"/questions/{len(current_responses)}")
    
    if question_index < len(current_survey.questions):
        return render_template("question.html" , survey = current_survey , question_index = question_index)
    
    else: 
        return redirect("/thankyou")
    

@app.route("/answer")
def get_answer():
    """handle answer, redirect to proceeding question"""
    question_index = int(request.args.get("question_index"))
    question_answer = int(request.args.get("radio_choice"))
    comment = request.args.get("comment")

    current_survey = get_current_survey()
    answer = current_survey.questions[question_index].choices[question_answer]

    set_current_responses(Response(answer , comment))

    return redirect(f"/questions/{question_index +1}")

@app.route("/thankyou")
def show_thankyou():
    """show thank you"""

    current_survey = get_current_survey()

    return render_template("thankyou.html" , survey = current_survey , responses = get_current_responses())

@app.route("/reset" , methods=["POST"])
def reset():
    """reset survey"""

    reset_current_responses()

    return redirect("/")