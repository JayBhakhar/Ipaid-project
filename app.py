from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/user'
db = SQLAlchemy(app)


class Client(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20), primary_key=False)
    email = db.Column(db.String(20), primary_key=False)
    country_code = db.Column(db.String(3), primary_key=False)
    phone_no = db.Column(db.String(10), primary_key=False)
    password = db.Column(db.String(20), primary_key=False)



@app.route('/')
def Home():
    return render_template("main.html")


@app.route('/login')
def login():
    return render_template("Login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        fullname = request.form.get('full_name')
        email = request.form.get('email')
        country_code = request.form.get('country_code')
        phone = request.form.get('phone')
        password = request.form.get('password')
        add_entry = Client(full_name=fullname, email=email, country_code=country_code, phone_no=phone,
                           password=password)
        db.session.add(add_entry)
        db.session.commit()
    return render_template("register.html")


app.run(debug=True)
