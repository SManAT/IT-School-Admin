#!/usr/bin/env perl
#Mag. Stefan Hagmann 20012

use Getopt::Std;
use Linux::usermod;
use File::Basename;
use Getopt::Long;
use Data::Dumper;
use FindBin;

use warnings;
use diagnostics;
#Test pod2text Filename, podchecker Filename
use Pod::Usage;
use File::Find::Rule;

#------------ DONT CHANGE
my $filename = basename(__FILE__);
# setup my defaults
my $help = 0;
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


#Arbeitsverzeichnis ermitteln
my $absDir="$FindBin::Bin/$FindBin::Script";
print "Path is: ".$absDir."\n";
my $profileDir=0;

if ($absDir =~ m/.*\/profile.*/) {
  print "We are working within: PROFILES \n";
  $profileDir=1;
}else{
  if ($absDir =~ m/.*\/home.*/) {
    print "We are working within: HOMES \n";
    $profileDir=0;
  }else{
    print "We are NOT working within AD User Directories (profile|home) ... exit \n";
    exit -1;
  }
}

print("\n");

#print Dumper(@files);
foreach $i (@files) {
  #Name heraussuchen
#print Dumper($i);
  my @words = split /\.V/, $i;
  $name = $words[0];
  $full = $i;

  #nicht für spezielle User
  if (($name =~ /rsyncuser/)||($name =~ /imager/)||($name =~ /laptop/)){
    print "--- ".$name." --- not used\n"
  }else{
    my $cmd="chown -R ".$name.":users ".$full;
    print($cmd."\n");
    if($go==1){
      system($cmd);
    }
    #------------------------------
    if($profileDir==1){
      $cmd="chmod -R 770 ".$full;
    }else{
      $cmd="chmod -R 2700 ".$full;
    }
    print($cmd."\n");
    if($go==1){
      system($cmd);
    }
    #------------------------------
    #nur Dateirechte
    $cmd="find ".$full." -type f -exec chmod 770 -- {} +";
    print($cmd."\n");
    if($go==1){
      system($cmd);
    }
    #------------------------------
    #aus profile Ordner NTUSER.DAT und ntuser.ini löschen
    if($profileDir==1){
      my $pattern = "ntuser\.(dat|ini|pol)+";

      my $rule =  File::Find::Rule->new;
      $rule->name( qr/$pattern/i );
      $rule->maxdepth(1);
      my @files = $rule->in($full);
      foreach my $item (@files) {
        $cmd="rm ".$item;
        print($cmd."\n");
        if($go==1){
          system($cmd);
        }
      }
    }
  }
}

if($go==0){
  print "\n\n==================================================================\n";
  print "Simulation > ausführen mit -g Parameter !\n";
  print "==================================================================\n";
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

