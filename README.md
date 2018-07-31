
# Samba4-Admin
Provides some (that is what i think) usefull scripts for managing a Samba4 Server.
Data available in these subfolders
- Usermanagement
- System
- Backup


# Prerequisites
The most Tools are written in Perl, so you had to install some libraries. Here are the steps

```
/* CPAN History & CPAN – Perl Docs */
apt-get install libterm-readline-gnu-perl perl-doc

cpan -i Bundle::CPAN

cpan -i YAML Term::ReadLine::Perl HTTP::Date Getopt::Std Getopt::Long  
Linux::usermod File::Basename Text::CSV Net::Ping DBI DBD::mysql Config::IniFiles 
Data::Dumper File::Spec::Unix File::Find::Rule Log::Log4perl
```

## Backup
`samba_backup` is the original script from samba4 Team, that was slightly modified by me.
It creates tarballs from `/etc/samba/`, `/var/lib/samba/private` and `/var/lib/samba/sysvol`.

`restore_Rechte.pl` is a Perl script, that will *chown* home directories after a backup.
Imaging that file structure after a backup.

name        | owner          
------------ | -------------
/home/moser       | root\:root
/home/sepp        | root\:root
/home/mozart      | root\:root

The script will use the name from the directory and will do the *chown* stuff

name        | owner          
------------ | -------------
/home/moser       | moser\:users
/home/sepp        | sepp\:users
/home/mozart      | mozart\:users

## Usermanagement

## System
