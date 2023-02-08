#Set UTF-8-----------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#Admin Privileges----------------
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
Write  'Running PS with Administrator Rights'
#Run as Admin--------------------

$rootpath = (Get-Item -Path ".\" -Verbose).FullName

echo "Liste aller installierten Apps mit Get-AppxPackage -AllUsers | Select Name, PackageFullName > $rootpath\AppsListINSTALLED.txt"

Get-AppxPackage -AllUsers | Select Name, PackageFullName >"AppsListINSTALLED.txt"
$file = Get-Content "AppsListINSTALLED.txt"
#leeres Array
$AppsList = @()
$Forbidden=@("Microsoft.Windows.CloudExperienceHost","Microsoft.AAD.BrokerPlugin","Microsoft.AccountsControl","Microsoft.BioEnrollment",
"Microsoft.LockApp","Microsoft.MicrosoftEdge","Microsoft.Windows.ContentDeliveryManager","Microsoft.Windows.ParentalControls",
"Microsoft.Windows.ShellExperienceHost","Microsoft.XboxGameCallable","Microsoft.XboxIdentityProvider","Windows.ContactSupport",
"windows.immersivecontrolpanel","Windows.MiracastView","Windows.PrintDialog","Windows.PurchaseDialog","windows.devicesflow",
"Microsoft.WindowsFeedback","Microsoft.Windows.Cortana","Microsoft.Windows.SecureAssessmentBrowser","Microsoft.Windows.SecondaryTileExperience",
"Microsoft.Windows.Apprep.ChxApp","Microsoft.PPIProjection","Microsoft.Windows.AssignedAccessLockApp")
$i=1
$k=0;

ForEach ($line in $file){
  #die Header Zeilen umgehen
  if($k -ge 3){
    #Split am Leerzeichen
    $parts = $line -split "\s+"
    ForEach ($item in $parts){
      if($item.Trim().length -gt 0){
        if($i % 2 -eq 1){
          echo "$i $item"
          #Die Systemweiten Apps nicht nehmen caseintensive
          $found = $false
		  ForEach($f in $Forbidden){
		    If ($item.ToLower().Contains($f.ToLower()) ){
		      $found = $true
		      break		      
		    }
		  }
		  if($found -eq $false){
		    $AppsList = $AppsList + $item
		  }
        }
        $i++
      }
    }
  }
  $k++
}
echo "Alle Apps die installiert sind (siehe Auflistung)"
$AppsList = $AppsList + "*Microsoft.Windows.Cortana*"
$AppsList = $AppsList + "*messaging*"
$AppsList = $AppsList + "*sway*"
$AppsList = $AppsList + "*commsphone*"
$AppsList = $AppsList + "*windowsphone*"
$AppsList = $AppsList + "*phone*"
$AppsList = $AppsList + "*communicationsapps*"
$AppsList = $AppsList + "*people*"
$AppsList = $AppsList + "*zunemusic*"
$AppsList = $AppsList + "*zunevideo*"
$AppsList = $AppsList + "*zune*"
$AppsList = $AppsList + "*bingfinance*"
$AppsList = $AppsList + "*bingnews*"
$AppsList = $AppsList + "*bingsports*"
$AppsList = $AppsList + "*bingweather*"
$AppsList = $AppsList + "*bing*"
$AppsList = $AppsList + "*onenote*"
$AppsList = $AppsList + "*alarms*"
$AppsList = $AppsList + "*calculator*"
$AppsList = $AppsList + "*camera*"
$AppsList = $AppsList + "*photos*"
$AppsList = $AppsList + "*maps*"
$AppsList = $AppsList + "*soundrecorder*"
$AppsList = $AppsList + "*xbox*"
$AppsList = $AppsList + "*solitaire*"
$AppsList = $AppsList + "*officehub*"
$AppsList = $AppsList + "*skypeapp*"
$AppsList = $AppsList + "*getstarted*"
$AppsList = $AppsList + "*3dbuilder*"
$AppsList = $AppsList + "*windowsstore*"

ForEach ($App in $AppsList)
{  
  $Packages = Get-AppxPackage | Where-Object {$_.Name -eq $App}
  if ($Packages -ne $null){
    echo "Removing Appx Package: $App"
    foreach ($Package in $Packages) { Remove-AppxPackage -package $Package.PackageFullName }
  }
  else { echo "Unable to find package: $App" }

  $ProvisionedPackage = Get-AppxProvisionedPackage -online | Where-Object {$_.displayName -eq $App}
  if ($ProvisionedPackage -ne $null){
    echo "Removing Appx Provisioned Package: $App"
	remove-AppxProvisionedPackage -online -packagename $ProvisionedPackage.PackageName
  }
  else { echo "Unable to find provisioned package: $App" }
}
