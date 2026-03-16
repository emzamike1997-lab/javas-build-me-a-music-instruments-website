```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from routes import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_instruments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
```

### Running the API
1. Create a new virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
3. Install the required packages: `pip install -r requirements.txt`
4. Create the database: `python`
```python
from app import db
db.create_all()
```
5. Run the API: `python app.py`

### Testing the API
You can use a tool like Postman or cURL to test the API endpoints. Make sure to include the `Content-Type` header with a value of `application/json` when sending JSON data in the request body.

Example requests:

* Register a new user: `POST /auth/register` with JSON body `{"username": "john", "email": "john@example.com", "password": "password"}`
* Login an existing user: `POST /auth/login` with JSON body `{"username": "john", "password": "password"}`
* Get a list of all instruments: `GET /instruments`
* Get a specific instrument: `GET /instruments/1`
* Create a new instrument: `POST /instruments` with JSON body `{"name": "Guitar", "description": "A musical instrument", "price": 100.0}`
* Update an existing instrument: `PUT /instruments/1` with JSON body `{"name": "Updated Guitar", "description": "An updated musical instrument", "price": 150.0}`
* Delete an instrument: `DELETE /instruments/1`
* Get the current user's cart: `GET /cart`
* Add an instrument to the current user's cart: `POST /cart` with JSON body `{"instrument_id": 1, "quantity": 2}`
* Update the quantity of an instrument in the current user's cart: `PUT /cart/1` with JSON body `{"quantity": 3}`
* Remove an instrument from the current user's cart: `DELETE /cart/1`
* Create a new order: `POST /orders` with JSON body `{"instrument_id": 1, "quantity": 2}`