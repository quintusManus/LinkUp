from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, RegistrationForm2
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for
import random, threading, webbrowser
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert, update
import sqlite3
import os

print("Hello world!")

app = Flask(__name__)    #Flask Application instance 

proxied = FlaskBehindProxy(app)  ## add this line

app.config['SECRET_KEY'] = '294146b1ac1045ca756e85649cd2486c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

#User Object For Table 
class users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  #age = db.Column(db.String(60), nullable = False)
  Q1 = db.Column(db.String(20), nullable=True)
  Q2 = db.Column(db.String(20), nullable=True)
  Q3 = db.Column(db.String(20), nullable=True)
  Q4 = db.Column(db.String(20), nullable=True)
  Q5 = db.Column(db.String(20), nullable=True)


  def __repr__(self):
    return f"users('{self.username}', '{self.email}')"

#Table for matches


#Table for Questions
class prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Q1 = db.Column(db.String(20), nullable=True)
    Q2 = db.Column(db.String(20), nullable=True)
    Q3 = db.Column(db.String(20), nullable=True)
    Q4 = db.Column(db.String(20), nullable=True)
    Q5 = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"prompt('{self.Q1}', '{self.Q2}', '{self.Q3}', '{self.Q4}', '{self.Q5}')" 

    
    

@app.route("/")
def hello_world():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')
    
@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')


#REGISTER
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = users(username=form.username.data, email=form.email.data, password=form.password.data, Q1=None, Q2=None, Q3=None, Q4=None, Q5=None)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        
        #making each users match table
        name = form.username.data
        engine = create_engine('sqlite:///site.db', echo = True)
        meta = MetaData()
        students = Table(
        name, meta, 
        Column('id', Integer, primary_key = True), 
        Column('matches', String)
        )
        meta.create_all(engine)

        return redirect('/questionnaire') # if so - send to questionnaire

    return render_template('register.html', title='Register', form=form)


#LOGIN
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = RegistrationForm2()
    if form.validate_on_submit(): # checks if entries are valid
        user = users(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('login.html', title='Login', form=form) 

@app.route("/questionnaire", methods=['GET', 'POST'])
def questions():
    return render_template('questionnaire.html', subtitle='Questionnaire Page', text='This is the questionnaire page')

#Where questionnaire data is actually added to the database. Linked here from submit button in questionnaire.html, 
#action="/questionnaire-result"
@app.route("/questionnaire-result", methods=['POST'])
def results():
    answer_1 = request.form.get('astrology')
    answer_2 = request.form.get('t.a')
    answer_3 = request.form.get('juice')
    answer_4 = request.form.get('planets')
    answer_5 = request.form.get('money')
    
    rows = session.query(users).count()
    print(rows)
    #name = form.username.data, Q1 = answer_1 , Q2 = answer_2 , Q3 = answer_3 , Q4 = answer_4, Q5 = answer_5)
    
    db.session.add(user_answers)
    db.session.commit()
    
    #send the user back home when they submit the questionnaire. Can be changed to another page
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/match", methods=['GET', 'POST'])
def match():
    #query username
    #query questionnaire
    return render_template('match.html', subtitle='Match Page', text='Welcome to the real Fun!')

'''@app.route("/match-result", methods=['POST'])
def matchresults():
    pass'''

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True, host="0.0.0.0")