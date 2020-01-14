from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, url_for
from werkzeug.urls import url_parse
from ipaid.form import RegistrationForm, LoginForm
from ipaid.models import Client, Event
from werkzeug.utils import redirect
from ipaid import app, db


@app.route('/')
def home():
    user = Client.query.filter_by().first()
    login_user(user)
    return render_template("main.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_client = Client.query.filter_by(email=email).first()
        if existing_client:
            passwords_match = check_password_hash(existing_client.password, password)
            if passwords_match:
                message = "client exist"
                login_user(existing_client, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('home')
                return redirect(next_page)
            else:
                message = "Please check your password"
        else:
            message = "client does not exist"
    return render_template("Login.html", title='log in', message=message, form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        entry = Client(
            full_name=request.form.get('username'),
            email=request.form.get('email'),
            country_code=request.form.get('country_code'),
            phone_no=request.form.get('phone_no'),
            password=generate_password_hash(request.form.get('password'))
            )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("register.html", title='register', form=form)


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    if request.method == 'POST':
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
