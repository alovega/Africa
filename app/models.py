#app/models.py
from sqlalchemy import Sequence
from app import db


class  Bucketlist(db.Model):
    """This class represents the bucketlist table"""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, name):
        """initialise with name"""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __rep__(self):
        return "<Bucketlist: {}>".format(self.name)


class User(db.Model):
        """This class represents the bucketlist table."""

        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True)
        phone_number = db.Column(db.String(32))
        username = db.Column(db.String(100))
        password = db.Column(db.String(100))

        def __init__(self, email, phone_number, username, password):
            self.email = email
            self.phone_number = phone_number
            self.username = username
            self.password = password

        def save(self):
            db.session.add(self)
            db.session.commit()

        @staticmethod
        def get_all():
            return User.query.all()

        def delete(self):
            db.session.delete(self)
            db.session.commit()

        @classmethod
        def find_by_email(cls, email):
            return cls.query.filter_by(email=email).first()

        @classmethod
        def find_by_username(cls, username):
            return cls.query.filter_by(username=username).first()

        def __repr__(self):
            return "<User:(email='%s', phone_number='%s', username='%s', password='%s')>" % (
            self.email, self.phone_number, self.username, self.password)


