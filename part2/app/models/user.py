#!/usr/bin/python3


from app.models.base_model import BaseModel
import re


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

class User(BaseModel):
    """User Class"""

    def __init__(self, id, first_name, last_name, email, is_admin=False):
        """init"""
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("Usually it doesn't exceed 50 characters..")
        if not last_name or len(last_name) > 50:
            raise ValueError("Usually it doesn't exceed 50 characters..")
        if not EMAIL_REGEX.match(email):
            raise ValueError("Are you sure you've written your email correctly?")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.is_admin = bool(is_admin)
