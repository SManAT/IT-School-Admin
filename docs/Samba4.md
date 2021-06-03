## Samba4
`restore_Rechte.pl` is a Perl script, that will *chown* home directories after a backup.
You can also use it within a *profile* folder, if you
are using roaming profiles. Therefor also directories like moser.V2, moser.V4 etc
will be renamed.
The script also deletes the files ntuser\.(dat|ini|pol)+, which will be created at next login.
The rights are
- 770 for profile directories
- 2770 for user directories
- and each file within theses directories 770

Imagin that file structure after a backup.

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
/PDC/mozart.V6    | mozart.V6\:users

## Samba4/LDIF
`getPolicies.sh` is a bash script, that loads from the subdir *private* (which is the
`/var/lib/samba/private directory`) all GPO entries from the database. The LDIF entries will
then be saved in the file *Policies.ldif*.
In case of a backup, you can use these Ldif File to update your LDAP Tree. After that,
you can copy back your GPO's from your backup to `/var/lib/samba/sysvol/....`  

## Samba4/DNS
hier you have a script to inject static IP adresses into the LDAP Tree.
- First, modify the Administrator Password inside `staticIP.exp` (its an expect file!, `apt install expect`).
- Second, modify `staticIP.cfg` with all your static IP's.
- Last, execute `./staticIP.exp`


## Samba4/Usermanagement
Here are some PerlScripts to manage Users within Samba4.  
`MySamba4-AddGroup.pl`  
`MySamba4-DelUser.pl`  
`MySamba4-RenameUsers.pl`  
`MySamba4-ImportExportCSV.pl`  
The most scripts are self explaining.