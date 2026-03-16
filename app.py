```python
from flask import Flask
from .routes import ecommerce
from .models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/dbname'
db.init_app(app)
app.register_blueprint(ecommerce)

if __name__ == '__main__':
    app.run(debug=True)
```

###