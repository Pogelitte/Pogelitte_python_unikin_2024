from celery import shared_task
from datetime import datetime
import subprocess
import os

@shared_task(bind=True, max_retries=3)
def backup_database(self):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{now}.sql"
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, filename)

    # Récupération sécurisée des variables
    user = os.environ.get('POSTGRES_USER')
    host = os.environ.get('DB_HOST')
    db = os.environ.get('POSTGRES_DB')
    password = os.environ.get('POSTGRES_PASSWORD')

    if not all([user, host, db, password]):
        return f"Backup failed: Missing one or more environment variables (POSTGRES_USER, DB_HOST, POSTGRES_DB, POSTGRES_PASSWORD)"

    command = [
        "pg_dump", "-U", user, "-h", host, "-d", db, "-f", backup_path
    ]

    try:
        subprocess.run(
            command,
            check=True,
            env={**os.environ, "PGPASSWORD": password}
        )
        return f"Backup success: {backup_path}"

    except subprocess.CalledProcessError as e:
        try:
            self.retry(exc=e, countdown=10)
        except Exception:
            return f"Backup retry failed after 3 attempts: {e}"
    except Exception as e:
        return f"Backup failed: {e}"
