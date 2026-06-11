import argparse
import sys
from models.user import User
from models.project import Project
from models.task import Task
from utils.persistence import load_db
from rich.console import Console #Used to make the Comand line visually appealing
from rich.table import Table #Will be used to print table of projects/taks

console = Console()
#Command handler for creating users
def handle_add_user(args):
    try:
        user = User.create(args.name, args.email, args.role)
        console.print(f"[bold green] Success !:Created profile for {user}[/bold green] ")
    except Exception as e:
        console.print(f"[bold red] Operational Error:[/bold red] {e}")
