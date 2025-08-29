#!/usr/bin/python3
from flask import Blueprint
from flask_restx import Api
from .v1.reviews import api as reviews_ns

api_bp = Blueprint("api", __name__)
api = Api(api_bp, title="HBnB API", version="1.0", doc="/docs")

api.add_namespace(reviews_ns, path="/api/v1/reviews")
