#!/usr/bin/perl -w
#Mag. Stefan Hagmann 2014
#Samba4 Posix/Windows Gruppe anlegen
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
my $usage = "\n$filename -g Gruppe";
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
my $gruppe   = '';
my $help = 0;

GetOptions(
    'gruppe|g=s'=> \$gruppe,
    'help|?'  => \$help,
);


sub dosleep{
  my $st=2;
  print("sleeping for $st seconds...\n");
  system("sleep $st");
}


#Alles da ? was nötig ist
pod2usage(-msg=>$usage, -verbose=>99, -sections=>"SYNOPSIS|DESCRIPTION") if($gruppe eq '');
#help angefordert?
pod2usage(-msg=>$usage, -verbose=>1) if $help;

#-------Main Program------------
my $cmd="";

$cmd="samba-tool group add ".$gruppe;
system($cmd);
dosleep();
print "$cmd\n\n";

print("Doing the LDIF stuff ... \n");
#LDIF File bauen
#get the gid
my $strgid=`(wbinfo --group-info=$gruppe)`;
my @parts=split(':', $strgid);
my $gid = $parts[2];

#LDIF File bauen
open (DATEI, ">$tmpfile") or die $!;
   print DATEI "dn: CN=$gruppe,CN=Users,".$baseDN."\n";
   print DATEI "changetype: modify\n";
   print DATEI "add: objectClass\n";
   print DATEI "objectClass: posixGroup\n";
   print DATEI "-\n";
   print DATEI "add: gidNumber\n";
   print DATEI "gidNumber: $gid\n";
close (DATEI);

#Modify User
$cmd="ldbmodify -v -H ".$smbPath."sam.ldb -b $baseDN $tmpfile";
system($cmd);
dosleep();

print "\n\nNeue Gruppe $gruppe POSIX-ified:\n";
print "gid: $gid\n";
print "getent group $gruppe\n";
system("getent group $gruppe");
system("ldbsearch --url=".$smbPath."sam.ldb cn=$gruppe | grep dn:");



__END__

#Achtung auf Syntax; erste Spalte, nach head Leerzeile, unformatiert mit 1 Space am Zeilenebginn
=encoding utf-8

=head1 NAME

$filename -g Gruppe

=head1 SYNOPSIS

 Erstellt in AD eine Windows/Linux Gruppe
 Optionen:
   --gruppe, -g    .... Benutzername\n

=head1 DESCRIPTION

 Erstellt mit den samba-tools eine AD Gruppe, und gibt dieser dann
 in der LDB Datenbank die posix Klasse, damit ist die Gruppe auch
 eine Linux Gruppe

=cut
