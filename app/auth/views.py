from flask import render_template, redirect, url_for, flash, request
from . import auth, forms
from app.models import db, User
from flask_login import login_required, login_user, logout_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Не верно введен логин или пароль.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, login=form.login.data, steam_id=form.steam_id.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрировались')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('main.index'))


