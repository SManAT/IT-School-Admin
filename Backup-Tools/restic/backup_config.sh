#Backup GYMBADEN Config Files erstellen
#Mag. Stefan Hagmann 2006

pfad="/backup/backup/"

for u in $pfad
do
echo "KonfigFiles"
  cp -p -u /etc/dhcpd.conf $u 2>/dev/null
  cp -p -u /etc/vsftpd.chroot_list $u
  cp -p -u /etc/vsftpd.conf $u

echo "/etc"
  rsync -v -a -A -X -u -z /etc $u
echo "Usermanagment"
  mkdir -p $u/usermanagment/
  perl /backup/maintaince/usermanagment/UserManagement.pl -e
  cp /backup/maintaince/usermanagment/UserManagement.pl $u/usermanagment/
  mv  userbackup.csv $u/usermanagment/
echo "Chrony"
  cp -r -a -u /etc/chrony $u  
#echo "MDADM"
#  cp -r -a -u /etc/mdadm $u  
echo "PHP"
  cp -r -a -u /etc/php $u  
echo "sSMTP"
  cp -r -a -u /etc/ssmtp/ $u
echo "OpenSSL Server"
  cp -r -a -u /etc/ssl $u
#echo "Postfix"
#  cp -r -a -u /etc/postfix $u
#echo "Squid"
#  cp -r -a -u /etc/squid $u
echo "SSH"
  cp -r -a -u /etc/ssh $u
echo "Apache 2"
  rm -r $u/apache2
  cp -r -a -u /etc/apache2 $u
#echo "IPTables"
#  cp -r -a -u /etc/iptables.rules $u
echo "Netplan"
  rm -r $u/netplan
  cp -r -a -u /etc/netplan $u
echo "Fail2Ban"
  cp -r -a -u /etc/fail2ban $u
echo "LetEncrypt"
  cp -r -a -u /etc/letsencrypt $u
echo "Root User"
  mkdir -p $u/root/
  rsync -v -a -A -X -u -z --exclude '.cpan' /root/  $u/root/
echo "TimerUnits"
  mkdir -p $u/system/SH-Timer-Scripts
  cp -r -a -u /etc/systemd/system/SH-Timer-Scripts $u/system
  cp -a -u /etc/systemd/system/SH* $u/system  

#echo "CUPS"
#  cp -r -a -u /etc/cups $u    
#echo "SpamAssassin"
#  cp -r -a -u /etc/mail $u      
#echo "Courier"
#  cp -r -a -u /etc/courier $u
#echo "Dovecot"
#  cp -r -a -u /etc/dovecot $u
echo "AppArmor"
  cp -r -a -u /etc/apparmor $u
  cp -r -a -u /etc/apparmor.d $u
#echo "Skeletton"
#  cp -r -a -u /etc/skel $u
#echo "Dansguardian"
#  cp -r -a -u /etc/dansguardian $u
echo "MySQL"
  # Backup mit /backup/backup/IT-School-Admin/MySQL/MySQLBackup.py
  mkdir -p $u/mysql
  cp -r -a -u /etc/mysql/ $u

  python3 /backup/IT-School-Admin/MySQL/MySQLBackup.py

#echo "MySQL Daten Rotierend"
#  systemctl stop  mysql
#  rm -r $u/mysql/mysqldb
#  mkdir -p $u/mysql/mysqldb
#  cp -P -r -a -u -v /var/lib/mysql $u/mysql/mysqldb
#  systemctl start mysql
#  mkdir -p $u/mysql/DB
#  perl doMySQLBackup.pl -t /backup/backup/mysql/DB/
done

logger "BACKUP CONFIG done ..."

echo