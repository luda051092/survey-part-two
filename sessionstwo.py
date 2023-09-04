from flask import request, session
from surveys import *

def get_responses():
    """return responses from session"""
    return session.get("responses", {})

def get_current_responses():
    """return responses for current survey"""
    return get_responses().get(get_current_survey_key(), [])

def set_responses(responses):
    """set responses value"""
    session["responses"] = responses

def set_current_responses(response):
    """set current response value"""
    responses = get_responses()
    current_responses = get_current_responses()
    current_responses.append(response)

    survey = get_current_survey_key()

    responses[survey] = current_responses

    set_responses(responses)

def reset_current_responses():
    """reset current responses"""
    responses = get_responses()
    survey = get_current_survey_key()
    responses[survey] = []
    set_responses(responses)

def get_current_survey_key():
    """return current survey key"""
    if request.args.get("survey"):
        return request.args.get("survey")
    return session.get("current_survey" , "satisfaction")

def set_current_survey(survey):
    """set current survey to session"""
    session["current_survey"] = survey

def get_current_survey():
    """return current survey"""
    return surveys.get(get_current_survey_key() , satisfaction_survey)