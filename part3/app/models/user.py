#!/usr/bin/python3


from app.models.BaseModel import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from datetime import datetime
import uuid
import re

bcrypt = Bcrypt()
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

class User(BaseModel):
    """User Class"""
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        """Initialize user with validation"""
        super().__init__(**kwargs)
        
        if not first_name or len(first_name) > 50:
            raise ValueError("Usually it doesn't exceed 50 characters..")
        if not last_name or len(last_name) > 50:
            raise ValueError("Usually it doesn't exceed 50 characters..")
        if not EMAIL_REGEX.match(email):
            raise ValueError("Are you sure you've written your email correctly?")
        if password and len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.is_admin = bool(is_admin)
        
        if password:
            self.set_password(password)

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def password(self):
        """Password property - should not be accessible"""
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password using set_password method"""
        self.set_password(password)

    # Relationships
    places = relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
