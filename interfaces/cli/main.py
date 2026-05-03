from rich.progress import Task

from app.use_cases.services.log_service import LogService
from app.use_cases.task.create_task import CreateTask
from app.use_cases.task.list_tasks import ListTasks
from app.use_cases.task.update_task import UpdateTask
from app.use_cases.task.update_task import UpdateTask
from domain.entities.log import Log
from domain.enums.task_status import TaskStatus
from infrastructure.repositories.sqllite_log_repository import SQLiteLogRepository
from infrastructure.repositories.sqllite_task_repository import SQLiteTaskRepository
from rich.console import Console
from rich.table import Table
from rich import print

console = Console()

def show_menu():
    print("\n[bold cyan]=== MENU ===[/]")
    print("[green]1[/] - Create task")
    print("[green]2[/] - List tasks")
    print("[green]3[/] - Update task")
    print("[yellow]4[/] - List logs")
    print("[red]0[/] - Exit")


def create_task_flow(use_case: CreateTask):
    title = input("Title: ")
    priority = int(input("Priority (1-5): "))
    description = input("Description (optional): ")

    try:
        task: Task = use_case.execute(
            title=title,
            priority=priority,
            description=description or None,
        )

        print(f"[green]Task created:[/] {task.id}")

    except Exception as e:
        print(f"[red]Error:[/] {e}")


def list_tasks_flow(use_case: ListTasks):
    tasks: list[Task] = use_case.execute()

    if not tasks:
        console.print("[bold red]No tasks found.[/]")
        return

    table = Table(title="📋 Task List")

    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title", style="white")
    table.add_column("Priority", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Created at")

    status_colors = {
        "pending": "yellow",
        "in_progress": "blue",
        "completed": "green",
    }

    for task in tasks:
        status = task.status.value
        color = status_colors.get(status, "white")

        table.add_row(
            str(task.id),
            task.title,
            str(task.priority),
            f"[{color}]{status}[/]",
            str(task.created_date),
        )

    console.print(table)


def list_logs_flow(service: LogService):
    logs: list[Log] = service.list_logs()

    if not logs:
        console.print("[bold red]No logs found.[/]")
        return

    table = Table(title="📋 Log List")

    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Task ID", style="white", justify="right")
    table.add_column("Action", style="magenta")
    table.add_column("Date", style="green")

    for log in logs:
        table.add_row(
            str(log.id),
            str(log.task_id),
            log.action,
            str(log.date),
        )

    console.print(table)
    
def update_task_flow(update_use_case: UpdateTask, list_use_case: ListTasks):
    list_tasks_flow(list_use_case)

    task_id = int(input("\nEnter task ID to update: "))
    
    title = input("New title (enter to skip): ")
    priority = input("New priority (enter to skip): ")
    description = input("New description (enter to skip): ")
    status_input = input(f"New status ({TaskStatus.PENDING.value}/{TaskStatus.IN_PROGRESS.value}/{TaskStatus.COMPLETED.value}): ")

    status = None
    if status_input:
        try:
            status = TaskStatus(status_input)
        except ValueError:
            console.print("[red]Invalid status[/]")
            return

    task: Task = update_use_case.execute(
        task_id=task_id,
        title=title or None,
        priority=int(priority) if priority else None,
        description=description or None,
        status=TaskStatus(status) if status else None
    )
    
    console.print("\n[green]Task updated successfully![/]\n")

    table = Table(title="✅ Updated Task")

    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title")
    table.add_column("Priority", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Created at")

    status_colors = {
        "pending": "yellow",
        "in_progress": "blue",
        "completed": "green",
    }

    status_value = task.status.value
    color = status_colors.get(status_value, "white")

    table.add_row(
        str(task.id),
        task.title,
        str(task.priority),
        f"[{color}]{status_value}[/]",
        str(task.created_date),
    )

    console.print(table)

def main():
    sqlite_task_repo = SQLiteTaskRepository()
    create_task = CreateTask(sqlite_task_repo)
    list_tasks = ListTasks(sqlite_task_repo)
    update_task = UpdateTask(sqlite_task_repo)

    sqlite_log_repo = SQLiteLogRepository()
    log_service = LogService(sqlite_log_repo)

    while True:
        show_menu()

        choice = input("Choose an option: ")

        if choice == "1":
            create_task_flow(create_task)

        elif choice == "2":
            list_tasks_flow(list_tasks)

        elif choice == "3":
            update_task_flow(update_task, list_tasks)

        elif choice == "4":
            list_logs_flow(log_service)

        elif choice == "0":
            print("[red]Exiting...[/]")
            break

        else:
            print("[red]Invalid option[/]")


if __name__ == "__main__":
    main()