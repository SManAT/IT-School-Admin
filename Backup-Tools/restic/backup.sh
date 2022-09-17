#!/bin/sh
REPOSITORY=10.0.10.5:/Backups/Webhost
PWDFILE=/root/.ssh/restic.pwd

restic -r sftp:sshUser@$REPOSITORY backup --files-from include.txt --exclude-file exclude.txt -p $PWDFILE -v

# keep n snapshots
restic -r sftp:sshUser@$REPOSITORY forget --keep-last  4 -p $PWDFILE

# free space
restic -r sftp:sshUser@$REPOSITORY prune --keep-last  4 -p $PWDFILE