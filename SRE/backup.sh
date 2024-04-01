#!/bin/bash

BACKUP_SRC="/var/www/html"
BACKUP_DEST="/mnt/backup"
DATE=$(date +%Y-%m-%d)
BACKUP_NAME="backup-$DATE.tar.gz"

echo "Starting backup of $BACKUP_SRC to $BACKUP_NAME"

# Create a compressed backup
tar -czf $BACKUP_DEST/$BACKUP_NAME $BACKUP_SRC

echo "Backup completed successfully!"
