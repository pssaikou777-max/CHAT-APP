import os
from flask import Flask, redirect, url_for, request
from extensions import db, login_mgr, bcrypt, socketio
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.push import push_bp

BASE_DIR = os.path.dirname(__file__)

# 本番(Render)は DATABASE_URL 環境変数を使用、開発はSQLite
def _db_url():
    url = os.environ.get("DATABASE_URL", "")
    if url.startswith("postgres://"):          # Render は postgres:// を返す場合がある
        url = url.replace("postgres://", "postgresql://", 1)
    return url or f"sqlite:///{os.path.join(BASE_DIR, 'chat.db')}"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"]              = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    app.config["SQLALCHEMY_DATABASE_URI"] = _db_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 本番は gevent、開発は threading
    async_mode = "gevent" if os.environ.get("RENDER") else "threading"

    db.init_app(app)
    login_mgr.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode=async_mode)

    login_mgr.login_view = "auth.login"

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(push_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    # sw.js に "/" スコープを許可するヘッダーを付与
    @app.after_request
    def add_sw_header(response):
        if "/static/sw.js" in response.headers.get("Content-Location", "") or \
           request.path == "/static/sw.js":
            response.headers["Service-Worker-Allowed"] = "/"
        return response

    with app.app_context():
        db.create_all()

    return app


# ── Socket.IO イベント ────────────────────────────
from flask_socketio import join_room, leave_room, emit
from flask_login import current_user
from models.models import User, Message
from extensions import db as _db
from datetime import datetime, timezone

app = create_app()


@socketio.on("join")
def on_join(data):
    room = _room_name(data["my_id"], data["partner_id"])
    join_room(room)


@socketio.on("send_message")
def on_send_message(data):
    sender_id   = data["sender_id"]
    receiver_id = data["receiver_id"]
    body        = data["body"].strip()
    if not body:
        return

    msg = Message(sender_id=sender_id, receiver_id=receiver_id, body=body)
    _db.session.add(msg)
    _db.session.commit()

    room = _room_name(sender_id, receiver_id)
    emit("new_message", msg.to_dict(), to=room)

    # Web Push通知（受信者がチャット画面を開いていない場合も届く）
    sender = User.query.get(sender_id)
    from routes.push import send_push
    send_push(
        user_id=receiver_id,
        title=f"{sender.nickname} からメッセージ",
        body=body[:80],
        url=f"/chat/{sender_id}",
    )


@socketio.on("read_messages")
def on_read_messages(data):
    """チャット画面を開いた側が既読にする"""
    reader_id = data["reader_id"]
    sender_id = data["sender_id"]

    updated = Message.query.filter_by(
        sender_id=sender_id, receiver_id=reader_id, is_read=False
    ).all()
    for m in updated:
        m.is_read = True
    _db.session.commit()

    if updated:
        room = _room_name(reader_id, sender_id)
        emit("messages_read", {"reader_id": reader_id}, to=room)


def _room_name(a, b):
    return f"room_{min(a,b)}_{max(a,b)}"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
