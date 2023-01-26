from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import *
from selenium.webdriver.chrome.options import Options
import json
from quizztine_site import app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from quizztine_site import db
from quizztine_site.models import Questionnaires, QuestionsHTML
import re

def replace_image_html(string_html):
    match = re.search(r'<img src="\./AZ-104_files/(.+)" class="in-exam-image">', string_html)
    if match :
        miaou = match.group(1)
        string_corrigee = r'''<img src="{{url_for('static',filename='images/'''+str(miaou)+r'''\')}}">'''
        new_string = re.sub(r'<img src="\./AZ-104_files/(.+)" class="in-exam-image">', string_corrigee, string_html)
        return(new_string)
    else :
        return(string_html)

pattern_1 = r'<span class="badge badge-success most-voted-answer-badge".+</span>'
pattern_2 = r'<div class="voted-answers-tally d-none">.+</div>'
capture_group = r'"voted_answers": "([A-E]{1,5})"'
regex_patterns = [pattern_1, pattern_2, capture_group]

#setup webdriver
chrome_options = Options()

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.implicitly_wait(3)
browser.maximize_window()

#get l'url de base :
local_url = 'C:\\Users\\mdequick\\OneDrive - Capgemini\\Documents\\by_coding\\quizztine_flask\\AZ-104.html'
base_url = "https://www.examtopics.com/exams/microsoft/az-104/custom-view/"
browser.get(local_url)

def login(browser):
    #login
    username = "sliman.derrouiche@hotmail.fr"
    password = "CAP2023"

    browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/div/form/div[1]/div/input").send_keys(username)
    browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/div[2]/div/form/div[2]/div[1]/input").send_keys(password)
    browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/div[2]/div/form/button").click()

    #cheminement pour activer la vue en 455 (apparement ça met 228, good enough)
    browser.find_element(By.ID, "QuestionCount").send_keys("455")
    browser.find_element(By.ID, "QuestionCount").click()
    browser.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()

#maintenant, recup le texte d'une question
def recup_question_inputable(card_exam_question_card, patterns):
    titre_question = card_exam_question_card.find_element(By.CLASS_NAME,value="card-header").text
    topic_question = card_exam_question_card.find_element(By.CLASS_NAME, value="question-title-topic").text
    text_question = card_exam_question_card.find_element(By.CLASS_NAME,value="card-text").get_attribute('innerHTML')
    text_question = replace_image_html(text_question)
    options_question = card_exam_question_card.find_element(By.CLASS_NAME,value="question-choices-container").get_attribute('innerHTML')
    options_question = replace_image_html(options_question)

    inputable_answer = card_exam_question_card.find_element(By.CLASS_NAME,value="correct-answer").text
    if len(inputable_answer) <= 1 :
        inputable_answer = card_exam_question_card.find_element(By.CLASS_NAME,value="correct-answer").get_attribute('innerHTML')
    answer_and_explanation = card_exam_question_card.find_element(By.CLASS_NAME,value="correct-answer").get_attribute('innerHTML')+" \n <br>"+card_exam_question_card.find_element(By.CLASS_NAME,value="answer-description").get_attribute('innerHTML')
    answer_and_explanation = replace_image_html(answer_and_explanation)

    #### UN PEU DE REGEX - je veux vérifier si la 'Correct Answer' est aussi la 'most voted'
    capture_group = patterns[2]
    match = re.search(capture_group,inputable_answer)
    if match:
        voted_answers = match.group(1)
        if re.search(r'"is_most_voted": true',inputable_answer) and inputable_answer == voted_answers:
            trustworthy = "true"
        else :
            trustworthy = "false"
    else :
        trustworthy = "unknown"
    liste_html = [titre_question, text_question, options_question, inputable_answer, answer_and_explanation, topic_question, trustworthy]
    #Re regex - cette fois ci pour éliminer les patterns poubelles
    for item in range(0, len(liste_html)):
            liste_html[item] = re.sub(str(patterns[0]), '', str(liste_html[item]))
            liste_html[item] = re.sub(str(patterns[1]), '', str(liste_html[item]))
    return liste_html
    #c'est reglé je crois -----WARNING DES FOIS YA RIEN QUI SORT POUR LE INPUTABLE ANSWER : visiblement le '.text' ne fait pas toujours le taf, faudra peut etre juste prendre le inner html et laver ça au regex.

def recup_question_non_inputable(card_exam_question_card):
    titre_question = card_exam_question_card.find_element(By.CLASS_NAME,value="card-header").text
    return titre_question

# En fait il faut commencer par itérer par toutes les questions. 

def miaou(browser, patterns):
    i = 0
    all_questions = browser.find_elements(By.CLASS_NAME, value="exam-question-card")
    liste_contenu_inputables = [] #ce sera une liste de liste contenants tt les colonnes
    liste_question_non_inputables = [] #pour juste stocker le nom (num + topic) des questions sans input possible
    for element_miaou in all_questions :
        je_check_juste_un_truc = element_miaou.find_element(By.CLASS_NAME,value="correct-answer")
        i += 1
        
        if je_check_juste_un_truc.find_elements(By.TAG_NAME,value="img"):
            print("voici une où la réponse est une image")
            liste_question_non_inputables.append(recup_question_non_inputable(element_miaou))
            print(liste_question_non_inputables)

        else :
            print("et là c'est une lettre")
            liste_contenu_inputables.append(recup_question_inputable(element_miaou,patterns))
        if i > 14 :
            break
    print("FINITO, GO DB MAITENANT")
    return(liste_contenu_inputables)

def add_to_the_db(liste_contenu_inputables):
    
    #questionnaire_name = "AZ-104 Everything"
    #new_questionnaire = Questionnaires(name=questionnaire_name)
    #db.session.add(new_questionnaire)
    #db.session.commit()
        # Iterate through the questions in the list
    for item in liste_contenu_inputables :
        item_name = item[5]
        itemkek = db.session.query(Questionnaires).filter_by(name=item_name).first()
        if itemkek:
            master_questionnaire = itemkek.id
        else:
            new_questionnaire = Questionnaires(name=item_name)
            db.session.add(new_questionnaire)
            db.session.commit()
            master_questionnaire = new_questionnaire.id
        # Create a new instance of the Questions model and add it to the session
        new_question = QuestionsHTML(question_name=item[0],
                                    question_html=item[1],
                                    options_html=item[2],
                                    answer=item[3],
                                    answer_html=item[4],
                                    master_questionnaire=master_questionnaire,
                                    trustworthiness=item[6])
        db.session.add(new_question)
        db.session.commit()
    db.session.commit()

with app.app_context():
    add_to_the_db(miaou(browser,regex_patterns))

#trouver un moyen d'exporter la liste au cas où ça merde
####Miaou

#insérer dans la ddb : bon exemple d'insertion toute faite
