from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

# User model (for authentication)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # New profile fields
    address = db.Column(db.String(255), nullable=True)  
    contact = db.Column(db.String(50), nullable=True)   
    # Relationships
    wishlist_items = db.relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")
    santa_gifts = db.relationship("GiftLock", foreign_keys="GiftLock.santa_id", back_populates="santa", cascade="all, delete-orphan")
    child_gifts = db.relationship("GiftLock", foreign_keys="GiftLock.child_id", back_populates="child", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Wishlist model
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    gift_name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    model_version = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    amazon_link = db.Column(db.String(300), nullable=True)

    # Relationships
    user = db.relationship("User", back_populates="wishlist_items")
    gift_locks = db.relationship("GiftLock", back_populates="gift", cascade="all, delete-orphan")

# Gift Locking model
class GiftLock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    santa_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    gift_id = db.Column(db.Integer, db.ForeignKey("wishlist.id"), nullable=False)
    revealed = db.Column(db.Boolean, default=False) 
    # Relationships
    santa = db.relationship("User", foreign_keys=[santa_id], back_populates="santa_gifts")
    child = db.relationship("User", foreign_keys=[child_id], back_populates="child_gifts")
    gift = db.relationship("Wishlist", back_populates="gift_locks")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    santa_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    task = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    # Relationships
    santa = db.relationship("User", foreign_keys=[santa_id], backref="tasks_given")
    child = db.relationship("User", foreign_keys=[child_id], backref="tasks_received")