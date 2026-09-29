from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt, login_mgr
from models.models import User

auth_bp = Blueprint("auth", __name__)


@login_mgr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ── 登録 ─────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("chat.friends"))

    if request.method == "POST":
        nickname = request.form.get("nickname", "").strip()
        user_id  = request.form.get("user_id", "").strip()
        password = request.form.get("password", "").strip()

        if not nickname or not user_id or not password:
            flash("すべての項目を入力してください", "error")
            return render_template("register.html")

        if User.query.filter_by(user_id=user_id).first():
            flash("そのIDはすでに使われています", "error")
            return render_template("register.html")

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        user   = User(nickname=nickname, user_id=user_id, password=hashed)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("chat.friends"))

    return render_template("register.html")


# ── ログイン ─────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("chat.friends"))

    if request.method == "POST":
        user_id  = request.form.get("user_id", "").strip()
        password = request.form.get("password", "").strip()
        user     = User.query.filter_by(user_id=user_id).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("chat.friends"))

        flash("IDまたはパスワードが違います", "error")

    return render_template("login.html")


# ── ログアウト ────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
