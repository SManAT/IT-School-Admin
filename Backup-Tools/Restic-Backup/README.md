# Restic
```bash
Restic is a fast and secure backup program. In the following sections, we will present typical workflows,  
starting with installing, preparing a new repository, and making the first backup.
```
see [Restic Documentation](https://restic.readthedocs.io/en/stable/)

# Example

Be sure to have an *SSH key pair* for an User, that will use restic for *sftp* operations.

## Linux
see `backup.sh` for an example. The Restic password is hardcoded in `restic.pwd` with root:root 400.  
Create a cron job or a Timer Unit to schedule the backup.

## Windows
the same on Windows, see `backup.bat`. The Restic password is hardcoded in `restic.pwd` with readonly rights.  
Create a job to schedule the backup.  