from models.base import Person
from utils.persistence import load_db, save_db

class User(Person):
    """(Child class of 'Person')"""
    def __init__(self, name: str, email: str, role: str):
        super().__init__(name, email)
        self.role = role