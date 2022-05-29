from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.balance_model import Balance


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
# first visit/root page
def root():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/welcome')

@app.route('/welcome')
# first page if user not logged in
def welcome():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('landing.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_all_present(request.form):
        return redirect('/welcome')
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'pw_hash' : pw_hash,
    }
    user_id = User.create_user(data)
    session['user_id'] = user_id
    Balance.create_balance({'user_id' : user_id })
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { 'email' : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid email or password!', 'err.login')
        return redirect('/welcome')
    if not bcrypt.check_password_hash(user_in_db.pw_hash, request.form['pw']):
        flash('Invalid email or password!', 'err.login')
        return redirect('/welcome')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/welcome')
    data = { 'id':session['user_id']}
    user=User.get_one(data)
    data = { 'user_id' : session['user_id']}
    session['temp_foods'] = []
    session['temp_id'] = 0
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/welcome')