from utils.persistence import load_db, save_db

class Project:
    """Represents a Workspace posted by a Client User."""
    def __init__(self, title: str, description: str, due_date: str, owner: str):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner