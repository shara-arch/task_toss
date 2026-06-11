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
            raise ValueError("Error: Invalid credentials profile .")
        if role not in ["client", "tasker"]:
            raise ValueError("Error: Role must be exactly 'client' or 'tasker'.")
        
        db = load_db()
        if name in db["users"]:
            raise KeyError(f"A user named '{name}' already exists.")
            
        db["users"][name] = {"email": email, "role": role}
        save_db(db)
        return cls(name, email, role)