from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/i_paid_database'
#password- Jay@1234$
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(20), primary_key=False)
    email = db.Column(db.String(20), primary_key=False)
    country_code = db.Column(db.String(3), primary_key=False)
    phone_no = db.Column(db.String(10), primary_key=False)
    password = db.Column(db.String(20), primary_key=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(20), primary_key=False)
    event_place = db.Column(db.String(20), primary_key=False)
    message = db.Column(db.String(20), primary_key=False)


@app.route('/')
def home():
    return render_template("main.html")


@app.route('/login')
def login():
    return render_template("Login.html", title='log in')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('full_name')
        email = request.form.get('email')
        country_code = request.form.get('country_code')
        phone = request.form.get('phone')
        password = request.form.get('password')
        add_entry = Client(full_name=fullname, email=email, country_code=country_code, phone_no=phone,
                           password=password)
        # add_entry = Client(full_name=fullname)
        db.session.add(add_entry)
        db.session.commit()
    return render_template("register.html", title='register')


@app.route('/event', methods=['GET', 'POST'])
def event():
    if (request.method == 'POST'):
        event_name     = request.form.get('event_name')
        event_place    = request.form.get('event_place')
        message        = request.form.get('message')
        for_entry = Event(event_name=event_name,event_place=event_place,message=message)
        db.session.add(for_entry)
        db.session.commit()
    return render_template("event.html", title='Event')


app.run(debug=True)
