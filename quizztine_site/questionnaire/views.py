from flask import render_template, url_for, flash, session, request, redirect, Blueprint, abort
from quizztine_site.questionnaire.forms import QuestionForm, SelectQuestionnaireForm
from quizztine_site import db
from quizztine_site.models import Questionnaires,Questions

questions = Blueprint('questions', __name__)


def get_questionnaires():
    questionnaires = Questionnaires.query.all()
    return [(q.id, q.name) for q in questionnaires]

def get_questions(questionnaire_id):
    return Questions.query.filter_by(master_questionnaire=questionnaire_id).all()


#choosing questionnaire
@questions.route('/questionnairechoice', methods=['GET', 'POST'])
def select_question_set():
    form = SelectQuestionnaireForm()
    form.questionnaires.choices = get_questionnaires()
    if form.validate_on_submit():
        # get selected question set
        session['questionnaire_id'] = form.questionnaires.data
        return redirect('/questionnaire')
    return render_template('select_questionnaire.html', form=form)



# viewing questions and entering input answer


@questions.route('/questionnaire', methods=['GET','POST'])
def questionnaire():
    questionnaire_id = session.get('questionnaire_id')
    if not questionnaire_id:
        return redirect('/questionnairechoice')
    all_questions = get_questions(questionnaire_id)

    if 'score' not in session:
        session['score'] = 0
    if 'current_question' not in session:
        session['current_question'] = 0

    #current_question = session.get('current_question', 0)
    #score = session.get('score', 0)
    current_question = session['current_question']
    score = session['score']

    form = QuestionForm()

    if form.validate_on_submit():

        #get the answer from QuestionForm
        answer = form.answer.data
        if answer.lower() == all_questions[current_question].answer.lower():
            message = 'Correct ! \n' + all_questions[current_question].explanation
            session['score'] += 1
            #current_question += 1
            #session['current_question'] = current_question
            #session['current_question'] += 1
        else:
            message = 'Incorrect ! \n' + all_questions[current_question].explanation
            #current_question += 1
            #session['current_question'] = current_question
            #session['current_question'] += 1

        if current_question >= len(all_questions):
            percentage = (score / len(all_questions)) * 100
            session['percentage'] = percentage
            return redirect(url_for('questions.result'))
        else :
            return render_template('questionnaire.html', form=form, question=all_questions[current_question].question, message=message)
    return render_template('questionnaire.html', form=form, question=all_questions[current_question].question)


@questions.route('/result')
def result():
    return render_template('result.html', score=session['percentage'])

@questions.route('/next_question', methods=['GET','POST'])
def next_question():
    session['current_question'] += 1
    return redirect(url_for('questions.questionnaire'))





