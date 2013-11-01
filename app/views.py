
from flask import Flask, render_template
from app import app

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/smoreStation')
def smoreStation():
	return render_template('smoreStation.html')

if __name__ == '__main__':
	app.run(debug=True)

