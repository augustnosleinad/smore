from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    tasks = db.relationship('Task', backref = 'user', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Task: %r, Duration: %r>' % (self.task_name, self.duration)