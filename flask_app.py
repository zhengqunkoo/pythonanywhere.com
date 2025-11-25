
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['DEBUG'] = True

comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('main_page.html', comments=comments)
    elif request.method == 'POST':
        comments.append(request.form['comment'])
        return redirect(url_for('index'))
    else:
        raise Exception('Unknown request method')