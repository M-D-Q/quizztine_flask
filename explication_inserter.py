from quizztine_site import app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from quizztine_site import db
from quizztine_site.models import Questionnaires, QuestionsHTML
import re




#with app.app_context():


   # question_a_changer = db.session.query(Questionnaires).filter_by(name=item_name).first()

