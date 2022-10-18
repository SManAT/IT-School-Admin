$Path = $PSScriptRoot
Copy-Item -Path "$Path\wallpapers" -Destination "$Env:AppData\wallpapers" -Recurse -Force
