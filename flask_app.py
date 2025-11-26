REQUIRE_LOGIN=False

from flask import Flask, redirect, render_template, request, url_for
from flask_httpauth import HTTPBasicAuth
if REQUIRE_LOGIN:
    from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

auth = HTTPBasicAuth()
USER_CREDENTIALS = {}
USER_CREDENTIALS['username'] = 'zhengqunkoo'
# Store hashed password (in a real application, save this securely in a database)
USER_CREDENTIALS['hashed_password'] = 'scrypt:32768:8:1$pLZfdLYlJ9sI8hZr$0894222e1765b0d212e11941441624f5fe9c606d8f0683187e9cab9373f23b80e25ee71a0c160305ae4dacff2abd3afd1562c2a692491d69d16edd9b5e095fa2' #generate_password_hash("password123")

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}'.format(
    username='zhengqunkoo',
    password='R3d!f7VxPq2Z',
    hostname='zhengqunkoo.mysql.pythonanywhere-services.com',
    databasename='zhengqunkoo$comments'
)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


comments = []

@app.route('/')
def index():
    return redirect(url_for('handle_comments'))

@auth.verify_password
def login(username, password):
    if REQUIRE_LOGIN:
        return username == USER_CREDENTIALS['username'] and check_password_hash(USER_CREDENTIALS['hashed_password'], password)
    else:
        return True

@app.route('/comment_page', methods=['GET', 'POST'])
@auth.login_required
def handle_comments():
    if request.method == 'GET':
        return render_template('main_page.html', comments=comments)
    elif request.method == 'POST':
        comments.append(request.form['comment'])
        return redirect(url_for('index'))
    else:
        return 'Unknown request method'