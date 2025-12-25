from datetime import datetime
from app.extensions import db

class AdoptionRequest(db.Model):
    __tablename__ = "adoption_request"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)
    message = db.Column(db.Text, nullable=True)  # Сообщение пользователя
    status = db.Column(db.String(20), default="pending")  # pending / approved / rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="adoption_requests")
    animal = db.relationship("Animal", backref="adoption_requests")

