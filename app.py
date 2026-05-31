from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)
app.secret_key = "rk_galaxy_super_secret"

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///galaxy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    opt1 = db.Column(db.String(200), nullable=False)
    opt2 = db.Column(db.String(200), nullable=False)
    opt3 = db.Column(db.String(200), nullable=False)
    opt4 = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/guest-login')
def guest_login():
    session['user'] = "Guest Pilot"
    session['is_guest'] = True
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('landing'))
    return render_template('home.html', user=session['user'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        u = request.form.get('username')
        e = request.form.get('email')
        p = request.form.get('password')
        if not User.query.filter((User.email == e) | (User.username == u)).first():
            new_user = User(username=u, email=e, password=p)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return "Pilot already exists!"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        user = User.query.filter_by(username=u, password=p).first()
        if user:
            otp = str(random.randint(1000, 9999))
            session['otp'] = otp
            session['temp_user'] = u
            session['is_guest'] = False
            print(f"\n🚀 [GALAXY TRANSMISSION] OTP for {user.email} is: {otp}\n")
            return redirect(url_for('otp_page'))
    return render_template('login.html')

@app.route('/otp')
def otp_page():
    return render_template('otp.html')

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    if request.form.get('otp_code') == session.get('otp'):
        session['user'] = session.get('temp_user')
        return redirect(url_for('home'))
    return "Access Denied: Wrong Code"

@app.route('/quiz')
def quiz():
    all_q = Question.query.all()
    quiz_list = [{"question": q.text, "options": [q.opt1, q.opt2, q.opt3, q.opt4], "answer": q.answer} for q in all_q]
    return render_template('index.html', quiz=quiz_list)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_q = Question(text=request.form['question'], opt1=request.form['opt1'], opt2=request.form['opt2'], 
                         opt3=request.form['opt3'], opt4=request.form['opt4'], answer=request.form['correct_answer'])
        db.session.add(new_q)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)