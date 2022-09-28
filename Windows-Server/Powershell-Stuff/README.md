Powershell Stuff

- **StoreCredidential.ps1**
  Stores User Credidentials in a Txt File encrypted.  
  Only the user that has created this file can decrypt it! So you can't it even copy to another maschine!

- **GetCredidential.ps1**
  Decrypt the File Content from script `StoreCredidential.ps1`

- **Create_Backup_task.ps1**
  Create a schedulded task with Powershell. It will use the encrypted credidentials from script `StoreCredidential.ps1`.


  

