from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyATJ6ckPS6_BPvCfJw5MFjtfRoAjIh5KsI",
  "authDomain": "samar-s-project.firebaseapp.com",
  "projectId": "samar-s-project",
  "storageBucket": "samar-s-project.appspot.com",
  "messagingSenderId": "920213704699",
  "appId": "1:920213704699:web:eb7b00d5d8c2de67d0055e",
  "measurementId": "G-HMPF6VNE6L",
  "databaseURL": "https://samar-s-project-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return  redirect(url_for('add_tweet'))
    except:
        return redirect(url_for("signin"))
    return render_template("signin.html")
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            UID = login_session['users']['localId']
            user = {'fullname':request.form['fullname'],'username':request.form['username'],'bio':request.form['bio']}
            db.child("users").child(UID).set(user)
            return redirect(url_for("add_tweet"))
    except:
        return redirect(url_for('signup'))
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)