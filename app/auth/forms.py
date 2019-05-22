from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, EqualTo, Email
from wtforms import ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={"placeholder": "Введите email"},
                        validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Пароль', render_kw={"placeholder": "Введите пароль"},
                             validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('Email', render_kw={"placeholder": "Введите email"},
                        validators=[DataRequired(), Email(), Length(1, 64)])
    login = StringField('Ник в игре', render_kw={"placeholder": "Введите ник как в игре"}, validators=[DataRequired(), Length(1, 64)])
    steam_id = StringField('Идентификатор steam', render_kw={"placeholder": "Введите steam_id"}, validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Пароль', render_kw={"placeholder": "Введите пароль"},
                             validators=[DataRequired(), EqualTo('password2', message='пароли не совпадают')])
    password2 = PasswordField('Повторите пароль', render_kw={"placeholder": "Введите пароль еще раз"},
                              validators=[DataRequired()])

    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
