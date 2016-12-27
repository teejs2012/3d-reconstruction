from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm, SigninForm
import os

app = Flask(__name__)
db.init_app(app)

app.secret_key = "development-key"

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tang48316254@localhost/flask1'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/upload", methods = ['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)

	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		destination = "/".join([target, filename])
		print(destination)
		file.save(destination)
	return redirect(url_for('home'))

@app.route("/about")
def about():
	return render_template("about.html")
@app.route("/signup", methods = ['GET','POST'])
def signup():
	if 'email' in session:
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template('signup.html', form = form)
		else:
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email

			return redirect(url_for('home'))

	elif request.method == "GET":
		return render_template('signup.html', form = form)
@app.route("/home")
def home():
	if 'email' not in session:
		return redirect(url_for('signin'))
	return render_template("home.html")

@app.route("/signin", methods = ['GET', 'POST'])
def signin():
	if 'email' in session:
		return redirect(url_for('home'))
	
	form = SigninForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template('signin.html', form = form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('signin'))

	elif request.method == 'GET':
		return render_template("signin.html", form = form)

@app.route("/signout")
def signout():
	session.pop('email',None)
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)