from quizztine_site import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Username {self.username}"

class BlogPost(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id
    def __repr__(self): 
        return f"Post ID: {self.id} -- Date: {self.date} ---- {self.title}"

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(140), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    original_url = db.Column(db.String(140), nullable=True)
    master_questionnaire = db.Column(db.Integer, db.ForeignKey('questionnaires.id'))

    def __init__(self, question, answer, explanation, original_url, master_questionnaire):
        self.question = question
        self.answer = answer
        self.explanation = explanation
        self.original_url = original_url
        self.master_questionnaire = master_questionnaire

class Questionnaires(db.Model):
    __tablename__ = 'questionnaires'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, description=''):
        self.name = name
        self.description = description

class QuestionsHTML(db.Model):
    __tablename__ = 'questionsHTML'
    id = db.Column(db.Integer, primary_key=True)
    question_name = db.Column(db.Text, nullable=False)
    question_html = db.Column(db.Text, nullable=False)
    options_html = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(140), nullable=False)
    answer_html = db.Column(db.Text, nullable=False)
    master_questionnaire = db.Column(db.Integer, db.ForeignKey('questionnaires.id'))
    trustworthiness = db.Column(db.String(140), nullable=False)

    def __init__(self, question_name, question_html, options_html, answer, answer_html, master_questionnaire, trustworthiness):
        self.question_name = question_name
        self.question_html = question_html
        self.options_html = options_html
        self.answer = answer
        self.answer_html = answer_html
        self.master_questionnaire = master_questionnaire
        self.trustworthiness = trustworthiness
