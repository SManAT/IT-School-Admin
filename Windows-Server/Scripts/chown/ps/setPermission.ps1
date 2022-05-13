$path = "%PATH%" 
$user = "%USER%" 
$Rights = "FullControl"
# Controls how permissions are inherited by children
# ContainerInherit, None, ObjectInherit
$InheritSettings = "ContainerInherit, ObjectInherit" 
# Usually set to none but can setup rules that only apply to children.
$PropogationSettings = "None" 
# Allow or Deny
$RuleType = "Allow" 

$acl = Get-Acl $path
$perm = $user, $Rights, $InheritSettings, $PropogationSettings, $RuleType
$rule = New-Object -TypeName System.Security.AccessControl.FileSystemAccessRule -ArgumentList $perm
$acl.SetAccessRule($rule)
$acl | Set-Acl -Path $path

# List of Rights
# AppendData 	Specifies the right to append data to the end of a file.
# ChangePermissions 	Specifies the right to change the security and audit rules associated with a file or folder.
# CreateDirectories 	Specifies the right to create a folder.
# CreateFiles 	Specifies the right to create a file.
# Delete 	Specifies the right to delete a folder or file.
# DeleteSubdirectoriesAndFiles 	Specifies the right to delete a folder and any files contained within that folder.
# ExecuteFile 	Specifies the right to run an application file.
# FullControl 	Specifies the right to exert full control over a folder or file, and to modify access control and audit rules. This value represents the right to do anything with a file and is the combination of all rights in this enumeration.
# ListDirectory 	Specifies the right to read the contents of a directory.
# Modify 	Specifies the right to read, write, list folder contents, delete folders and files, and run application files. This right includes the ReadAndExecute right, the Write right, and the Delete right.
# Read 	Specifies the right to open and copy folders or files as read-only. This right includes the ReadData right, ReadExtendedAttributes right, ReadAttributes right, and ReadPermissions right.
# ReadAndExecute 	Specifies the right to open and copy folders or files as read-only, and to run application files. This right includes the Read right and the ExecuteFile right.
# ReadAttributes 	Specifies the right to open and copy file system attributes from a folder or file. For example, this value specifies the right to view the file creation or modified date. This does not include the right to read data, extended file system attributes, or access and audit rules.
# ReadData 	Specifies the right to open and copy a file or folder. This does not include the right to read file system attributes, extended file system attributes, or access and audit rules.
# ReadExtendedAttributes 	Specifies the right to open and copy extended file system attributes from a folder or file. For example, this value specifies the right to view author and content information. This does not include the right to read data, file system attributes, or access and audit rules.
# ReadPermissions 	Specifies the right to open and copy access and audit rules from a folder or file. This does not include the right to read data, file system attributes, and extended file system attributes.
# Synchronize 	Specifies whether the application can wait for a file handle to synchronize with the completion of an I/O operation.
# TakeOwnership 	Specifies the right to change the owner of a folder or file. Note that owners of a resource have full access to that resource.
# Traverse 	Specifies the right to list the contents of a folder and to run applications contained within that folder.
# Write 	Specifies the right to create folders and files, and to add or remove data from files. This right includes the WriteData right, AppendData right, WriteExtendedAttributes right, and WriteAttributes right.
# WriteAttributes 	Specifies the right to open and write file system attributes to a folder or file. This does not include the ability to write data, extended attributes, or access and audit rules.
# WriteData 	Specifies the right to open and write to a file or folder. This does not include the right to open and write file system attributes, extended file system attributes, or access and audit rules.
# WriteExtendedAttributes