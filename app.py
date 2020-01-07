from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ipaid.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=True)
    country_code = db.Column(db.String(3), nullable=True)
    phone_no = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(20), nullable=True)


    def __init__(self, full_name, email, country_code, phone_no, password):
        self.full_name = full_name
        self.email = email
        self.country_code = country_code
        self.phone_no = phone_no
        self.password = password


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(20), nullable=True)
    event_place = db.Column(db.String(20), nullable=True)
    message = db.Column(db.String(3), nullable=True)
    event_type = db.Column(db.String(10), nullable=True)
    no_of_peoples = db.Column(db.String(20), nullable=True)

    def __init__(self, event_name, event_place, message, event_type, no_of_peoples):
        self.event_name = event_name
        self.event_place = event_place
        self.message = message
        self.event_type = event_type
        self.no_of_peoples = no_of_peoples


# db.create_all()


@app.route('/')
def home():
    return render_template("main.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_client = Client.query.filter_by(email=email).first()
        if existing_client:
            passwords_match = check_password_hash(existing_client.password, password)
            if passwords_match:

                message = "client exist"
            else:
                message = "Please check your password"
        else:
            message = "client does not exist"

    return render_template("Login.html", title='log in', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        entry = Client(
            full_name=request.form.get('full_name'),
            email=request.form.get('email'),
            country_code=request.form.get('country_code'),
            phone_no=request.form.get('phone'),
            password=generate_password_hash(request.form.get('password'))
        )

        db.session.add(entry)
        db.session.commit()
    return render_template("register.html", title='register')


@app.route('/event', methods=['GET', 'POST'])
def event():
    if (request.method == 'POST'):
        event_name = request.form.get('event_name')
        event_place = request.form.get('event_place')
        message = request.form.get('message')
        no_of_peoples = request.form.get('quatity')
        event_type = request.form.get('event_type')
        entry = Event(event_name=event_name, event_place=event_place, message=message, no_of_peoples=no_of_peoples,
                      event_type=event_type)
        db.session.add(entry)
        db.session.commit()
    return render_template("event.html", title='Event')


app.run(debug=True)
