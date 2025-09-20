#!/usr/bin/python3


from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    """User-specific repository with additional methods"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email):
        """Get user by email"""
        return self.get_by_attribute('email', email.lower())
    
    def email_exists(self, email):
        """Check if email already exists"""
        return self.get_by_email(email) is not None
