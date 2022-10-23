# changeWallpaper

It is written in Python, and will load wallpapers from a Network-Share or a local directory.
If using a Share, an offline Copy from all wallpapers will be saved to the host.

## Installation & Configuration

- Copy the program to a preferred location. Then run `pip install .` to get all needed modules.  

- Edit configuration in `config.yaml`
  ```bash
  config:
    # if set, then we use a Network Share for loading wallpapers
    # otherwise, we use a path relative to script dir
    USE_SHARE: 1
    # local path to wallpapers
    LOCAL_PATH: wallpapers\
    # where to store the wallpapers
    LOCAL_STORAGE: tmp\
    
    share:
      PATH: \\<server>\Public\wallpapers
      # if USER and PWS is set to NONE, no credidentials will be used
      USER: None
      # hash the password with --encrypt Parameter
      PWD: None
  ```

# Create Standalone Application

You can pack Python to the Application if you build it with `python setup_cx.py build_exe`.
