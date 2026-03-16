```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Instrument, Cart, Order

api = Blueprint('api', __name__)

# Authentication
@api.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'msg': 'Missing username, email or password'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'msg': 'Username already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'User created successfully'}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': 'Invalid username or password'}), 401

    if user.password != password:
        return jsonify({'msg': 'Invalid username or password'}), 401

    return jsonify({'msg': 'Logged in successfully'}), 200

# Instruments
@api.route('/instruments', methods=['GET'])
def get_instruments():
    instruments = Instrument.query.all()
    return jsonify([{'id': i.id, 'name': i.name, 'description': i.description, 'price': i.price} for i in instruments]), 200

@api.route('/instruments/<int:instrument_id>', methods=['GET'])
def get_instrument(instrument_id):
    instrument = Instrument.query.get(instrument_id)
    if not instrument:
        return jsonify({'msg': 'Instrument not found'}), 404

    return jsonify({'id': instrument.id, 'name': instrument.name, 'description': instrument.description, 'price': instrument.price}), 200

@api.route('/instruments', methods=['POST'])
@jwt_required()
def create_instrument():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not name or not description or not price:
        return jsonify({'msg': 'Missing name, description or price'}), 400

    new_instrument = Instrument(name=name, description=description, price=price)
    db.session.add(new_instrument)
    db.session.commit()

    return jsonify({'msg': 'Instrument created successfully'}), 201

@api.route('/instruments/<int:instrument_id>', methods=['PUT'])
@jwt_required()
def update_instrument(instrument_id):
    instrument = Instrument.query.get(instrument_id)
    if not instrument:
        return jsonify({'msg': 'Instrument not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if name:
        instrument.name = name
    if description:
        instrument.description = description
    if price:
        instrument.price = price

    db.session.commit()

    return jsonify({'msg': 'Instrument updated successfully'}), 200

@api.route('/instruments/<int:instrument_id>', methods=['DELETE'])
@jwt_required()
def delete_instrument(instrument_id):
    instrument = Instrument.query.get(instrument_id)
    if not instrument:
        return jsonify({'msg': 'Instrument not found'}), 404

    db.session.delete(instrument)
    db.session.commit()

    return jsonify({'msg': 'Instrument deleted successfully'}), 200

# Cart
@api.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': c.id, 'instrument_id': c.instrument_id, 'quantity': c.quantity} for c in cart]), 200

@api.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    instrument_id = data.get('instrument_id')
    quantity = data.get('quantity')

    if not instrument_id or not quantity:
        return jsonify({'msg': 'Missing instrument_id or quantity'}), 400

    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id, instrument_id=instrument_id).first()
    if cart:
        cart.quantity += quantity
    else:
        new_cart = Cart(user_id=user_id, instrument_id=instrument_id, quantity=quantity)
        db.session.add(new_cart)

    db.session.commit()

    return jsonify({'msg': 'Instrument added to cart successfully'}), 201

@api.route('/cart/<int:cart_id>', methods=['PUT'])
@jwt_required()
def update_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({'msg': 'Cart not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    quantity = data.get('quantity')

    if quantity:
        cart.quantity = quantity

    db.session.commit()

    return jsonify({'msg': 'Cart updated successfully'}), 200

@api.route('/cart/<int:cart_id>', methods=['DELETE'])
@jwt_required()
def delete_from_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({'msg': 'Cart not found'}), 404

    db.session.delete(cart)
    db.session.commit()

    return jsonify({'msg': 'Instrument removed from cart successfully'}), 200

# Orders
@api.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    instrument_id = data.get('instrument_id')
    quantity = data.get('quantity')

    if not instrument_id or not quantity:
        return jsonify({'msg': 'Missing instrument_id or quantity'}), 400

    user_id = get_jwt_identity()
    new_order = Order(user_id=user_id, instrument_id=instrument_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'msg': 'Order created successfully'}), 201
```

####