import argparse
import sys
from models.user import User
from models.project import Project
from models.task import Task
from utils.persistence import load_db
from rich.console import Console #Used to make the Comand line visually appealing
from rich.table import Table #Will be used to print table of projects/taks

console = Console()
#Command handler for CREATING USERS
def handle_add_user(args):
    try:
        user = User.create(args.name, args.email, args.role)
        console.print(f"[bold green] Success! :[/bold green]Created profile for {user} ")
    except Exception as e:
        console.print(f"[bold red] Operational Error:[/bold red] {e}")

#Command handler for ADDING PROJECTS
def handle_add_project(args):
    try:
        project = Project.create(args.title, args.desc, args.due, args.user)
        console.print(f"[bold green] Success! :[/bold green] Client '{project.owner}' posted project '{project.title}'")
    except Exception as e:
        console.print(f"[bold red] Operational Error:[/bold red] {e}")
