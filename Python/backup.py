import os
import subprocess
import datetime
import psycopg2

def backup_postgresql(database_url, backup_directory):
    # Generate a timestamp for the backup file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_directory, f"backup_{timestamp}.sql")

    # Use pg_dump to create a backup
    command = f"pg_dump {database_url} > {backup_file}"
    subprocess.run(command, shell=True)

    print(f"Backup completed successfully. Backup file: {backup_file}")

if __name__ == "__main__":
    # Replace 'YOUR_DATABASE_URL' with the actual PostgreSQL database URL
    database_url = os.environ.get("DATABASE_URL", "YOUR_DATABASE_URL")

    # Replace 'BACKUP_DIRECTORY' with the desired backup directory
    backup_directory = os.environ.get("BACKUP_DIRECTORY", "/path/to/backups")

    # Create the backup
    backup_postgresql(database_url, backup_directory)
