#!/bin/bash

FILENAME="Machines.ldif"

#mit Base DN
ldbsearch -H private/sam.ldb -b CN=Computers,DC=schule,DC=local > $FILENAME

#Ausgabe der Namen
cat $FILENAME | grep name

#Delete objectGUID
sed '/objectGUID/ d' $FILENAME > work.ldif
mv work.ldif $FILENAME

#isCriticalSystemObject
#primaryGroup
#sAMAccountType
#pwdLastSet

