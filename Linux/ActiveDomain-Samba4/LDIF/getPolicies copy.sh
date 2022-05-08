#!/bin/bash

FILENAME="Policies.ldif"
echo""
echo "Kopiere die Sicherung von samba/private/ an diese Stelle"
echo "Liest aus der Datenbank sam.ldb die Policies aus dem LDAP Tree"
echo "und speichert sie ab in der Datei $FILENAME"
echo""
echo "Diese LDIF Datei kann man dann win den LDAP Tree einspielen"

echo -n "Press any key ...."
read var_name

#mit Base DN
#Achtung: Search in '...' einschliessen
ldbsearch -H private/sam.ldb -b CN=Policies,CN=System,DC=schule,DC=local '(&(!(displayName=Default*Domain*))(gPCFileSysPath=*schule.local*))' > $FILENAME

#Ausgabe der Namen
cat $FILENAME | grep displayName

#Delete objectGUID
sed '/objectGUID/ d' $FILENAME > work.ldif
mv work.ldif $FILENAME
