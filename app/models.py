from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    tasks = db.relationship('Task', backref = 'user', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(64))
    creation_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    work_sessions = db.relationship('Worklog', backref = 'task', lazy = 'dynamic')

    def __repr__(self):
        return '<Task: %r, Started on: %r, Belongs to: %r>' % (self.task_name, self.timestamp, self.user_id)

class Worklog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    timestamp = db.Column(db.DateTime)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return '<Date: %r, Task: %r, Duration: %r>' % (self.timestamp, self.task_id, self.duration)