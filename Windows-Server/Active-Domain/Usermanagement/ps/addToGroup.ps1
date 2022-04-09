Import-Module ActiveDirectory
Add-ADGroupMember -Identity %GRUPPE% -Members %USERNAME%
