from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'abcdefg'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in!")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"
    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route("/", methods=['POST', 'GET'])
def index():
    return redirect("/blog")

@app.route("/blog", methods=['POST', 'GET'])
def mainblog():
    owner = User.query.filter_by(email=session['email']).first()
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_post = request.form['content']
        new_blog = Blog(blog_title, blog_post, owner)
        db.session.add()
        db.session.commit()
        
    posts = Blog.query.filter_by(owner=owner).all()
    return render_template('blog.html', title="Build-A-Blog", posts = posts)

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    # this page should display the form where you can enter a new post
    return "Hey!"

if __name__ == '__main__':
    app.run()
