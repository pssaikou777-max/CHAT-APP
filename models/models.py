from datetime import datetime, timezone, timedelta
from flask_login import UserMixin
from extensions import db

# 1ヶ月後の期限を返すデフォルト関数
def _one_month_later():
    return datetime.now(timezone.utc) + timedelta(days=30)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id       = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(30), nullable=False)
    user_id  = db.Column(db.String(30), unique=True, nullable=False)   # ログインID
    password = db.Column(db.String(255), nullable=False)               # bcryptハッシュ
    is_admin   = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # 送信メッセージ
    sent_messages     = db.relationship("Message", foreign_keys="Message.sender_id",    back_populates="sender",   lazy="dynamic")
    # フレンド申請（申請者側）
    friend_requests   = db.relationship("Friend",  foreign_keys="Friend.requester_id",  back_populates="requester", lazy="dynamic")
    # フレンド申請（受信者側）
    friend_received   = db.relationship("Friend",  foreign_keys="Friend.receiver_id",   back_populates="receiver",  lazy="dynamic")

    def to_dict(self):
        return {"id": self.id, "nickname": self.nickname, "user_id": self.user_id}


class Friend(db.Model):
    __tablename__ = "friends"

    id           = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # pending / accepted / blocked
    status       = db.Column(db.String(10), default="pending", nullable=False)
    created_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    requester = db.relationship("User", foreign_keys=[requester_id], back_populates="friend_requests")
    receiver  = db.relationship("User", foreign_keys=[receiver_id],  back_populates="friend_received")

    __table_args__ = (
        db.UniqueConstraint("requester_id", "receiver_id", name="uq_friend_pair"),
    )


class Message(db.Model):
    __tablename__ = "messages"

    id         = db.Column(db.Integer, primary_key=True)
    sender_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id= db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    body       = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # 1ヶ月後に期限切れ
    expires_at = db.Column(db.DateTime, default=_one_month_later)
    is_read    = db.Column(db.Boolean, default=False)

    sender   = db.relationship("User", foreign_keys=[sender_id],   back_populates="sent_messages")

    def to_dict(self):
        return {
            "id":          self.id,
            "sender_id":   self.sender_id,
            "receiver_id": self.receiver_id,
            "body":        self.body,
            "created_at":  self.created_at.isoformat(),
            "is_read":     self.is_read,
        }


class PushSubscription(db.Model):
    __tablename__ = "push_subscriptions"

    id       = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    endpoint = db.Column(db.Text, nullable=False)
    p256dh   = db.Column(db.Text, nullable=False)
    auth     = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", foreign_keys=[user_id])

    __table_args__ = (
        db.UniqueConstraint("user_id", "endpoint", name="uq_user_endpoint"),
    )
