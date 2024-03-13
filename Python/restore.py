import os
import subprocess
import psycopg2

def restore_postgresql(database_url, backup_file):
    # Use pg_restore to restore the database from the backup file
    command = f"pg_restore --no-owner --dbname={database_url} {backup_file}"
    subprocess.run(command, shell=True)

    print(f"Restore completed successfully from {backup_file}")

if __name__ == "__main__":
    # Replace 'YOUR_DATABASE_URL' with the actual PostgreSQL database URL
    database_url = os.environ.get("DATABASE_URL", "YOUR_DATABASE_URL")

    # Replace 'BACKUP_FILE' with the path to the backup file you want to restore
    backup_file = os.environ.get("BACKUP_FILE", "/path/to/backup.sql")

    # Restore the database
    restore_postgresql(database_url, backup_file)
