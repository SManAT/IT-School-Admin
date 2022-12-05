@echo off
echo =============== BACKUP Data with Restic ===============
set ROOTPATH=S:\Backups\Restic-Backup\
set RESTIC=%ROOTPATH%restic_0.14.0_windows_amd64.exe

set REPOSITORY=10.0.10.5:/Backups/PDC
set PWDFILE=%ROOTPATH%restic.pwd
set KEEP=4

rem remove all Keys and load the rquired one
ssh-add -D
ssh-add C:\Users\Administrator\.ssh\Backup@SCHULE.ssh

rem remove locks
%RESTIC% -r sftp:sshUser@%REPOSITORY% unlock --password-file %PWDFILE%

rem backup
%RESTIC% -r sftp:sshUser@%REPOSITORY% backup --files-from include.txt --exclude-file exclude.txt -p %PWDFILE% -v

rem keep n snapshots
%RESTIC% -r sftp:sshUser@%REPOSITORY% forget --keep-last %KEEP% -p %PWDFILE%

rem free space
%RESTIC% -r sftp:sshUser@%REPOSITORY% prune -p %PWDFILE%
