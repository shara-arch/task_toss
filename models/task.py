from utils.persistence import load_db, save_db

class Task:
    """Represents a unit of work within a Project, assigned to a Tasker."""
    def __init__(self, title: str, project: str, assigned_to: str = None, status: str = "Pending"):
        self.title = title
        self.project = project
        self.assigned_to = assigned_to
        self._status = status

    @classmethod
    def create(cls, title: str, project: str) -> "Task":
        """Allows a Client to add an unassigned task to their project."""
        db = load_db()
        if project not in db["projects"]:
            raise KeyError(f"Project : '{project}' does not exist.")

        task_key = f"{project}:{title}"
        if task_key in db["tasks"]:
            raise KeyError(f"Task '{title}' already exists inside this project.")
        
        #  Save new tesk to db
        db["tasks"][task_key] = {
            "title": title,
            "project": project,
            "assigned_to": None,  # Spawns empty, waiting for a Tasker
            "status": "Pending"
        }
        save_db(db)
        return cls(title, project)
    
    @classmethod
    def claim(cls, project: str, title: str, tasker_name: str):
        """Allows a Tasker to attend to the task by claiming it."""
        db = load_db()
        if tasker_name not in db["users"]:
            raise KeyError(f"User '{tasker_name}' does not exist.")
