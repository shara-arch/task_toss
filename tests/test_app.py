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