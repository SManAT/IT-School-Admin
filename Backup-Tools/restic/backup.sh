#!/bin/sh

REPOSITORY=10.0.10.5:/Backups/Webhost
PWDFILE=/root/.ssh/restic.pwd

restic -r sftp:sshUser@$REPOSITORY backup --files-from include.txt --exclude-file exclude.txt -p $PWDFILE -v