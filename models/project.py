from utils.persistence import load_db, save_db

class Project:
    """Represents a Workspace posted by a Client User."""
    def __init__(self, title: str, description: str, due_date: str, owner: str):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner
        
    @classmethod
    def create(cls, title: str, description: str, due_date: str, owner: str) -> "Project":
        db = load_db()
        if owner not in db["users"]:
            raise KeyError(f"User '{owner}' was not found.")
        
        # Enforce Role-Based Access Control: Only clients can create projects
        if db["users"][owner]["role"] != "client":
            raise PermissionError(f"Access Denied: '{owner}' is a tasker and cannot post projects.")
            
        if title in db["projects"]:
            raise KeyError(f"Project workspace '{title}' already exists.")        