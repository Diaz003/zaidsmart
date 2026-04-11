import sqlite3
from pathlib import Path
from typing import Any, Dict, List
import uuid


class AgentRunner:
    def __init__(self, db_path: str = "data/tasks.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = self._connect()
        
        # Tabla de proyectos
        conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de tareas
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE,
                project_id TEXT,
                status TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                description TEXT NOT NULL,
                result TEXT DEFAULT '',
                logs TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        """)
        
        # Migración: Añadir columna project_id si no existe
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(tasks)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'project_id' not in columns:
                conn.execute("ALTER TABLE tasks ADD COLUMN project_id TEXT REFERENCES projects(id) ON DELETE CASCADE")
            if 'progress' not in columns:
                conn.execute("ALTER TABLE tasks ADD COLUMN progress INTEGER DEFAULT 0")
                
            cursor.execute("PRAGMA table_info(projects)")
            proj_columns = [info[1] for info in cursor.fetchall()]
            if 'output_path' not in proj_columns:
                conn.execute("ALTER TABLE projects ADD COLUMN output_path TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass

        conn.commit()
        conn.close()

    # --- CRUD Proyectos ---
    
    def create_project(self, name: str, output_path: str = "") -> str:
        project_id = str(uuid.uuid4())
        conn = self._connect()
        conn.execute(
            "INSERT INTO projects (id, name, output_path) VALUES (?, ?, ?)",
            (project_id, name, output_path)
        )
        conn.commit()
        conn.close()
        return project_id

    def list_projects(self) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.execute("SELECT id, name, created_at, output_path FROM projects ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [{"id": r[0], "name": r[1], "created_at": r[2], "output_path": r[3] or ""} for r in rows]

    def get_project(self, project_id: str) -> Dict[str, Any]:
        conn = self._connect()
        cur = conn.execute("SELECT id, name, created_at, output_path FROM projects WHERE id = ?", (project_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return {}
        return {"id": row[0], "name": row[1], "created_at": row[2], "output_path": row[3] or ""}

    def delete_project(self, project_id: str):
        conn = self._connect()
        # Enable foreign keys for cascade delete
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()

    # --- CRUD Tasks (with project_id) ---

    def create_task(self, task_id: str, project_id: str, agent_name: str, description: str):
        conn = self._connect()
        conn.execute(
            """
            INSERT INTO tasks (task_id, project_id, status, agent_name, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (task_id, project_id, "queued", agent_name, description),
        )
        conn.commit()
        conn.close()

    def update_task(self, task_id: str, status: str, result: str = "", logs: str = "", progress: int = None):
        conn = self._connect()
        if progress is not None:
            conn.execute(
                """
                UPDATE tasks
                SET status = ?, result = ?, logs = ?, progress = ?, updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ?
                """,
                (status, result, logs, progress, task_id),
            )
        else:
            conn.execute(
                """
                UPDATE tasks
                SET status = ?, result = ?, logs = ?, updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ?
                """,
                (status, result, logs, task_id),
            )
        conn.commit()
        conn.close()

    def append_log(self, task_id: str, new_log: str):
        task = self.get_task(task_id)
        current_logs = task.get("logs", "")
        combined = f"{current_logs}\n{new_log}".strip()

        conn = self._connect()
        conn.execute(
            """
            UPDATE tasks
            SET logs = ?, updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ?
            """,
            (combined, task_id),
        )
        conn.commit()
        conn.close()

    def get_task(self, task_id: str) -> Dict[str, Any]:
        conn = self._connect()
        cur = conn.execute(
            """
            SELECT task_id, project_id, status, agent_name, description, result, logs, progress, created_at, updated_at
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,),
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return {}

        return {
            "task_id": row[0],
            "project_id": row[1],
            "status": row[2],
            "agent_name": row[3],
            "description": row[4],
            "result": row[5],
            "logs": row[6],
            "progress": row[7],
            "created_at": row[8],
            "updated_at": row[9],
        }

    def list_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.execute(
            """
            SELECT task_id, project_id, status, agent_name, description, result, logs, progress, updated_at
            FROM tasks
            WHERE project_id = ?
            ORDER BY updated_at DESC
            LIMIT 20
            """,
            (project_id,)
        )
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "task_id": row[0],
                "project_id": row[1],
                "status": row[2],
                "agent_name": row[3],
                "description": row[4],
                "result": row[5],
                "logs": row[6],
                "progress": row[7],
                "updated_at": row[8],
            }
            for row in rows
        ]
