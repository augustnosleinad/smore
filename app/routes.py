# import sqlite3

# with sqlite3.connect("smores.db") as connection:
# 	c = connection.cursor()
# 	c.execute("""CREATE TABLE worklog
# 				(day TEXT, duration REAL, runningTotal REAL)
# 				""")
# 	c.execute('INSERT INTO posts VALUES("6/25","1.5","6.25")')
# 	c.execute('INSERT INTO posts VALUES("6/26","0.5","6.75")')
# 	c.execute('INSERT INTO posts VALUES("6/27","2.5","9.25")')


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/smoreStation')
def smoreStation():
	return render_template('smoreStation.html')

if __name__ == '__main__':
	app.run(debug=True)

