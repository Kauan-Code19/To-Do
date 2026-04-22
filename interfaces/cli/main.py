from app.use_cases.create_task import CreateTask
from infrastructure.repositories.task_repository import SQLiteTaskRepository


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

def main():
    repo = SQLiteTaskRepository()
    create_task = CreateTask(repo)

    while True:
        print("\n=== MENU ===")
        print("1 - Criar tarefa")
        print("0 - Sair")

        choice = input("Escolha: ")

        if choice == "1":
            create_task_flow(create_task)

        elif choice == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()