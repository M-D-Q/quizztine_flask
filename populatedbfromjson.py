import json
from quizztine_site import app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from quizztine_site import db
from quizztine_site.models import Questionnaires, Questions


with open ("auto_christine.json", "r", encoding='utf-8') as dico:
    dataset = dico.read()
    data = json.loads(dataset)

with app.app_context():
    db.create_all()








    for key in data.keys():
            new_questionnaire = Questionnaires(name=str(key))
            db.session.add(new_questionnaire)
            db.session.commit()
            # Iterate through the questions in the questionnaire
            for questione in data[key]:
                # Create a new instance of the Questions model and add it to the session
                new_question = Questions(question=questione['question'], answer=questione['answer'],
                                        explanation=questione['explanation'], original_url=questione.get('url', None), master_questionnaire=new_questionnaire.id)
                db.session.add(new_question)
            db.session.commit()

