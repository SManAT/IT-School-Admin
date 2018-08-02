#!/usr/bin/env perl
#Mag. Stefan Hagmann 20012

use Getopt::Std;
use Linux::usermod;
use File::Basename;
use Getopt::Long;
use Data::Dumper;


use warnings;
use diagnostics;
#Test pod2text Filename, podchecker Filename
use Pod::Usage;

#------------ DONT CHANGE
my $filename = basename(__FILE__);
# setup my defaults
my $hekp = 0;
my $go = 0;

GetOptions(
    'go|g'=> \$go,
    'help|?'  => \$help,
);


#-------Main Program------------
#Alles da ? was nötig ist
#help angefordert?
pod2usage(-verbose=>1) if $help;

#Verzeichnis auslesen
@files=();
opendir(DIR,"./");
  while($datei = readdir(DIR)) {
    unless( ($datei eq ".") || ($datei eq "..") ){
        #nur Directorys
        if (-d $datei) {
          push(@files, $datei);
        }
    }
  }
closedir(DIR);


foreach $i (@files) {
  #Name heraussuchen
  #moser.V2 -> moser
  #splitte am punkt
  my @words = split /\./, $i;
#  print Dumper @words[0];
  $name = $words[0];
  $full = $i;

  #nicht für spezielle User
  if (($name =~ /rsyncuser/)||($name =~ /imager/)||($name =~ /laptop/)){
    print "--- ".$name." --- not used\n"
  }else{
    print "chown -R ".$name.":users ".$full."\n";
    if($go==1){
      system("chown -R ".$name.":users ".$full);
    }
  }
}





__END__

#Achtung auf Syntax; erste Spalte, nach head Leerzeile, unformatiert mit 1 Space am Zeilenebginn
=encoding utf-8

=head1 NAME

$filename [-g] 

=head1 SYNOPSIS

 Setzt die Rechte der im Verzeichnis liegenden Unterordner nach dern Namen.
 Home Ordner heissen so wie der User z.B. moser
 Die Rechte werden dann für den Ordner moser nach moser:users gesetzt.

 Das gilt auch für Windows ProfilOrdner z.B. moser.V2 oder moser.V4 werden
 ebenfalls nach moser:users gesetzt.

 Optionen:
   --go, -g    .... Jetzt wirklich machen


=head1 DESCRIPTION

  AD Windows/Linux Rechte setzen, Restore Tool

=cut

