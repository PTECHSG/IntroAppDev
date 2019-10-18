from flask import Flask, render_template, request, json, session, redirect, url_for, g
from redis import Redis
from random import *
import random

app = Flask(__name__)
# Connecting to Redis
redis = Redis(host='redis', port=6379)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

# Index route, first page to load for the app
@app.route('/')
def index():
    # checking for the user session
    if not g.user:
        return redirect('/login')
    # Checking for the total questions 
    if not session['total']:
        return redirect('/gameover')
    # Loading questions from JSON file
    data = json.loads(getJsonData())
    value = str(random.randint(1, 26))
    data['guess'] = data[value] # Name to Guess
    data['index'] = value # Index of the name
    data['score'] = session['userscore'] # Score
    session['total'] -= 1  # Decrementing the Number of questions
    # Storing the name to guss in redis
     redis.set('secret', str(data['guess']['name']))
    # session['secret'] = str(data['guess']['name'])
    # Passing personality image, name to guess, Score to UI
    return render_template('index.html', data=data )

@app.route('/login')
# Renders the login page
def checkUser():
    return render_template('login.html')

def getJsonData():
    with open('guess.json', 'r') as jsonfile:
        file_data = jsonfile.read()
    return file_data

@app.route('/startGame', methods=['POST'])
# Receives the emailid from login screen and
# registers the user session
def startGame():
    if request.method == "POST":
        myname = request.form['myname']
        if myname:
            # Registering user session
            session['user'] = myname
            # Initial score set as 0
            session['userscore'] = 0
            # Total Questions
            session['total'] = 5
            return "startGame"

@app.route('/checkguess', methods=['POST'])
# Checking the Guess
def checkguess():
    responseCode = "Lose"
    if request.method == "POST":
        # Receiving the form value
        guess = request.form['myguess']
        index = request.form['index']
        # Reading from redis
        #chkData = redis.get('secret').decode()
        chkData = session['secret']
        # Comparing the secret and guess
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