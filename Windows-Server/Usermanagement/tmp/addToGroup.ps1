Import-Module ActiveDirectory
$groupDN='CN=Lehrer,OU=Gruppen,DC=schule,DC=local'
Add-ADGroupMember -Identity $groupDN -Members 'CN=Hagmann Christina,OU=Lehrer,OU=Benutzer,DC=schule,DC=local'
