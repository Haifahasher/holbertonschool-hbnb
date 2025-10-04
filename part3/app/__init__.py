#!/usr/bin/python3


from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import config
from app.models.BaseModel import Base

db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()

def create_app(config_name="default"):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    app.config.from_object(config[config_name])
    
    # Enable CORS for frontend integration
    CORS(app, origins=['http://127.0.0.1:5500', 'http://localhost:5500', 'file://'])
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Create database tables
    with app.app_context():
        # Import all models to ensure they are registered
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity
        
        db.create_all()
    
    # Import and register API namespaces
    from app.api.v1.users import api as users_api
    from app.api.v1.amenities import api as amenities_api
    from app.api.v1.places import api as places_api
    from app.api.v1.reviews import api as reviews_api
    import importlib.util
    spec = importlib.util.spec_from_file_location("auth_api", "app/api/v1/auth-login-protection.py")
    auth_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(auth_module)
    auth_api = auth_module.api

    # Add namespaces to the API
    api.add_namespace(users_api, path='/api/v1/users')
    api.add_namespace(amenities_api, path='/api/v1/amenities')
    api.add_namespace(places_api, path='/api/v1/places')
    api.add_namespace(reviews_api, path='/api/v1/reviews')
    api.add_namespace(auth_api, path='/api/v1/auth')

    return app
