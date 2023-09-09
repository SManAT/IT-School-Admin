param([switch]$Elevated)
function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
    $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}
if ((Test-Admin) -eq $false)  {
    if ($elevated) {
        # tried to elevate, did not work, aborting
    } else {
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    }
    exit
}

'Running with full privileges ....'

$User = "{% username %}"
$strPass = ConvertTo-SecureString -String "{% password %}" -AsPlainText -Force
$UserCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ($User, $strPass)
Connect-AzureAD -Credential $UserCredential

