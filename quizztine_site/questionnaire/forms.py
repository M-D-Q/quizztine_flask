from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from quizztine_site.models import Questionnaires, Questions


class QuestionForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
"""class QuestionnaireSelectionForm(FlaskForm):
    questionnaire = SelectField('Questionnaire', choices=[], coerce=int)
    submit = SubmitField('Start')
    def __init__(self, *args, **kwargs):
        super(QuestionnaireSelectionForm, self).__init__(*args, **kwargs)
        questionnaires = Questionnaires.query.all()
        self.questionnaire.choices = [(q.id, q.name) for q in questionnaires]"""

class SelectQuestionnaireForm(FlaskForm):
    questionnaires = SelectField('Select a questionnaire', choices=[], validators=[DataRequired()])
    yes_no = BooleanField('Do you want only the 25 first questions?')
    submit = SubmitField('Start')


