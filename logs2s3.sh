#!/bin/bash
DATE=`date "+%b %e %I:%M:%S"`
ANO=`date +%Y`
MES=`date +%m`
DIA=`date +%d`
BUCKET="the-name-of-the-bucket"
RUTA_DESTINO="$ANO/$MES/$DIA"
HOSTNAME="/bin/hostname"
HOST="`$HOSTNAME`"
SERVICE="logs"
OPTIONS="--acl bucket-owner-full-control --region eu-west-1 --sse"
RUTA="/var/log/"
AWS="/usr/bin/aws"

for file in `find -L $RUTA -ctime -1 -name "*-*.gz"`
do
	$AWS s3 cp $file s3://$BUCKET/$RUTA_DESTINO/$HOST/$SERVICE/ $OPTIONS >> /var/log/cron 2>&1
        if [ $? -gt 0 ]; then
            echo "$DATE $HOST [CROND] An ERROR occured uploading log $file to s3. Backups cannot be completed" >> /var/log/cron
            exit 1
        else
                echo "$DATE $HOST [CROND] Log $file succesfully uploaded to s3" >> /var/log/cron
                rm -f $file
        fi
done
exit 0
