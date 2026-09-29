from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from datetime import datetime, timezone
from extensions import db
from models.models import User, Friend, Message

chat_bp = Blueprint("chat", __name__)


# ── 友達一覧ページ ────────────────────────────────
@chat_bp.route("/friends")
@login_required
def friends():
    return render_template("friends.html")


# ── トーク一覧ページ ──────────────────────────────
@chat_bp.route("/talks")
@login_required
def talks():
    return render_template("talks.html")


# ── チャット画面 ──────────────────────────────────
@chat_bp.route("/chat/<int:friend_id>")
@login_required
def chat(friend_id):
    partner = User.query.get_or_404(friend_id)
    return render_template("chat.html", partner=partner)


# ════════════════════════════════════════════════
#  API エンドポイント
# ════════════════════════════════════════════════

# ── ユーザー検索 API ──────────────────────────────
@chat_bp.route("/api/users/search")
@login_required
def api_search_users():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    users = User.query.filter(
        User.id != current_user.id,
        or_(
            User.nickname.ilike(f"%{q}%"),
            User.user_id.ilike(f"%{q}%"),
        )
    ).limit(20).all()

    result = []
    for u in users:
        # フレンド状態を付与
        friend = Friend.query.filter(
            or_(
                and_(Friend.requester_id == current_user.id, Friend.receiver_id == u.id),
                and_(Friend.requester_id == u.id,           Friend.receiver_id == current_user.id),
            )
        ).first()
        status = friend.status if friend else "none"
        result.append({**u.to_dict(), "friend_status": status})

    return jsonify(result)


# ── 友達申請 API ──────────────────────────────────
@chat_bp.route("/api/friends/request/<int:target_id>", methods=["POST"])
@login_required
def api_friend_request(target_id):
    if target_id == current_user.id:
        return jsonify({"error": "自分自身には送れません"}), 400

    exists = Friend.query.filter(
        or_(
            and_(Friend.requester_id == current_user.id, Friend.receiver_id == target_id),
            and_(Friend.requester_id == target_id,       Friend.receiver_id == current_user.id),
        )
    ).first()
    if exists:
        return jsonify({"error": "既に申請済みまたは友達です"}), 400

    f = Friend(requester_id=current_user.id, receiver_id=target_id)
    db.session.add(f)
    db.session.commit()
    return jsonify({"ok": True})


# ── 申請承認 API ──────────────────────────────────
@chat_bp.route("/api/friends/accept/<int:requester_id>", methods=["POST"])
@login_required
def api_friend_accept(requester_id):
    f = Friend.query.filter_by(
        requester_id=requester_id, receiver_id=current_user.id, status="pending"
    ).first_or_404()
    f.status = "accepted"
    db.session.commit()
    return jsonify({"ok": True})


# ── 友達一覧 API ──────────────────────────────────
@chat_bp.route("/api/friends")
@login_required
def api_friends():
    rows = Friend.query.filter(
        or_(
            and_(Friend.requester_id == current_user.id, Friend.status == "accepted"),
            and_(Friend.receiver_id  == current_user.id, Friend.status == "accepted"),
        )
    ).all()

    result = []
    for r in rows:
        partner = r.receiver if r.requester_id == current_user.id else r.requester
        result.append(partner.to_dict())
    return jsonify(result)


# ── 受信済み申請一覧 API ──────────────────────────
@chat_bp.route("/api/friends/pending")
@login_required
def api_friends_pending():
    rows = Friend.query.filter_by(receiver_id=current_user.id, status="pending").all()
    return jsonify([r.requester.to_dict() for r in rows])


# ── トーク一覧 API ────────────────────────────────
@chat_bp.route("/api/talks")
@login_required
def api_talks():
    """最後のメッセージと相手情報を返す"""
    uid = current_user.id
    # 有効期限内メッセージのみ
    now = datetime.now(timezone.utc)
    msgs = Message.query.filter(
        or_(Message.sender_id == uid, Message.receiver_id == uid),
        Message.expires_at > now,
    ).order_by(Message.created_at.desc()).all()

    seen = {}
    for m in msgs:
        partner_id = m.receiver_id if m.sender_id == uid else m.sender_id
        if partner_id not in seen:
            partner = User.query.get(partner_id)
            unread = Message.query.filter_by(
                receiver_id=uid, sender_id=partner_id, is_read=False
            ).count()
            seen[partner_id] = {
                "partner":    partner.to_dict(),
                "last_msg":   m.body[:40],
                "last_at":    m.created_at.isoformat(),
                "unread":     unread,
            }
    return jsonify(list(seen.values()))


# ── メッセージ取得 API ────────────────────────────
@chat_bp.route("/api/messages/<int:partner_id>")
@login_required
def api_messages(partner_id):
    uid = current_user.id
    now = datetime.now(timezone.utc)
    msgs = Message.query.filter(
        or_(
            and_(Message.sender_id == uid,       Message.receiver_id == partner_id),
            and_(Message.sender_id == partner_id, Message.receiver_id == uid),
        ),
        Message.expires_at > now,
    ).order_by(Message.created_at.asc()).all()

    # 既読更新
    Message.query.filter_by(
        sender_id=partner_id, receiver_id=uid, is_read=False
    ).update({"is_read": True})
    db.session.commit()

    return jsonify([m.to_dict() for m in msgs])
