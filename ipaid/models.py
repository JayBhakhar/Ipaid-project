from datetime import datetime
from flask_login import UserMixin,LoginManager
from ipaid import db, app


login_manager = LoginManager()
login = LoginManager(app)
login_manager.init_app(app)

class Client(db.Model, UserMixin):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=True)
    country_code = db.Column(db.String(3), nullable=True)
    phone_no = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"Client('{self.full_name}', '{self.email}', '{self.country_code}', '{self.phone_no}', '{self.password}')"


class Event(db.Model, UserMixin):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(20), nullable=True)
    event_place = db.Column(db.String(20), nullable=True)
    message = db.Column(db.String(3), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_type = db.Column(db.String(10), nullable=True)
    no_of_peoples = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"Event('{self.event_name}', '{self.event_place}', '{self.message}', '{self.event_type}', '{self.no_of_peoples}')"


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))