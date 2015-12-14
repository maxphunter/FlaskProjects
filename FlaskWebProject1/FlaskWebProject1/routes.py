from flask import Flask, url_for, render_template, redirect, request;
from app import app;
import redis;

r = redis.StrictRedis(host='localhost',port=6379, db=0, charset="utf-8", decode_responses=True );

@app.route('/')
def hello():
    createLink = "<a href='"+ url_for('create') + "'>Create a question </a>";
    """Renders a sample page."""
    return """<html>
                <head> <title>Hello, world!</title>
                </head>
                <body>""" + createLink + """
                </body>
            </html>""";

@app.route('/candy')
def candy():
    print('got to step 1');
    if request.method == 'GET':
        print("hello step 2");
        return render_template('Correct.html');
    else:
        return "failed";

@app.route('/create', methods=['GET', 'POST'])
def create():
    
    if request.method == 'GET':           
        return render_template('CreateQuestion.html');
    elif request.method == 'POST':
        title = request.form['title'];
        answer = request.form['answer'];
        question = request.form['question'];

        r.set(title +':question', question)
        r.set(title + ':answer', answer)

        return render_template('CreatedQuestion.html', question = question);
    else:
        return '<h2>Invalid Request</h2>';

@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == 'GET':
        question = r.get(title+':question')
        print(question)
        return render_template('AnswerQuestion.html', question = question);
    elif request.method == 'POST':
        submittedAnswer = request.form['submittedAnswer'];

        answer = r.get(title+':answer')

        if submittedAnswer == answer:
            print("almost there!")
            return render_template('Correct.html')
        else:
            return render_template('Incorrect.html', submittedAnswer = submittedAnswer, answer = answer)
    else:
        return "<h2>" + title + "</h2>";