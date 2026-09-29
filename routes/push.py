import os, json
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.models import PushSubscription

push_bp = Blueprint("push", __name__)

VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_PUBLIC_KEY  = os.environ.get("VAPID_PUBLIC_KEY", "")
VAPID_CLAIMS      = {"sub": "mailto:admin@freechat.app"}


@push_bp.route("/api/push/vapid-public-key")
@login_required
def vapid_public_key():
    return jsonify({"publicKey": VAPID_PUBLIC_KEY})


@push_bp.route("/api/push/subscribe", methods=["POST"])
@login_required
def subscribe():
    data     = request.get_json()
    endpoint = data["endpoint"]
    p256dh   = data["keys"]["p256dh"]
    auth     = data["keys"]["auth"]

    sub = PushSubscription.query.filter_by(
        user_id=current_user.id, endpoint=endpoint
    ).first()
    if not sub:
        sub = PushSubscription(
            user_id=current_user.id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
        )
        db.session.add(sub)
    else:
        sub.p256dh = p256dh
        sub.auth   = auth
    db.session.commit()
    return jsonify({"ok": True})


@push_bp.route("/api/push/unsubscribe", methods=["POST"])
@login_required
def unsubscribe():
    data = request.get_json()
    PushSubscription.query.filter_by(
        user_id=current_user.id, endpoint=data["endpoint"]
    ).delete()
    db.session.commit()
    return jsonify({"ok": True})


def send_push(user_id: int, title: str, body: str, url: str = "/"):
    """指定ユーザーの全デバイスにWeb Push通知を送る"""
    if not VAPID_PRIVATE_KEY:
        return
    from pywebpush import webpush, WebPushException
    subs = PushSubscription.query.filter_by(user_id=user_id).all()
    payload = json.dumps({"title": title, "body": body, "url": url})
    for sub in subs:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {"p256dh": sub.p256dh, "auth": sub.auth},
                },
                data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS,
            )
        except WebPushException:
            # 無効なサブスクリプションは削除
            db.session.delete(sub)
    db.session.commit()
