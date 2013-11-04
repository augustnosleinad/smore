
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from app import models
from app import app


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/smoreStation')
def smoreStation():
	tasks = models.Task.query.all()
	return render_template('smoreStation.html', tasks=tasks)


if __name__ == '__main__':
	app.run(debug=True)

