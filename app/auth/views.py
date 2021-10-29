from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from app.forms import LoginForm
from flask_login import login_user, login_required, logout_user
from . import auth
from app.firestore_service import get_user, put_user
from app.models import UserData, UserModel
from werkzeug.security import generate_password_hash

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if password_from_db == password:
                user_data = UserData(username,password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bon Dia')
                return redirect(url_for('hello'))

            else:
                flash('La información es incorrecta')

        return redirect(url_for("index"))

    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username,password_hash)
            put_user(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Benvenuto')
            return redirect(url_for('hello'))

        else:
            flash('El usuario ya existe')

    return render_template('signup.html', **context)
