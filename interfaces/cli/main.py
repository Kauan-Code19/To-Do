from app.use_cases.create_task import CreateTask
from app.use_cases.list_tasks import ListTasks
from infrastructure.repositories.task_repository import SQLiteTaskRepository
from rich.console import Console
from rich.table import Table
from rich import print

console = Console()

def show_menu():
    print("\n[bold cyan]=== MENU ===[/]")
    print("[green]1[/] - Criar tarefa")
    print("[green]2[/] - Listar tarefas")
    print("[red]0[/] - Sair")

def create_task_flow(use_case: CreateTask):
    title = input("Título: ")
    priority = int(input("Prioridade (1-5): "))
    description = input("Descrição (opcional): ")

    try:
        task = use_case.execute(
            title=title,
            priority=priority,
            description=description or None,
        )

        print(f"Tarefa criada: {task.id}")

    except Exception as e:
        print(f"Erro: {e}")


def list_tasks_flow(use_case):
    tasks = use_case.execute()

    if not tasks:
        console.print("[bold red]Nenhuma tarefa encontrada.[/]")
        return

    table = Table(title="📋 Lista de Tarefas")

    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Título", style="white")
    table.add_column("Prioridade", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Criado em")

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


def main():
    repo = SQLiteTaskRepository()
    create_task = CreateTask(repo)
    list_tasks = ListTasks(repo)

    while True:
        show_menu()

        choice = input("Escolha: ")

        if choice == "1":
            create_task_flow(create_task)

        elif choice == "2":
            list_tasks_flow(list_tasks)

        elif choice == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()
