import os
import shutil
from datetime import datetime

def backup_database(db_path, backup_dir):
    today = datetime.now().strftime('%Y-%m-%d')
    backup_path = os.path.join(backup_dir, f"db_backup_{today}.sql")
    # Assuming a PostgreSQL database for the example
    os.system(f"pg_dump your_database_name > {backup_path}")

def backup_files(source_dir, backup_dir):
    today = datetime.now().strftime('%Y-%m-%d')
    destination = os.path.join(backup_dir, f"files_backup_{today}")
    shutil.copytree(source_dir, destination)

backup_database('/path/to/your/database', '/path/to/backup/directory')
backup_files('/path/to/important/files', '/path/to/backup/directory')
