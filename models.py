from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Drone(db.Model):
    # Existing fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(255), nullable=False)

    # Relationship to votes
    votes = db.relationship('Vote', backref='drone', lazy=True)

    def __repr__(self):
        return f"<Drone {self.name}>"


class Motor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(255), nullable=False)

    # Relationship to votes
    votes = db.relationship('Vote', backref='motor', lazy=True)

    def __repr__(self):
        return f"<Motor {self.name}>"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Can be associated with a user, for now it can be a guest cart (user_id=None)
    user_id = db.Column(db.Integer, nullable=True)  # Guest users will have None as user_id
    created_at = db.Column(db.DateTime, default=db.func.now())

    cart_items = db.relationship('CartItem', backref='cart', lazy=True)

    def __repr__(self):
        return f"<Cart {self.id}>"


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    drone = db.relationship('Drone', backref='cart_items', lazy=True)

    def __repr__(self):
        return f"<CartItem {self.drone.name}, Quantity: {self.quantity}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200))
    hobbies = db.Column(db.String(200))
    job = db.Column(db.String(100))
    skill = db.Column(db.String(100))
    purchases = db.relationship('Purchase', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    date_of_purchase = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Purchase('{self.item_name}', '{self.item_price}')"


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Link vote to a user
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Link vote to a product
    rating = db.Column(db.Integer, nullable=False)  # Rating (1-5)
    comment = db.Column(db.String(255), nullable=True)  # Optional comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp

    user = db.relationship('User', backref='votes', lazy=True)
    product = db.relationship('Product', backref='votes', lazy=True)

    def __repr__(self):
        return f"<Vote User: {self.user_id}, Product: {self.product_id}, Rating: {self.rating}>"


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)  # Rating stars
    comment = db.Column(db.String(255), nullable=True)  # Optional comment