from flask import render_template, url_for, flash, session, request, redirect, Blueprint, abort
from quizztine_site.questionnaire.forms import QuestionForm, SelectQuestionnaireForm
from quizztine_site import db
from quizztine_site.models import Questionnaires,QuestionsHTML, Questions
from random import shuffle
from  sqlalchemy.sql.expression import func


questions = Blueprint('questions', __name__)


def get_questionnaires():
    questionnaires = Questionnaires.query.all()
    return [(q.id, q.name) for q in questionnaires]

def get_questions(questionnaire_id):
    return Questions.query.filter_by(master_questionnaire=questionnaire_id).all()
    #order_by(func.random())

def get_questions_azure(questionnaire_id):
    return QuestionsHTML.query.filter_by(master_questionnaire=questionnaire_id).all()
    

#choosing questionnaire
@questions.route('/questionnairechoice', methods=['GET', 'POST'])
def select_question_set():
    form = SelectQuestionnaireForm()
    form.questionnaires.choices = get_questionnaires()
    if form.validate_on_submit():
        # get selected question set
        session['questionnaire_id'] = form.questionnaires.data
        session['25first'] = form.yes_no.data
        if int(session['questionnaire_id']) == 17 : 
            return redirect('/questionnaireazure')
        else :
            return redirect('/questionnaire')
    return render_template('select_questionnaire.html', form=form)



# viewing questions and entering input answer


@questions.route('/questionnaire', methods=['GET','POST'])
def questionnaire():
    questionnaire_id = session.get('questionnaire_id')
    if not questionnaire_id:
        return redirect('/questionnairechoice')
    all_questions = get_questions(questionnaire_id)
    

    #shuffle(all_questions)
    if session['25first']:
        all_questions = all_questions[:25]

    if 'score' not in session:
        session['score'] = 0
    if 'current_question' not in session:
        session['current_question'] = 0

    #current_question = session.get('current_question', 0)
    #score = session.get('score', 0)
    current_question = session['current_question']
    session['len_questions'] = len(all_questions)

    form = QuestionForm()

    if form.validate_on_submit():

        #get the answer from QuestionForm
        answer = form.answer.data
        if answer.lower() == all_questions[current_question].answer.lower():
            message = '<br>Correct ! <br>' + all_questions[current_question].explanation
            session['score'] += 1
        else:
            message = '<br>Incorrect ! <br>' + all_questions[current_question].explanation

        return render_template('questionnaire.html', form=form, question=all_questions[current_question].question, message=message, curr_question=current_question, len_questions=session['len_questions'])
    print(all_questions)
    return render_template('questionnaire.html', form=form, question=all_questions[current_question].question, curr_question=current_question, len_questions=session['len_questions'])

@questions.route('/questionnaireazure', methods=['GET','POST'])
def questionnaireazure():
    questionnaire_id = session.get('questionnaire_id')
    if not questionnaire_id:
        return redirect('/questionnairechoice')

    all_questions = get_questions_azure(questionnaire_id)
    print(all_questions)
    QuestionsHTML.query.filter_by(master_questionnaire=questionnaire_id).all()

    #shuffle(all_questions)
    if session['25first']:
        all_questions = all_questions[:25]

    if 'score' not in session:
        session['score'] = 0
    if 'current_question' not in session:
        session['current_question'] = 0

    #current_question = session.get('current_question', 0)
    #score = session.get('score', 0)
    current_question = session['current_question']
    session['len_questions'] = len(all_questions)

    form = QuestionForm()

    if form.validate_on_submit():

        #get the answer from QuestionForm
        answer = form.answer.data
        if answer.lower() == all_questions[current_question].answer.lower():
            message = '<br>Correct ! <br>' + all_questions[current_question].answer_html
            session['score'] += 1
        else:
            message = '<br>Incorrect ! <br>' + all_questions[current_question].answer_html

        return render_template('questionnaireazure.html', form=form, question=all_questions[current_question].question_html, options=all_questions[current_question].options_html, message=message, curr_question=current_question, len_questions=session['len_questions'])
    
    print(all_questions)
    return render_template('questionnaireazure.html', form=form, question=all_questions[current_question].question_html, options=all_questions[current_question].options_html, curr_question=current_question, len_questions=session['len_questions'])



@questions.route('/result')
def result():
    return render_template('result.html', score=session['percentage'])

@questions.route('/next_question', methods=['GET','POST'])
def next_question():
    session['current_question'] += 1
    if session['current_question'] >= session['len_questions']:
        percentage = (session['score'] / session['len_questions']) * 100
        session['percentage'] = percentage
        return redirect(url_for('questions.result'))
    if int(session['questionnaire_id']) == 17 : 
        return redirect(url_for('questions.questionnaireazure'))
    else:
        return redirect(url_for('questions.questionnaire'))

@questions.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('questions.select_question_set'))





