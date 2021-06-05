## MySQL
It works with MySQL 5.7>.  
The **Username** and **Password** for mysql ares stored in `mysql.cnf`.    
You configure the behavor in `config.yaml`
```yaml
# where to store the Backups, for realtive path start with ./ or ../
backupPath: ./DB_BACKUP
# how many Backups schould be in the rotate Process
versions: 2
```
The backup will be a Tarball of all databases.

## MySQL/Backup
`MySQLBackup.py` will help you to create mysqldumps of all of your databases.  
Just run `MySQLBackup.py`.  
You will get a Backup in a ***.tar.bzip2** file.

## MySQL/Restore
Just run `MySQLRestore.py`.  
It will also restore the users and their privileges.  
Be aware, that all **databases** and **users** with same name are going to be dropped first!
