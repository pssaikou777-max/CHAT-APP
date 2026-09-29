import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, bcrypt
from models.models import User, Message, Friend

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin1234")


def _admin_required():
    """管理者セッションチェック。未認証なら True を返す（リダイレクト用）"""
    return not session.get("is_admin")


# ── 管理者ログイン ────────────────────────────────
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_admin"):
        return redirect(url_for("admin.users"))

    if request.method == "POST":
        pwd = request.form.get("password", "").strip()
        if pwd == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin.users"))
        flash("パスワードが違います", "error")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin.login"))


# ── ユーザー一覧 ──────────────────────────────────
@admin_bp.route("/users")
def users():
    if _admin_required():
        return redirect(url_for("admin.login"))

    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


# ── ユーザー削除 ──────────────────────────────────
@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    if _admin_required():
        return redirect(url_for("admin.login"))

    user = User.query.get_or_404(user_id)
    # 関連データも削除
    Message.query.filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).delete()
    Friend.query.filter(
        (Friend.requester_id == user_id) | (Friend.receiver_id == user_id)
    ).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f"ユーザー「{user.nickname}」を削除しました", "success")
    return redirect(url_for("admin.users"))


# ── パスワードリセット ─────────────────────────────
@admin_bp.route("/users/<int:user_id>/reset", methods=["POST"])
def reset_password(user_id):
    if _admin_required():
        return redirect(url_for("admin.login"))

    user     = User.query.get_or_404(user_id)
    new_pass = request.form.get("new_password", "").strip()
    if not new_pass:
        flash("新しいパスワードを入力してください", "error")
        return redirect(url_for("admin.users"))

    user.password = bcrypt.generate_password_hash(new_pass).decode("utf-8")
    db.session.commit()
    flash(f"「{user.nickname}」のパスワードをリセットしました", "success")
    return redirect(url_for("admin.users"))
