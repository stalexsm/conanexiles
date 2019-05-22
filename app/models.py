from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    name = db.Column(db.String(500))
    description = db.Column(db.Text)
    image = db.Column(db.String(500))
    price = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Items %r>' % self.name

    def get_url_image(self):
        """
        метод для формирования адреса картинки
        :return: string
        """
        return 'files/%s' % self.image

    def get_description_for_list(self):
        """
        метод формирования длинны строки для списка товаров.
        :return: string
        """
        if len(self.description) > 52:
            return self.description[:52] + '...'
        return self.description


class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    login = db.Column(db.String(128))
    steam_id = db.Column(db.String(64))
    sum = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer, default=1)
    status = db.Column(db.SmallInteger, default=0)

    def __repr__(self):
        return '<Order %r>' % self.id


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    login = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.steam_id

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        метод для проверки пароля
        :param password: пароль пользователя
        :return: boolean
        """
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
