Import-Module ActiveDirectory
$groupDN='%GRUPPE%'
Add-ADGroupMember -Identity $groupDN -Members '%USERNAMEDN%'
