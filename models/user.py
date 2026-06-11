from models.base import Person
from utils.persistence import load_db, save_db

class User(Person):
    """(Child class of 'Person')"""
    def __init__(self, name: str, email: str, role: str):
        super().__init__(name, email)
        self.role = role

        
    @classmethod
    def create(cls, name: str, email: str, role: str) -> "User":
        if not name or "@" not in email:
            raise ValueError("Invalid credentials profile template.")
        if role not in ["client", "tasker"]:
            raise ValueError("Role must be exactly 'client' or 'tasker'.")