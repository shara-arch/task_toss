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

#Command handler for ADDING TASKS
def handle_add_task(args):
    try:
        task = Task.create(args.title, args.project)
        console.print(f"[bold green] Success! :[/bold green] Open task '{task.title}' added to '{task.project}'")
    except Exception as e:
        console.print(f"[bold red] Operational Error:[/bold red] {e}")         

#Command handler for CLAIMING TASKS
def handle_claim_task(args):
    try:
        Task.claim(args.project, args.title, args.user)
        console.print(f"[bold green] Success! :[/bold green] Tasker '{args.user}' claimed task '{args.title}'!")
    except Exception as e:
        console.print(f"[bold red] Operational Error:[/bold red] {e}")

#Command handler for COMPLETING TASKS
def handle_complete_task(args):
    try:
        Task.complete(args.project, args.title, args.user)
        console.print(f"[bold green] Success!:[/bold green] Task '{args.title}' marked as Completed by {args.user}!")
    except Exception as e:
        console.print(f"[bold red] Operational Error:[/bold red] {e}")        
#Command handler for FETCHING,FORMATTING AND DISPLAYING PROJECTS
def handle_render_projects(args):
    # Loads the entire databaase JSON file into memory
    db = load_db()
    if not db["projects"]:
        #fall back if the dictionary is empty
        console.print("[yellow]No tracked project workspaces detected.[/yellow]")
        return
    #Table initialization
    table = Table(title="TASK TOSSER(Toss that task away!)")
    table.add_column("Project Owner)")
    table.add_column("Target Deadline", )
    table.add_column("Task Assignment Status", width=50)

    for p_title, p_info in db["projects"].items():
        linked_tasks = []
        for t_key, t_info in db["tasks"].items():
            if t_info["project"] == p_title:
                #Status Symbol and Assigment Formatting
                status_symbol = "✔" if t_info["status"] == "Completed" else "⏳"
                assignee = f" Assigned to: {t_info['assigned_to']}" if t_info['assigned_to'] else "⚠️ [bold yellow]UNCLAIMED[/bold yellow]"
                linked_tasks.append(f"[{status_symbol}] {t_info['title']} ({assignee})")
        #joins all the formatted tasks for that project with newlines (\n) so they stack neatly inside the table cell. 
        # If a project has zero tasks, it defaults to a clean [No tasks added yet] placeholder string.
        tasks_str = "\n".join(linked_tasks) if linked_tasks else "[No tasks added yet]"
        table.add_row(f"{p_title} (by {p_info['owner']})", p_info["due_date"], tasks_str)                
        
        #Prints table
        console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Task Tosser: A platform that allows you to toss those pesky taks away.")
    subparsers = parser.add_subparsers(dest="command", required=True)      

    # Command: add-user
    u_parser = subparsers.add_parser("add-user", help="Register a profile.")
    u_parser.add_argument("--name", required=True)
    u_parser.add_argument("--email", required=True)
    u_parser.add_argument("--role", choices=["client", "tasker"], required=True, help="Experience role type.") #(help) used as a userguide when user types --help
    u_parser.set_defaults(func=handle_add_user)        

    # Command: add-project
    p_parser = subparsers.add_parser("add-project", help="Post a project needing assistance (Client Only).")
    p_parser.add_argument("--title", required=True)
    p_parser.add_argument("--user", required=True, help="Your registered Client username.")
    p_parser.add_argument("--desc", default="Help required.")
    p_parser.add_argument("--due", default="2026-12-31")
    p_parser.set_defaults(func=handle_add_project)  

    # Command: add-task
    t_parser = subparsers.add_parser("add-task", help="Add specific tasks to your project (Client Only).")
    t_parser.add_argument("--title", required=True)
    t_parser.add_argument("--project", required=True)
    t_parser.set_defaults(func=handle_add_task)

    # Command: claim-task
    cl_parser = subparsers.add_parser("claim-task", help="Cater to an unclaimed task on the board (Tasker Only).")
    cl_parser.add_argument("--project", required=True)
    cl_parser.add_argument("--title", required=True)
    cl_parser.add_argument("--user", required=True, help="Your registered Tasker username.")
    cl_parser.set_defaults(func=handle_claim_task)

    # Command: complete-task
    cplt_parser = subparsers.add_parser("complete-task", help="Flag a claimed task finished (Assigned Tasker Only).")
    cplt_parser.add_argument("--project", required=True)
    cplt_parser.add_argument("--title", required=True)
    cplt_parser.add_argument("--user", required=True, help="Your registered Tasker username.")
    cplt_parser.set_defaults(func=handle_complete_task)

    # Command: render-projects
    subparsers.add_parser("render-projects", help="View the complete projects table.")
    subparsers.set_defaults(func=handle_render_projects)
    