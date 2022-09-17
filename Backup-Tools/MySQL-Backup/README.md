## MySQL
It is written in Python and you can use it on a Linux Machine.  

First of all you had to install **Python** and all needed **Python modules**.  
After the Installation of Python, open a console in the this directory and run  `pip install .` Now we are ready to go!    

It works with MySQL 5.7>.  
The **Username** and **Password** for mysql ares stored in `mysql.cnf`.  
Be sure to give `mysql.cnf` 400 rights, because there is listed a cleartext password!  
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
The script will also restore the users and their privileges.  
Be aware, that all **databases** and **users** with same name are going to be dropped first!
Also be aware, that **password hashes** may not compatible with a newer MySQL Version!  
