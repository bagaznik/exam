from flask import Blueprint, request, render_template
from app.models.user import User
from app.extensions import db
from flask import redirect, url_for, flash
from flask_login import logout_user

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            flash("Email обязателен!")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Пользователь с таким именем уже существует")
            return redirect(url_for("auth.register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация успешна")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


from flask_login import login_user

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()  # или email=email
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            flash("Неверные данные для входа")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")





@bp.route("/logout")
def logout():
    logout_user()  # разлогиниваем пользователя
    flash("Вы вышли из аккаунта")
    return redirect(url_for("auth.login"))  # обязательно возвращаем редирект