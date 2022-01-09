#!/usr/bin/perl -w
#Mag. Stefan Hagmann 2014
#Samba4 Posix/Windows delete
#Bitte die globalen Parameter im INI File anpassen
use File::Basename;
use File::Find::Rule;

use warnings;
use diagnostics;
#Test pod2text Filename, podchecker Filename
use Pod::Usage;
use Getopt::Long;
use Config::IniFiles;

#------------ DONT CHANGE
my $filename = basename(__FILE__);
my $usage = "\n$filename -u Benutzername";


# setup my defaults
my $username = '';
my $help = 0;
my $go = 0;

GetOptions(
    'username|u=s'=> \$username,
    'go|g'=> \$go,
    'help|?'  => \$help,
);

#Config File
tie my %ini, 'Config::IniFiles', (-file => "./config.ini");
my %Config = %{$ini{"Domain"}};
my $home = $Config{HOME};
my $profile = $Config{PROFILE};


#Alles da ? was nötig ist
pod2usage(-msg=>$usage, -verbose=>99, -sections=>"SYNOPSIS|DESCRIPTION") if($username eq '');
#help angefordert?
pod2usage(-msg=>$usage, -verbose=>1) if $help;

#-------Main Program------------
#AD User löschen
my $cmd = "samba-tool user delete ".$username;
print($cmd."\n");
if($go==1){
  system($cmd);
}

$cmd="rm -r -v  ".$home.$username;
print($cmd."\n");
if($go==1){
  system($cmd);
}

#Profile mit Versionsnummern
my $pattern = $username."(\.V[1-9])?";

my $rule =  File::Find::Rule->new;
$rule->name( qr/$pattern/ );
$rule->maxdepth(1);
my @files = $rule->in( $profile );
foreach my $item (@files) {
  $cmd="rm -r -v  ".$item;
  print($cmd."\n");
  if($go==1){
    system($cmd);
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

$filename -u Benutzername [-g]

=head1 SYNOPSIS

 Löscht einen Windows/Linux Benutzer
 Optionen:
   --username, -u    .... Benutzername\n
   --go, -g    .... Jetzt wirklich machen

=head1 DESCRIPTION

 Löscht einen Windows/Linux Benutzer 

=cut
