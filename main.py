from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, RegistrationForm2
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for
import random, threading, webbrowser

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '294146b1ac1045ca756e85649cd2486c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/")
def hello_world():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')
    
@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = RegistrationForm2()
    if form.validate_on_submit(): # checks if entries are valid
        if form.validate_on_submit():
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('login.html', title='Login', form=form) 

@app.route("/questionnaire")
def questions():
    return render_template('questionnaire.html', subtitle='Questionnaire Page', text='This is the questionnaire page')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")