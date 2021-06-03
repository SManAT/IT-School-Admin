## MySQL
## MySQL/Backup
`MySQLBackup.py` will help you to create mysqldumps of all of your databases.  
You configure the behavor in `config.yaml`
```yaml
# where to store the Backups, for realtive path start with ./ or ../
backupPath: ./DB_BACKUP
# how many Backups schould be in the rotate Process
versions: 2
```
The backup will be a Tarball of all databases.

## MySQL/Restore