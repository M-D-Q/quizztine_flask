from quizztine_site import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from quizztine_site import db
from quizztine_site.models import Questionnaires, QuestionsHTML



def mod_answer (app, db):
   with app.app_context():
      input_id = int(input("""Which ID :
   --> """))
      question_a_changer = db.session.query(QuestionsHTML).filter_by(id=input_id).first()
      print(f"Current question : {question_a_changer.question_html}")
      print(f"Current Answer : {question_a_changer.answer}")
      answer_change = input("Your change :")
      question_a_changer.answer = answer_change
      db.session.add(question_a_changer)
      db.session.commit()

def mod_explanation (app, db):
   with app.app_context():
      input_id = int(input("""Which ID :
   --> """))
      question_a_changer = db.session.query(QuestionsHTML).filter_by(id=input_id).first()
      print(f"Current question : {question_a_changer.question_html}")
      print(f"Current Explanation : {question_a_changer.answer_html}")
      answerhtml_change = input("Your change :")
      question_a_changer.answer_html = answerhtml_change
      db.session.add(question_a_changer)
      db.session.commit()

def mod_question (app, db):
   with app.app_context():
      input_id = int(input("""Which ID:
   --> """))
      question_a_changer = db.session.query(QuestionsHTML).filter_by(id=input_id).first()
      print(f"Current question : {question_a_changer.question_html}")
      questionhtml_change = input("Your change: ")
      question_a_changer.question_html = questionhtml_change
      db.session.add(question_a_changer)
      db.session.commit()

def mod_options (app, db):
   with app.app_context():
      input_id = int(input("""Which ID:
   --> """))
      question_a_changer = db.session.query(QuestionsHTML).filter_by(id=input_id).first()
      print(f"Current question : {question_a_changer.question_html}")
      print(f"Current options : {question_a_changer.options_html}")
      optionhtml_change = input("Your change: ")
      question_a_changer.options_html = optionhtml_change
      db.session.add(question_a_changer)
      db.session.commit()

while True:
   choice = int(input("Modify 1.Answer or 2.Explanation 3.Question or 4.Options ?"))
   if choice == 1 :
      mod_answer(app,db)
   elif choice == 2 :
      mod_explanation(app,db)
   elif choice == 3 :
      mod_question(app,db)
   elif choice == 4 :
      mod_options(app,db)
   else :
      print("Miaou")
      exit()