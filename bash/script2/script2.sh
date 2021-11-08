#!/bin/bash
pid_file=/var/run/script2.pid

#Ensuring a Single Instance of an Application
if [ -f $pid_file ]; then
  echo "Found existing .pid file named $pid_file. Exiting."
  exit
else
  echo "Creating .pid file $pid_file"
  echo $$ > $pid_file
fi

cd /local/backups
SIZE=`du -B 1 /local/backups | awk '{ print $1 }'`
files=( * )

if [[ ${#files[@]} -gt 3 ]];
then
total=`ls -l | wc -l`
lines=`expr $total - 1`
 echo "Directory /local/backups has ${lines} files"  | sendmail root
else
echo "Directory /local/backups has less than 3 files"
fi

if [[ $SIZE -gt 20480 ]];
then
   echo "Directory /local/backups has ${SIZE} bytes"  | sendmail root
else
echo "Size of directory /local/backups is less than 20480 bytes"
fi
