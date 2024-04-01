#!/bin/bash

LOG_FILE="/var/log/application.log"
PATTERN="ERROR"

echo "Monitoring $LOG_FILE for occurrences of '$PATTERN'"

tail -fn0 $LOG_FILE | \
while read line ; do
    echo "$line" | grep "$PATTERN" &> /dev/null
    if [ $? = 0 ]; then
        echo "Found an error in the log: $line"
        # Implement alerting mechanism here (e.g., send an email or Slack message)
    fi
done
