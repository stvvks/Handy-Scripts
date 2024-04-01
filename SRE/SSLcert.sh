#!/bin/bash

DOMAIN="example.com"
NOTIFY_DAYS=30

exp_date=$(echo | openssl s_client -connect $DOMAIN:443 -servername $DOMAIN 2>/dev/null | openssl x509 -noout -dates | grep 'notAfter' | cut -d= -f2)
exp_seconds=$(date -d "$exp_date" +%s)
now_seconds=$(date +%s)
exp_days=$(( ($exp_seconds - $now_seconds) / 86400 ))

echo "The SSL certificate for $DOMAIN expires in $exp_days days."

if [ $exp_days -le $NOTIFY_DAYS ]; then
    echo "The SSL certificate for $DOMAIN is close to expiry. Time to renew."
    # Implement notification mechanism here
fi
