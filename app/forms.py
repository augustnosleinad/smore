from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, IntegerField
from wtforms.validators import Required

class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

class NewTaskForm(Form):
	task = TextField('task', validators = [Required()])

class TrackDurationForm(Form):
	duration = IntegerField('duration', validators = [Required()])
	active_task = TextField('active_task', validators = [Required()])