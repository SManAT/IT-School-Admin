#Set UTF-8-----------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#Admin Privileges----------------
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
Write  'Running PS with Administrator Rights'
#Run as Admin--------------------

$User = "{% username %}"
$strPass = ConvertTo-SecureString -String "{% password %}" -AsPlainText -Force
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ($User, $strPass)

#Test Credidentals---------------
<#PSScriptInfo  
.DESCRIPTION  
    Simulates an Authentication Request in a Domain envrionment using a PSCredential Object. Returns $true if both Username and Password pair are valid.  
.VERSION  
    1.3 
.GUID  
    6a18515f-73d3-4fb4-884f-412395aa5054  
.AUTHOR  
    Thomas Malkewitz @dotps1  
.TAGS  
    PSCredential, Credential 
.RELEASENOTES  
    Updated $Domain default value to $Credential.GetNetworkCredential().Domain. 
    Added support for multipul credential objects to be passed into $Credential. 
.PROJECTURI 
    http://dotps1.github.io 
 #> 
 
Function Validate-Credential { 
    [OutputType([Bool])] 
     
    Param ( 
        [Parameter( 
            Mandatory = $true, 
            ValueFromPipeLine = $true, 
            ValueFromPipelineByPropertyName = $true 
        )] 
        [Alias( 
            'PSCredential' 
        )] 
        [ValidateNotNull()] 
        [System.Management.Automation.PSCredential] 
        [System.Management.Automation.Credential()] 
        $Credential, 
 
        [Parameter()] 
        [String] 
        $Domain = $Credential.GetNetworkCredential().Domain 
    ) 
 
    Begin { 
        [System.Reflection.Assembly]::LoadWithPartialName("System.DirectoryServices.AccountManagement") | 
            Out-Null 
 
        $principalContext = New-Object System.DirectoryServices.AccountManagement.PrincipalContext( 
            [System.DirectoryServices.AccountManagement.ContextType]::Domain, $Domain 
        ) 
    } 
 
    Process { 
        foreach ($item in $Credential) { 
            $networkCredential = $Credential.GetNetworkCredential() 
             
            Write-Output -InputObject $( 
                $principalContext.ValidateCredentials( 
                    $networkCredential.UserName, $networkCredential.Password 
                ) 
            ) 
        } 
    } 
 
    End { 
        $principalContext.Dispose() 
    } 
} 
Validate-Credential $Credential
#Test Credidentals---------------

Start-Sleep -s 2

#Rename and Join
Add-Computer -Domain "{% domain %}" -ComputerName "{% oldhostname %}" -Credential $Credential

Start-Sleep -s 2
