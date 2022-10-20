# changeWallpaper

It is written in Python, and will load wallpapers from a Network-Share or a local directory.

See Configuration in `config.yaml`
```bash
config:
  # if set, then we use a Network Share for loading wallpapers
  # otherwise, we use a path relative to script dir
  USE_SHARE: 0
  SHARE: \\<server>\wallpapers
  PATH: wallpapers\
```

