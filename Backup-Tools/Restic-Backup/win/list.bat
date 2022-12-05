@echo off
set ROOTPATH=S:\Backups\Restic-Backup\
set RESTIC=%ROOTPATH%restic_0.14.0_windows_amd64.exe

set REPOSITORY=10.0.10.5:/Backups/PDC
set PWDFILE=%ROOTPATH%restic.pwd

%RESTIC% -r sftp:sshUser@%REPOSITORY% snapshots -p %PWDFILE%

