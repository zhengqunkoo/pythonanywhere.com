REQUIRE_LOGIN=True

from flask import Flask, redirect, render_template, request, url_for
from flask_httpauth import HTTPBasicAuth
if REQUIRE_LOGIN:
    from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin

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

app.secret_key = "sduivdluyt8o86575"
login_manager = LoginManager()
login_manager.init_app(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

all_users = {
    'admin': User('admin', generate_password_hash('secret')),
    'bob': User('bob', generate_password_hash('less-secret')),
    'caroline': User('caroline', generate_password_hash('completelysecret')),
}

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)


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

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_page.html', login_error=False)

    username = request.form['username']
    if username not in all_users:
        return render_template('login_page.html', login_error=True)

    user = all_users[username]
    if not user.check_password(request.form['password']):
        return render_template('login_page.html', login_error=True)

    login_user(user)
    return redirect(url_for('index'))
