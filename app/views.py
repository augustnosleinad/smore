
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
# from flask.ext.sqlalchemy import SQLAlchemy
from app import app, db, models, lm, oid
from forms import LoginForm
from models import User, Task, ROLE_USER, ROLE_ADMIN


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('smoreStation'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname','email'])
	return render_template('login.html', title = 'Sign In', form = form, providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('smoreStation'))

@app.route('/smoreStation')
def smoreStation():
	tasks = models.Task.query.all()
	return render_template('smoreStation.html', tasks=tasks)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)

