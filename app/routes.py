# import sqlite3

# with sqlite3.connect("timelog.db") as connection:
# 	c = connection.cursor()
# 	c.execute("""CREATE TABLE timelog
# 				(day TEXT, duration INT)
# 				""")
# 	c.execute("INSERT INTO timelog VALUES('6/25',90)")
# 	c.execute("INSERT INTO timelog VALUES('6/26',30)")
# 	c.execute("INSERT INTO timelog VALUES('6/27',150)")


from flask import Flask, render_template
from app import app
from flask.ext.sqlalchemy import SQLAlchemy

# configuration

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/smoreStation')
def smoreStation():
	return render_template('smoreStation.html')

if __name__ == '__main__':
	app.run(debug=True)

