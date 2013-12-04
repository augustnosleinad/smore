

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from app import app, db, models, lm, oid
from forms import LoginForm, NewTaskForm, TrackDurationForm
from models import User, Task, ROLE_USER, ROLE_ADMIN
from datetime import datetime


import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO


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
                return redirect(url_for('smore_station'))
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
    return redirect(request.args.get('next') or url_for('smore_station'))

@app.route('/smore_station', methods = ['GET','POST'])
@login_required
def smore_station():
    form = NewTaskForm()

    if form.validate_on_submit():
        task = Task(task_name = form.task.data, timestamp = datetime.utcnow(), duration = 0, user_id = g.user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task added!')
        return redirect(url_for('smore_station'))

    duration_form = TrackDurationForm()

    if duration_form.validate_on_submit():
        active_task = duration_form.active_task.data
        task = Task.query.get(active_task)
        task.duration += duration_form.duration.data
        db.session.commit()
        flash('Database updated!')
        return redirect(url_for('smore_station'))

    tasks = models.Task.query.all()
    return render_template('smore_station.html', user = user, form = form, duration_form = duration_form, tasks=tasks)


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()

    # get the tasks associated with the user
    #haven't tested yet task_list = Task.query.filter_by(user_id = user)
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('home'))
    tasks = Task.query.all()


    html = '''

        <img src="data:image/png;base64,{}" />

    ''' 

    N = 5
    smore = (20, 35, 30, 35, 27)
    
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)


    rects1 = ax.bar(ind, smore, width, color='r')

    sqlal = (25, 32, 55, 20, 25)
    rects2 = ax.bar(ind+width, sqlal, width, color='y')

    # add some
    ax.set_ylabel('Duration')
    ax.set_title('Time spent working')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('11/21', '11/22', '11/23', '11/24', '11/25') )

    ax.legend( (rects1[0], rects2[0]), ('Smore', 'SQLAlchemy') )

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    # Encode image to png in base64
    io = StringIO()
    fig.savefig(io, format='png')
    data = io.getvalue().encode('base64')
    graph = html.format(data)

    return render_template('user.html', user = user, tasks = tasks, graph = graph)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
        app.run(debug=True)