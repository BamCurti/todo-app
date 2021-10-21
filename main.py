from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "SUPER SECRETO"

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Enviar')

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
