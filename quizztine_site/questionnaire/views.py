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

def get_questions_id(questionnaire_id, short):
    liste =  Questions.query.filter_by(master_questionnaire=questionnaire_id).all()
    liste_id = []
    for x in liste :
        liste_id.append(x.id)
    shuffle(liste_id)
    if short is True :
        liste_id = liste_id[:25]
    return liste_id

def get_questions_id_azure(questionnaire_id, short):
    liste = QuestionsHTML.query.filter_by(master_questionnaire=questionnaire_id).all()
    liste_id = []
    for x in liste :
        liste_id.append(x.id)
    shuffle(liste_id)
    if short is True :
        liste_id = liste_id[:25]
    return liste_id

def get_shuffled_list_of_id(questionnaire_id):
    pass

def get_shuffled_list_id_short(questionnaire_id):
    pass





#choosing questionnaire
@questions.route('/questionnairechoice', methods=['GET', 'POST'])
def select_question_set():
    form = SelectQuestionnaireForm()
    form.questionnaires.choices = get_questionnaires()
    if form.validate_on_submit():
        # get selected question set
        session['questionnaire_id'] = form.questionnaires.data

        if int(session['questionnaire_id']) >= 17 : 
            session['all_questions_id'] = get_questions_id_azure(int(session['questionnaire_id']), form.yes_no.data)
            session['len_questions'] = len(session['all_questions_id'])
            return redirect('/questionnaireazure')
        else :
            session['all_questions_id'] = get_questions_id(int(session['questionnaire_id']), form.yes_no.data)
            session['len_questions'] = len(session['all_questions_id'])
            return redirect('/questionnaire')
    return render_template('select_questionnaire.html', form=form)



# viewing questions and entering input answer


@questions.route('/questionnaire', methods=['GET','POST'])
def questionnaire():
    questionnaire_id = session.get('questionnaire_id')
    if not questionnaire_id:
        return redirect('/questionnairechoice')
    
    all_questions_id = session['all_questions_id']
    if 'score' not in session:
        session['score'] = 0
    if 'current_question' not in session:
        session['current_question'] = 0

    current_question_id = all_questions_id[session['current_question']]
    real_current_question = Questions.query.filter_by(id=current_question_id).first()
    form = QuestionForm()

    if form.validate_on_submit():

        #get the answer from QuestionForm
        answer = form.answer.data
        if answer.lower() == real_current_question.answer.lower():
            message = '<br>Correct ! <br>' + real_current_question.explanation
            session['score'] += 1
        else:
            message = '<br>Incorrect ! <br>' + real_current_question.explanation

        return render_template('questionnaire.html', form=form, question=real_current_question.question, message=message, curr_question=session['current_question'], len_questions=session['len_questions'])
    return render_template('questionnaire.html', form=form, question=real_current_question.question, curr_question=session['current_question'], len_questions=session['len_questions'])

@questions.route('/questionnaireazure', methods=['GET','POST'])
def questionnaireazure():
    questionnaire_id = session.get('questionnaire_id')
    if not questionnaire_id:
        return redirect('/questionnairechoice')
    
    if 'score' not in session:
        session['score'] = 0
    if 'current_question' not in session:
        session['current_question'] = 0
        
    all_questions_id = session['all_questions_id']

    current_question_id = all_questions_id[session['current_question']]
    real_current_question = QuestionsHTML.query.filter_by(id=current_question_id).first()
    form = QuestionForm()

    if form.validate_on_submit():

        #get the answer from QuestionForm
        answer = form.answer.data
        if answer.lower() == real_current_question.answer.lower():
            message = '<br>Correct ! <br>' + real_current_question.answer_html
            session['score'] += 1
        else:
            message = '<br>Incorrect ! <br>' + real_current_question.answer_html

        return render_template('questionnaireazure.html', form=form, questionid=real_current_question.id, question=real_current_question.question_html, options=real_current_question.options_html, message=message, curr_question=session['current_question'], len_questions=session['len_questions'])
    
    return render_template('questionnaireazure.html', form=form, questionid=real_current_question.id, question=real_current_question.question_html, options=real_current_question.options_html, curr_question=session['current_question'], len_questions=session['len_questions'])



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
    if int(session['questionnaire_id']) >= 17 : 
        return redirect(url_for('questions.questionnaireazure'))
    else:
        return redirect(url_for('questions.questionnaire'))

@questions.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('questions.select_question_set'))





