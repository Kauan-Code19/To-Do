from app.use_cases.services.log_service import LogService
from app.use_cases.task.create_task import CreateTask
from app.use_cases.task.list_tasks import ListTasks
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
    print("[yellow]3[/] - List logs")
    print("[red]0[/] - Exit")


def create_task_flow(use_case: CreateTask):
    title = input("Title: ")
    priority = int(input("Priority (1-5): "))
    description = input("Description (optional): ")

    try:
        task = use_case.execute(
            title=title,
            priority=priority,
            description=description or None,
        )

        print(f"[green]Task created:[/] {task.id}")

    except Exception as e:
        print(f"[red]Error:[/] {e}")


def list_tasks_flow(use_case: ListTasks):
    tasks = use_case.execute()

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
    logs = service.list_logs()

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


def main():
    sqlite_task_repo = SQLiteTaskRepository()
    create_task = CreateTask(sqlite_task_repo)
    list_tasks = ListTasks(sqlite_task_repo)

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
            list_logs_flow(log_service)

        elif choice == "0":
            print("[red]Exiting...[/]")
            break

        else:
            print("[red]Invalid option[/]")


if __name__ == "__main__":
    main()