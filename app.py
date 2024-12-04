# from flask import Flask, render_template
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     #return 'Flask  Page'
#     return render_template("index.html")
#
#
# @app.route('/hello')
# def hello():
#     return 'Hello, World'
#
#
# @app.route("/variable/<name>")
# def welcome(name):
#     return render_template("welcome.html", name=name)
#
#
#
# @app.route('/login')
# def Login():
#     return render_template("login.html")
#
#
#
# # if __name__ == '__main__':
# #    app.run()
# #
# #
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, bcrypt, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.before_request
def initialize_once():
    if not getattr(app, 'db_initialized', False):
        db.create_all()
        app.db_initialized = True


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or Email already exists!', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html')




@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"

if __name__ == '__main__':
    app.run(debug=True)


