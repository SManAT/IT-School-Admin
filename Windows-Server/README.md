Here are some usefull Script, that I use

- **restoreRechte.py**
  start it inside a directory, with some AD-User data direcrories, e.g.
  ```bash
  h.moser/
  s.davies/
  e.fitzgerald/
  ```
  the script will then get a List of all subdirectories, and will change recursive the Owner
  of all data to **<DOMAIN>\<username>**.  
  h.moser will be owned bei User **\<DOMAIN>\h.moser**  
  s.davies will be owned bei User **<DOMAIN>\s.davies**  
  and so on.

  Will only work, if the directory name is excact the AD-Username (as it is in my environment).

