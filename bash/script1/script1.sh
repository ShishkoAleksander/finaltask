#!/bin/bash
su - postgres
psql -d literature -c 'SELECT * FROM articles' > /local/files/articles-3`date +"%Y%m%d%H%M"`.bak
psql -c "\q"
cd /local/files
files=( * )
if [[ ${#files[@]} -gt 3 ]];
then
filename=`ls -1 -t | tail -1`
gzip -f $filename
mv $filename.gz /local/backups/
else
echo "Not enough"
fi
