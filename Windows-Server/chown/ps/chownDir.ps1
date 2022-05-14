# get ACL Object
$ACL = Get-ACL "%PATH%"
$Group = New-Object System.Security.Principal.NTAccount("%USER%")
$ACL.SetOwner($Group)
# set Owner of File
Set-Acl -Path "%PATH%" -AclObject $ACL
