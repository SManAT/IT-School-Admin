# Change Owner with Powershell

It is written in Python, and just executes Powershell on the fly.  

First of all you had to install **Python** and all needed **Python modules**.  
After the Installation of Python, open a console in the this directory and run  `pip install .`  

Now we are ready to go!

## Usage
```bash
chown -u DOMAIN\User -t <targetfile or targetdirectory>
```
if you target a directory, than it will change the Owner recursive!  