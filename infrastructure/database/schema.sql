CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority INTEGER CHECK(priority >= 1 AND priority <= 5) NOT NULL,
    status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP,
    completion_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,

    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id) ON DELETE CASCADE,

    UNIQUE (task_id, depends_on_task_id),

    CHECK(depends_on_task_id != task_id)
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    action TEXT CHECK(action IN ('created', 'updated', 'deleted', 'status_changed')) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);