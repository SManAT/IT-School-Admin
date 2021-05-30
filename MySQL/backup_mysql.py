import subprocess
import os

print("Hallo")
--single-transaction uses a consistent read and guarantees that data seen by mysqldump does not change.

Backup in single Files

for DB in $(mysql - u root - p mysqlmaster - e 'show databases' - s - -skip-column-names)
do
mysqldump $DB > "$DB.sql"
done
