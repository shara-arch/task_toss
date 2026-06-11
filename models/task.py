from utils.persistence import load_db, save_db

class Task:
    """Represents a unit of work within a Project, assigned to a Tasker."""
    def __init__(self, title: str, project: str, assigned_to: str = None, status: str = "Pending"):
        self.title = title
        self.project = project
        self.assigned_to = assigned_to
        self._status = status