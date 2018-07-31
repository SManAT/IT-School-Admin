#!/usr/bin/perl -w
#Mag. Stefan Hagmann 2014
#Samba4 Posix/Windows User anlegen aus CSV Datei

use File::Basename;

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

# setup my defaults
my $csv = '';
my $help = 0;
my $import = 0;
my $export = 0;

GetOptions(
    'filename|f=s'=> \$csv,
    'import|i'=> \$import,
    'export|e'=> \$export,
    'help|?'  => \$help,
);

sub FileExists{
  my $file = shift;
  if (! -e $file){
    print "File not found ($file) !\n";
    exit(-1);
  }
}

#Exists('--email', $email);
sub Exists{
  my $praefix=shift;
  my $data=shift;

  my $em='';
  $em = "N/A" if (!defined($data) || ($data eq ""));
  if($em eq "N/A"){
    $data = "";
  }else{
    $data=" ".$praefix." ".$data;
  }
  return $data;
}

#gibt es den Benutzer am System?
sub UserExists{
  my $username=shift;
  my $usersData = `(samba-tool user list)`;
  my @users = split('\\n', $usersData);
  my $erg=0;
  #durchsuche Zeilen nach username
  foreach (@users) {
    #print Dumper($_);
    if($_ =~ /(^$username$)+/g){

        print "####\nBenutzer $_ $username existiert bereits, Abbruch...\n";
        $erg=1;
        last;
     }
    }
  return $erg;
}

#Eine Zeile aus CSV bearbeiten
sub ProcessEntry{
  my $vorname = shift;
  my $nachname = shift;
  my $username = shift;
  my $email = shift;
  my $gruppen = shift;
  my $ou = shift;
  if(UserExists($username) eq 0){
    printf "Vorname: %-10s Nachname: %s\n", $vorname, $nachname;
    print "--------------------------------------------\n";
    $cmd="perl MySamba4-AddUser.pl -u $username -p $initPwd ".Exists('-vn',$vorname).Exists('-nn',$nachname).Exists('-g',$gruppen).Exists('-ou',$ou).Exists('-e', $email);
    print $cmd."\n";
    print "--------------------------------------------------------\n";
    system($cmd);
    print "\n\n";
  }
}



#-------Main Program------------
#Alles da ? was nötig ist
#help angefordert?
pod2usage(-verbose=>1) if $help;


#print Dumper($import);
#print Dumper($export);
#print Dumper($csv);

#Import Export geht nicht beides
if(($import==1)&&($export==1)){
  print "Import und Export geht nicht zusammen! Abbruch ...\n";
  exit;
}
if(($csv ne '')&&($import==0)){
  pod2usage(-verbose=>99, -sections=>"SYNOPSIS|DESCRIPTION");
}
if(($import==0)&&($export==0)){
  pod2usage(-verbose=>99, -sections=>"SYNOPSIS|DESCRIPTION");
}

if(($csv ne '')&&($import==1)){
    FileExists($csv);
    open my $fh, "<:encoding(utf8)", $csv;
    my $first=0;
    while (<$fh>) {
        if($first eq 0){ $first=1; }
	else{
	  chomp;
          my ( $vorname, $nachname, $username, $email, $gruppen, $ou ) = split ';';
 	  ProcessEntry($vorname, $nachname, $username, $email, $gruppen, $ou);
	}
    }
    close $fh;
}

if($export==1){
  #Datum 
  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime time;
  #muss sein siehe perldoc -f localtime
  $year += 1900;
  $mon += 1;

  $csv = "export_AD_Users.csv";
 # $csv = $csv.'-'.$mday.'-'.$mon.'-'.$year.'.csv';


  open my $fh, ">:encoding(utf8)", $csv;

  print $fh "Vorname;Nachname;Username;Email;Zusatzgruppen;OU\n";
    
  #Daten exportieren
  #User laden
  my $usersData = `(samba-tool user list)`;
  my @users = split('\\n', $usersData);

  #herausnehmen die Built in Users Administrator,nslcd-service,dns-,krbtgt,Guest
  ##Remove items from an array from backward
  for(my $i=$#users;$i>=0;$i--) {
	if ($users[$i] =~ m/(Administrator|.*-service|dns-|krbtgt|Guest|goofy|.*-mount|bibliothek|physik|informatik|test|schularzt)+/) {splice(@users,$i,1);}
  }
  
  my $i=0;
  print "Exporting Data\n";
  foreach (@users){
	#Daten laden
       #Username $_
	my $dn=MySamba4Tools::get_DN($_)."\n";
	my $vorname = MySamba4Tools::get_VornameFromCN($_);
	my $nachname = MySamba4Tools::get_NachnameFromCN($_);
	my $username = $_;
	my $email = MySamba4Tools::get_EmailFromCN($_);

#	print Dumper( $_);
#	print Dumper( MySamba4Tools::get_NachnameFromCN($_));
        print $fh $vorname.";".$nachname.";".$username.";".$email.";"."\n";

	print ".";
	$i++;
	if ($i==80){
	    print "\n";
	    $i=0;
	}
  }

  close $fh;
  print "\n";
  print "done\n";
}

__END__

#Achtung auf Syntax; erste Spalte, nach head Leerzeile, unformatiert mit 1 Space am Zeilenebginn
=encoding utf-8

=head1 NAME

$filename -f Dateiname.csv [-i|-e]

=head1 SYNOPSIS

 Erstellt in AD Windows/Linux Benutzer aus einer CSV Datei
 Die CSV Datei sieht so aus
 Vorname;Nachname;Username;Email;Zusatzgruppen

 ACHTUNG: Linux Zeilenumbrüche und am Ende keine Leerzeilen!

 Zusatzgruppen ... Default ist Domain Users, das sind weitere z.B: Gruppe1,Gruppe2

 Optionen:
   --file, -f    .... Dateiname
   --import, -i  .... Import aus CSV Datei
   --export, -e  .... Export in CSV Datei


=head1 DESCRIPTION

  Erstellt in AD Windows/Linux Benutzer aus einer CSV Datei

=cut
