#!/usr/bin/perl -w
#Mag. Stefan Hagmann 2018

use File::Basename;
use String::Util qw(trim);

use warnings;
use diagnostics;
#Test pod2text Filename, podchecker Filename
use Pod::Usage;
use Getopt::Long;
use Config::IniFiles;
use Data::Dumper;
use lib ('./');
use MySamba4Tools;
use utf8;


#------------ DONT CHANGE
my $filename = basename(__FILE__);

#Config File
tie my %ini, 'Config::IniFiles', (-file => "./config.ini");
my %Config = %{$ini{"Domain"}};
my $baseDN=$Config{BASE_DN};
my $smbPath=$Config{SMB_PATH};
my $initPwd=$Config{INITPWD};
my $homePath=$Config{HOME};
my $profilePath=$Config{PROFILE};


# setup my defaults
my $csv = '';
my $help = 0;
my $go = 0;

GetOptions(
    'filename|f=s'=> \$csv,
    'go|i'=> \$go,
    'help|?'  => \$help,
);

sub FileExists{
  my $file = shift;
  if (! -e $file){
    print "File not found ($file) !\n";
    exit(-1);
  }
}


#gibt es den Benutzer am System?
sub UserExists{
  my ($DB, $username) = @_;
  my $erg=0;
  #durchsuche Zeilen nach username
  foreach my $item (@$DB) {
    if($item =~ /(^$username$)+/g){
        #user gefunden
        $erg=1;
        last;
    }
  }
  return $erg;
}

sub readDir{
  my $path = shift;
  #Verzeichnis auslesen
  @files=();
  opendir(DIR,$path);
  while($datei = readdir(DIR)) {
    unless( ($datei eq ".") || ($datei eq "..") ){
        #nur Directorys
        if (-d $path.$datei) {
          push(@files, $path.$datei);
        }
    }
  }
 closedir(DIR);
 return @files;
}

sub setRechte{
  my ($path, $username) = @_;
  my @files = readDir($path);

 my $found=0; 
 foreach $i (@files) {
   if($i =~ /($username)+/g){
     #Name heraussuchen
     #moser.V2 -> moser
     my @words = split /\.V/, $i;
     #Letzten Ordner extrahieren
     $name = basename($words[0]);

     $full = $i;
     print "chown -R ".$name.":users ".$full."\n";
     $found = $found + 1;
     if($go==1){
       system("chown -R ".$name.":users ".$full);
     }
  }
 }
 if($found==0){
    print "[".$username.":".$path."] Keine Ordner umd die Rechte zu setzen!\n";
  }
}



sub renameHomes{
  my($path, $username_old, $username_new) = @_;
  my $oldname = File::Spec->catfile( $path, $username_old );
  if (-d $oldname) {
    $cmd = "mv ".$oldname." ".File::Spec->catfile( $path, $username_new );
    print $cmd."\n";
    if($go==1){
      system($cmd);
    }
  }
}

sub renameProfiles{
  my($path, $username_old, $username_new) = @_;
  my $oldname = File::Spec->catfile( $path, $username_old );
  #teste Profilnummern V2 V3 V4 etc
  for (my $i=2; $i <= 20; $i++) {
    if (-d $oldname.".V".$i) {
       $cmd = "mv ".$oldname.".V".$i." ".File::Spec->catfile( $path, $username_new ).".V".$i;
       print $cmd."\n";
       if($go==1){
         system($cmd);
       }
    }
  }
}

sub createLDIF{
  my ($username_old, $username_new) = @_;

  #Suche passenden DN
  my $userData = `(ldbsearch -H /var/lib/samba/private/sam.ldb '(cn=*$username_old*)' DN)`;
  my @data = split('\\n', $userData);
  my $DN;
  foreach $line(@data){
    if($line =~ /(dn:.*CN=$username_old.*$baseDN$)+/g){
      $DN = $line;
      last;
    }
  }


  open(my $fh, '>', 'tmp.ldif');
  print $fh "#https://access.redhat.com/documentation/en-US/Red_Hat_Directory_Server/8.2/html/Administration_Guide/Creating_Directory_Entries-LDIF_Update_Statements.html\n";
  print $fh "#modrdn changes only CN Part in dn and changes CN and NAME Attribut\n";
  print $fh $DN."\n";
  print $fh "changetype: modrdn\n";
  print $fh "newrdn: CN=".$username_new."\n";
  print $fh "deleteoldrdn: 1\n";

  print $fh "\n";

  #Replace in DN OLD mit NEW
  $DN =~ s/$username_old/$username_new/ig;

  print $fh $DN."\n";
  print $fh "changetype: modify\n";
  print $fh "replace: sAMAccountName\n";
  print $fh "sAMAccountName: ".$username_new."\n";
  print $fh "-\n";
  print $fh "replace: userPrincipalName\n";
  print $fh 'userPrincipalName: '.$username_new.'@schule.local'."\n";
  print $fh "-\n";
  print $fh "replace: unixHomeDirectory\n";
  print $fh "unixHomeDirectory: /PDC/homes/".$username_new."\n";
  print $fh "-\n";
  print $fh "replace: homeDirectory\n";
  print $fh 'homeDirectory: \\\\daddy\\home$\\'.$username_new."\n";
  
  close $fh;
}

sub doLDIF{
  $cmd = "ldbmodify -v -H /var/lib/samba/private/sam.ldb -b ".$baseDN." tmp.ldif";
  print $cmd."\n";
  if($go==1){
    system($cmd);
  }
}

#Umbenenne
sub RenameUser{
  my($username_old, $username_new, $DB) = @_;

  if(UserExists(\@$DB, $username_old) eq 1){
    printf "Username: %-10s Neu: %s\n", $username_old, $username_new;
    print "============================================\n";

    #Suche in Home Verzeichnissen
    renameHomes($homePath, $username_old, $username_new);

    #Suche in Profile Verzeichnissen
    renameProfiles($profilePath, $username_old, $username_new);

    #Such in LDB
    print "\nDurchsuche die Datenbank\n";
    print "--------------------------------------------\n";
    print "Erstelle LDIF File tmp.ldif\n";
    createLDIF($username_old, $username_new);
    doLDIF();

    #Setze die Rechte
    print "\nSetze die richtigen Rechte\n";
    print "--------------------------------------------\n";
    setRechte($homePath, $username_new);
    setRechte($profilePath, $username_new);


    print "\n";
  }else{
    printf "### User %s existiert nich in der Database! --cancel--\n", $username_old;
  }
}

sub LoadUsersfromDB(){
  my $usersData = `(samba-tool user list)`;
  my @users = split('\\n', $usersData);

  #herausnehmen die Built in Users Administrator,nslcd-service,dns-,krbtgt,Guest
  ##Remove items from an array from backward
  for(my $i=$#users;$i>=0;$i--) {
	if ($users[$i] =~ m/(Administrator|.*-service|.*-mount)+/) {splice(@users,$i,1);}
  }
  return @users;
}

#-------Main Program------------
#Alles da ? was nötig ist
#help angefordert?
pod2usage(-verbose=>1) if $help;

#print Dumper($csv);

if($csv eq ''){
  pod2usage(-verbose=>99, -sections=>"SYNOPSIS|DESCRIPTION");
}


FileExists($csv);
open my $fh, "<:encoding(utf8)", $csv;
my $first=0;
my @DB = LoadUsersfromDB();

while (<$fh>) {
  chomp;
  my( $username_old, $username_new ) = split ';';
  chomp($username_old);
  chomp($username_new);
  #array as reference
  RenameUser(trim($username_old), trim($username_new), \@DB);
}
close $fh;
if($go==0){
  print "\n\n#*****************************************************#\n";
  print "SIMULATION wirklich ausfuehren mit -g als Parameter\n";
  print "#*****************************************************#\n\n\n\n\n";
}


  

__END__

#Achtung auf Syntax; erste Spalte, nach head Leerzeile, unformatiert mit 1 Space am Zeilenebginn
=encoding utf-8

=head1 NAME

$filename -f Dateiname.csv [-i|-e]

=head1 SYNOPSIS

 Benennt USer in der AD um. Dabei werden sowohl die home Verzeichnisnamen als auch
 die Profil Verzeichnisnamen angepasst. In der LDB Datenbank werden alle Anpassungen
 vorgenommen
 Die CSV Datei sieht so aus
 Username_OLD;Username_NEW

 ACHTUNG: Linux Zeilenumbrüche und am Ende keine Leerzeilen!

 Optionen:
   --file, -f    .... Dateiname
   --go, -g      .... lets do it, ansonsten nur simuliert


=head1 DESCRIPTION

  Benennt User in der AD um

=cut
