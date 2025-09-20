#!/usr/bin/python3

from abc import ABC, abstractmethod
from app import db

class Repository(ABC):
    @abstractmethod
    def add(self, instance):
        pass

    @abstractmethod
    def get(self, instance_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, instance_id, data):
        pass

    @abstractmethod
    def delete(self, instance_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attribute_name, attribute_value):
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self.storage = {}

    def add(self, instance):
        self.storage[instance.id] = instance

    def get(self, instance_id):
        return self.storage.get(instance_id)

    def get_all(self):
        return list(self.storage.values())

    def update(self, instance_id, data):
        instance = self.get(instance_id)
        if instance:
            instance.update(data)

    def delete(self, instance_id):
        if instance_id in self.storage:
            del self.storage[instance_id]

    def get_by_attribute(self, attribute_name, attribute_value):
        return next((instance for instance in self.storage.values() if getattr(instance, attribute_name) == attribute_value), None)

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, instance):
        db.session.add(instance)
        db.session.commit()

    def get(self, instance_id):
        return self.model.query.get(instance_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, instance_id, data):
        instance = self.get(instance_id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            db.session.commit()
            return instance
        return None

    def delete(self, instance_id):
        instance = self.get(instance_id)
        if instance:
            db.session.delete(instance)
            db.session.commit()

    def get_by_attribute(self, attribute_name, attribute_value):
        return self.model.query.filter_by(**{attribute_name: attribute_value}).first()
