from app.extensions import db

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="available")  # available, reserved, adopted
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # для брони/усыновления