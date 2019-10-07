from flask import Flask, render_template, request, json, session, redirect, url_for, g
from redis import Redis
from random import *
import random

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/')
def index():
    # checking for the user email
    if not g.user:
        return redirect('/login')
    if not session['total']:
        return redirect('/gameover')
    data = json.loads(getJsonData())
    value = str(random.randint(1, 26))
    data['guess'] = data[value]
    data['index'] = value
    data['score'] = session['userscore']
    session['total'] -= 1
    redis.set('secret', str(data['guess']['name']))
    return render_template('index.html', data=data )

@app.route('/login')
def checkUser():
    return render_template('login.html')

def getJsonData():
    with open('guess.json', 'r') as jsonfile:
        file_data = jsonfile.read()
    return file_data

@app.route('/startGame', methods=['POST'])
def startGame():
    if request.method == "POST":
        emailid = request.form['myemail']
        if emailid:
            session['user'] = emailid
            session['userscore'] = 0
            session['total'] = 10
            return "startGame"

@app.route('/checkguess', methods=['POST'])
def checkguess():
    responseCode = "Lose"
    if request.method == "POST":
        guess = request.form['myguess']
        index = request.form['index']
        chkData = redis.get('secret').decode()
        if chkData == guess.lower():
            session['userscore'] += 10
            responseCode = "Win"
        return responseCode

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/gameover')
def gameOver():
    score = session['userscore']
    name = session['user']
    logout()
    return render_template('gameover.html', name=name, score=score)

if __name__ == "__main__":
    app.secret_key = 'guess the celebrity game'
    app.run(host="0.0.0.0", debug=True)