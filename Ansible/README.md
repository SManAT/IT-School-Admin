# Ansible for schools

![Galaxy](https://github.com/SManAT/IT-School-Admin/blob/master/Ansible/img/AnsiblePower.png)

## What it is

Will provide automatic install case for Windows Clients with the power of Red Hat's [Ansible](https://www.ansible.com/).  
The playbooks are grouped by _packages_, in Order to simplify customization.

(see image)

# Installation

## Linux Side - Server Node

```bash
apt install python3 python3-pip
pip3 install ansible pywinrm requests-credssp jmespath
```

see also **install/Linux/setup.py**

## Windows Side

see [Ansible - Winrm Guide](https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html)

### Configure Ansible Listener

```ps
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

powershell.exe -ExecutionPolicy ByPass -File $file -EnableCredSSP -Verbose
```

### Set the authentication method

```ps
Set-Item -Path WSMan:\localhost\Service\Auth\credSSP -Value $true

# enables CredSSP authentication on the client
Enable-WSManCredSSP -Role "Server"
```

That's it!

## How to use?

## Where to find other roles?

see [Ansible Galaxy](https://galaxy.ansible.com/)

# List of roles

Global variables are taken from _vars/global_vars.yml_. If they are not defined, role variables will be used.

## some usefull roles

- collect  
  Collect some data from Client, e.g.

```bash
Manufacturer: Dell Inc.
Model: Latitude 5310
Name: DESKTOP-VFEQ5BI
SystemType: x64-based PC
SystemFamily: Latitude
```

## base-package.yml

- elevateAnsibleUser  
  Elevates the User to Administrator and hides the user from Login Screen.
- createUsers  
  Create Administrators and some default Users.
- chocolaty  
  Be sure chocolaty is on client.

## coder-package

- node_yarn_sass
  - vscodium
  - netbeans
  - mysqlworkbench
