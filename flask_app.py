REQUIRE_LOGIN=True

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
USER_CREDENTIALS['hashed_password'] = 'scrypt:32768:8:1$egpdQHmkDe9eMU4M$b22cd80c2528b8ffc3f8697c607812df36ecdf1b69ed3a39e21748e59a79c423c3508e8086923e24429e7aec4aee8583c11a486fa3f5cd727ef89732e90340a8' #generate_password_hash("password123")

@auth.verify_password
def auth_verify_password(username, password):
    if REQUIRE_LOGIN:
        return username == USER_CREDENTIALS['username'] and check_password_hash(USER_CREDENTIALS['hashed_password'], password)
    else:
        return True

def auth_login_toggled(route):
    if REQUIRE_LOGIN:
        return auth.login_required(route)
    return route

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}'.format(
    username='zhengqunkoo',
    password='q7F2!hP!PxF5s4g',
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


@app.route('/')
def index():
    return redirect(url_for('handle_comments'))

def get_comments():
    return render_template('main_page.html', comments=Comment.query.all())

@auth_login_toggled
def post_comment():
    content = request.form['comment']
    comment = Comment(content=content)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('handle_comments'))

@app.route('/comment_page', methods=['GET', 'POST'])
def handle_comments():
    if request.method == 'GET':
        return get_comments()
    elif request.method == 'POST':
        return post_comment()
    else:
        return 'Unknown request method'

@app.route("/login/")
def login():
    return render_template("login_page.html")
