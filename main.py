from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
import unittest
from app import create_app
from app.forms import LoginForm

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.route("/")
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("/hello"))
    session["user_ip"] = user_ip

    return response


@app.route("/hello", methods=["GET", "POST"])
def hello():
    todos = {
        "Comprar café",
        "Hacer tarea lenguajes formales",
        "Acabar de documentar homework recollector",
    }

    user_ip = session.get("user_ip")
    login_form = LoginForm()
    username = session.get("username")

    context = {
        "todos": todos,
        "user_ip": user_ip,
        'login_form': login_form,
        'username': username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito!')

        return redirect(url_for("index"))

    return render_template("hello.html", **context)
