#!/bin/bash

echo `date`
cd e-menu/
docker exec API bash -c 'python /opt/python/app/email_cron.py'
echo "Finish mail send"
