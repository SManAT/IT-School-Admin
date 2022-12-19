# changeWallpaper

It is written in Python, and will load wallpapers SFTP or a local directory.
If using SFTP, an offline Copy from all wallpapers will be saved to the host.

Why SFTP?  
Because i had massive problem to get network share working right on windows.  
I'm a Linux nerd, so take SFTP ...

## Installing OpenSSH Server on Windows Server
Go to *Apps und Features* > *Optionale Features* …. and install the OpenSSH Server.
- Create a User to connect with to SSH
- Create a chrooted directory somewhere. The user above, must have read rights (no need to write)
- edit *%ProgramData%/ssh/sshd_config* and configure `ChrootDirectory C:\Users\admin\Downloads\SFTP-DataDir` (example)
- then restart SSH `net stop sshd` and `net start sshd`


## Installation & Configuration

- Copy the program to a preferred location. Then run `pip install .` to get all needed modules.  

- Edit configuration in `config.yaml`
  ```bash
  config:
    # if set, then we use a Network Share for loading wallpapers
    # otherwise, we use a path relative to script dir
    USE_SFTP: 1
    # local path to wallpapers
    LOCAL_PATH: wallpapers\
    # where to store the wallpapers from sftp
    LOCAL_STORAGE: tmp\
    LAST: 26.jpg
    sftp:
      # sftp hostname from server
      HOSTNAME: toolbox
      # path on sftp server
      PATH: wallpapers
      # sftp User
      USER: 
      # hash the password with --encrypt Parameter
      PWD: 
  ```

# Create Standalone Application
You can pack Python to the Application if you build it with `python setup_cx.py build_exe`.

# Start inside Active Domain
Create a GPO to start the file `startWallpaperChanger.bat`
