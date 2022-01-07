#!/usr/bin/perl -w
#Mag. Stefan Hagmann 2014
#Samba4 Posix/Windows User anlegen
#Bitte die globalen Parameter im INI File anpassen

use File::Basename;

use warnings;
use diagnostics;
#Test pod2text Filename, podchecker Filename
use Pod::Usage;
use Getopt::Long;
use Config::IniFiles;
use Data::Dumper;

#------------ DONT CHANGE
my $filename = basename(__FILE__);
my $usage = "\n$filename -u Benutzername -p Passwort [-pp Profilpfad] [-g Gruppen]";
my $tmpfile="/tmp/work.ldif";

#Config File
tie my %ini, 'Config::IniFiles', (-file => "./config.ini");
my %Config = %{$ini{"Domain"}};
my $baseDN=$Config{BASE_DN};
my $smbPath=$Config{SMB_PATH};
my $home=$Config{HOME};
my $homeShare=$Config{HOME_SHARE};
my $profileShare=$Config{PROFILE_SHARE};

# setup my defaults
my $username = '';
my $password = '';
my $groups   = '';
my $vorname   = '';
my $nachname   = '';
my $email   = '';
my $ou = '';
chomp($hostname = `hostname -s`);
my $profile  = "\\\\$hostname\\$profileShare\\%USERNAME%";
my $help = 0;
my $extendedinfo=0;
my $initials='';

GetOptions(
    'username|u=s'=> \$username,
    'password|p=s'  => \$password,
    'profile|pp=s'  => \$profile,
    'vorname|vn=s'  => \$vorname,
    'nachname|nn=s'  => \$nachname,
    'email|e=s'  => \$email,
    'orgunit|ou=s' => \$ou,
    'groups|g=s@'  => \@groups,
    'help|?'  => \$help,
);

sub dosleep{
  my $st=2;
  print("sleeping for $st seconds...\n");
  system("sleep $st");
}

#gibt es die geforderte OU?
sub OUExists{
  my $oustr=shift;
  my $answ=`ldbsearch -H /var/lib/samba/private/sam.ldb '(&(ou=$oustr)(objectClass=organizationalUnit))'`;
  my @lines = split(/[\n\r\l]+/, $answ);
  my $erg=0;
  #durchsuche Zeilen nach name: OU
  foreach (@lines) {
    #print Dumper($_);
    if($_ =~ /(name:)+/g){
      if($_ =~ /($oustr)+/gi){
        print "OU=$oustr existiert ...\n";
        $erg=1;
        last;
     }
    }
  }
  return $erg;
}

#Alles da ? was nötig ist
pod2usage(-msg=>$usage, -verbose=>99, -sections=>"SYNOPSIS|DESCRIPTION") if($username eq '' || $password eq '');
#help angefordert?
pod2usage(-msg=>$usage, -verbose=>1) if $help;
#pod2usage(-msg =>$usage, -verbose=>1) if $username;

#split options
@groups = split(/,/,join(',',@groups));

#-------Main Program------------
#OU befehl
#print Dumper($ou);
my $partou="";
if($ou ne ''){
  $partou =" --userou='ou=".$ou."'";
  #Teste ob OU überhaupt existiert
  if(OUExists($ou)==0){
    print "Die Organizational Unit (OU=$ou) existiert nicht!\nBenutzer $username wird nicht angelegt!\n";
    exit -1;
  }
}


my $cmd="";
if($vorname eq '' && $nachname eq ''){
  $cmd="samba-tool user create ".$username." ".$password." --profile-path='".$profile."' --must-change-at-next-login".$partou;
  system($cmd);
  $extendedinfo=0;
}else{
  #username wird bei cn verwendet, das ist auch bei uid
  $initials = substr($vorname, 0, 1).substr($nachname, 0, 1);
  $cmd="samba-tool user create ".$username." ".$password." --use-username-as-cn --profile-path='".$profile."' --surname='".$nachname."' --initials='".$initials."' --given-name='".$vorname."' --mail-address='".$email."' --must-change-at-next-login".$partou;
  system($cmd);
  $extendedinfo=1;
}
print "$cmd\n\n";

#In Gruppen aufnehmen
foreach (@groups){
  #gibt es die Gruppe
  chomp($_);
  my $search = `samba-tool group list | grep $_`;
  $search = "N/A" if (!defined($search) || ($search eq ""));
  if($search eq "N/A"){
    #Gruppe anlegen
    system("samba-tool group add $_");
  }
  system("samba-tool group addmembers $_ $username");
}
dosleep();

print("Doing the LDIF stuff ... \n");
#LDIF File bauen
#get the uid
my $struid=`(wbinfo -i $username)`;
my @parts=split(':', $struid);
my $uid = $parts[2];
#get the gid
my $strgid=`(wbinfo --group-info='Domain Users')`;
@parts=split(':', $strgid);
my $gid = $parts[2];

#User in andere OU?
my $partDN="CN=Users";
if($ou ne ''){
  $partDN="OU=".$ou;
}

#LDIF File bauen
open (DATEI, ">$tmpfile") or die $!;
   print DATEI "dn: CN=$username,".$partDN.",$baseDN\n";
   print DATEI "changetype: modify\n";
   print DATEI "add: objectClass\n";
   print DATEI "objectClass: posixAccount\n";
   print DATEI "-\n";
   print DATEI "add: uidNumber\n";
   print DATEI "uidNumber: $uid\n";
   print DATEI "-\n";
   print DATEI "add: gidNumber\n";
   print DATEI "gidNumber: $gid\n";
   print DATEI "-\n";
   print DATEI "add: unixHomeDirectory\n";
   print DATEI "unixHomeDirectory: $home$username\n";
   print DATEI "-\n";
   print DATEI "add: loginShell\n";
   print DATEI "loginShell: /bin/bash\n";
   print DATEI "add: homeDrive\n";
   print DATEI "homeDrive: Z:\n";
   print DATEI "-\n";
   print DATEI "add: homeDirectory\n";
   print DATEI "homeDirectory: \\\\$hostname\\$homeShare\\$username\n";
   if($extendedinfo==1){
     print DATEI "-\n";
     print DATEI "changetype: modify\n";
     print DATEI "replace: displayName\n";
     print DATEI "displayName: $vorname $nachname\n";
     print DATEI "-\n";
     print DATEI "changetype: modify\n";
     print DATEI "replace: initials\n";
     print DATEI "initials: $initials\n";
   }
close (DATEI);

#Modify User
$cmd="ldbmodify -v -H ".$smbPath."sam.ldb -b $baseDN $tmpfile";
system($cmd);
dosleep();


print("Doing the Linux home stuff ... \n");
#Am Linux System anlegen
system("mkdir -p $home$username");
system("chown root:users $home$username");
#nur USer darf auf Linux Ebene rein
system("chmod 700 $home$username");
#Skeleton kopieren
#system("cp -r /etc/skel/.* $home$username/  >/dev/null 2>&1");
system("cp -r /etc/skel/. $home$username");
system("chown -R $uid:$gid $home$username");
system("rm $tmpfile");

print "\n\nNeuer Benutzer $username POSIX-ified:\n";
print "uid: $uid\n";
print "gid: $gid\n";
print "getent passwd $username\n";
system("getent passwd $username");
my $sid=`(wbinfo --gid-to-sid=$gid)`;
print "sid: $sid\n";
system("ldbsearch --url=".$smbPath."sam.ldb cn=$username | grep \\\\$hostname");
system("ldbsearch --url=".$smbPath."sam.ldb cn=$username | grep homeDrive");



__END__

#Achtung auf Syntax; erste Spalte, nach head Leerzeile, unformatiert mit 1 Space am Zeilenebginn
=encoding utf-8

=head1 NAME

$filename -u Benutzername -p Passwort [-vn Vorname -nn Nachname -e Email] [-g Gruppen] [-ou OrgUnits]

=head1 SYNOPSIS

 Erstellt in AD einen Windows/Linux Benutzer in der Standardgruppe 
 Domain Users
 Optionen:
   --username, -u    .... Benutzername\n
   --password, -p    .... Passwort
   --vorname, -vn    .... Vorname
   --nachname, -nn   .... Nachname
   --email, -e       .... Email Adresse
   --profile, -pp    .... ProfilPfad, z.B:\\\\pdc\\Profile\\%USERNAME%
                          legt fest, wo das Profil der Win User liegt
                          Backslashes escaped angeben!
                          \\<hostname>\<Sharename>\
                          wird per default of obigen Pfad gelegt
   --groups, -g      .... zusätzliche Gruppen 
                          z.B. Lehrer,Physiker,Hausmeister
   --orgunit, -ou    .... in welche Organization Unit wird der User gelegt
                          Muss existieren!
                          Standard ist ou=Users

=head1 DESCRIPTION

 Erstellt mit den samba-tools einen AD User, und gibt diesem dann
 in der LDB Datenbank die posix Klasse, damit ist der User auch
 ein Linux User

=cut
