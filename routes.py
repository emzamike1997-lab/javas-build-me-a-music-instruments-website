```python
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import User, Product, Cart, Order, OrderItem
from . import db
import stripe

stripe.api_key = 'YOUR_STRIPE_API_KEY'

ecommerce = Blueprint('ecommerce', __name__)

@ecommerce.route('/register', methods=['POST'])
def register():
    """Register user"""
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@ecommerce.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({'message': 'User logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@ecommerce.route('/products', methods=['GET'])
def get_products():
    """Get products"""
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image_url': product.image_url} for product in products]), 200

@ecommerce.route('/cart', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def cart():
    """Cart operations"""
    if request.method == 'GET':
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        return jsonify([{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]), 200
    elif request.method == 'POST':
        data = request.get_json()
        cart_item = Cart(user_id=current_user.id, product_id=data['product_id'], quantity=data['quantity'])
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to cart successfully'}), 201
    elif request.method == 'PUT':
        data = request.get_json()
        cart_item = Cart.query.filter_by(id=data['id']).first()
        cart_item.quantity = data['quantity']
        db.session.commit()
        return jsonify({'message': 'Cart item updated successfully'}), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        cart_item = Cart.query.filter_by(id=data['id']).first()
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Cart item deleted successfully'}), 200

@ecommerce.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """Checkout"""
    data = request.get_json()
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum([item.product.price * item.quantity for item in cart_items])
    order = Order(user_id=current_user.id, total=total)
    db.session.add(order)
    db.session.commit()
    for item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.product.price)
        db.session.add(order_item)
        db.session.commit()
    try:
        charge = stripe.Charge.create(
            amount=int(total * 100),
            currency='usd',
            source=data['stripeToken'],
            description='Music Instruments Order'
        )
        return jsonify({'message': 'Order placed successfully'}), 200
    except stripe.error.CardError as e:
        return jsonify({'message': 'Card error'}), 400
    except stripe.error.RateLimitError as e:
        return jsonify({'message': 'Rate limit error'}), 429
    except stripe.error.InvalidRequestError as e:
        return jsonify({'message': 'Invalid request error'}), 400
    except Exception as e:
        return jsonify({'message': 'Error occurred'}), 500
```

###