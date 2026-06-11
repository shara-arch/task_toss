import argparse
import sys
from models.user import User
from models.project import Project
from models.task import Task
from utils.persistence import load_db
from rich.console import Console
from rich.table import Table


