#!/usr/bin/python3


import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime

class BaseModel:
    """Base model class with common attributes"""
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """updates updated_at whenever object is modified"""
        from app import db
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def update(self, data):
        """updates attributes of object based on provided dict"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convert object to dictionary for JSON serialization"""
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif hasattr(value, 'to_dict'):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
            else:
                result[key] = value
        return result

    def __repr__(self):
        """String representation of the object"""
        return f"<{self.__class__.__name__} {self.id}>"
