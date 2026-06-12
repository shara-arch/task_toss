import pytest
import os
import json
from unittest.mock import patch
import utils.persistence
from models.user import User
from models.project import Project
from models.task import Task

# Point data layer interactions safely to an isolated virtual runtime file
TMP_TEST_FILE = os.path.join(os.path.dirname(__file__), "test_storage.json")

@pytest.fixture(autouse=True)
def mock_db_file():
    """Isolates the testing lifecycle environment from production data stores."""
    with patch("utils.persistence.STORAGE_FILE", TMP_TEST_FILE):
        with open(TMP_TEST_FILE, "w") as f:
            json.dump({"users": {}, "projects": {}, "tasks": {}}, f)
        yield
        if os.path.exists(TMP_TEST_FILE):
            os.remove(TMP_TEST_FILE)

def test_user_role_creation_and_constraints():
    """Verifies user generation logic and role type boundaries."""
    # Test valid creation paths
    client_user = User.create("Alice", "alice@hi.com", "client")
    tasker_user = User.create("Bob", "bob@work.com", "tasker")
    
    assert client_user.role == "client"
    assert tasker_user.role == "tasker"
    
    # Assert validation rules block random roles
    with pytest.raises(ValueError):
        User.create("Charlie", "charlie@hi.com", "manager")  # Invalid role type            


def test_role_based_project_creation():
    """Ensures ONLY client accounts are authorized to post project workspaces."""
    User.create("Alice", "alice@hi.com", "client")
    User.create("Bob", "bob@work.com", "tasker")

    # A Client creating a project should pass seamlessly
    project = Project.create("FixSink", "Repair kitchen pipe leaks", "2026-08-15", "Alice")
    assert project.owner == "Alice"

    # A Tasker trying to create a project must throw a PermissionError
    with pytest.raises(PermissionError):
        Project.create("PaintHouse", "Paint walls", "2026-09-01", "Bob")


def test_dual_experience_task_lifecycle():
    """Tracks workflows where a Client creates a task and a Tasker caters to it."""
    # 1. Setup participants and workspace
    User.create("Alice", "alice@hi.com", "client")
    User.create("Bob", "bob@work.com", "tasker")
    Project.create("FixSink", "Repair kitchen pipe leaks", "2026-08-15", "Alice")

    # 2. Client adds an unassigned task
    task = Task.create("ReplacePipe", "FixSink")
    
    db = utils.persistence.load_db()
    assert db["tasks"]["FixSink:ReplacePipe"]["assigned_to"] is None
    assert db["tasks"]["FixSink:ReplacePipe"]["status"] == "Pending"