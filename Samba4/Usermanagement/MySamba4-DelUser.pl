#!/usr/bin/perl -w
#Mag. Stefan Hagmann 2014
#Samba4 Posix/Windows delete
#Bitte die globalen Parameter im INI File anpassen
use File::Basename;

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

GetOptions(
    'username|u=s'=> \$username,
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
system("samba-tool user delete ".$username);
system("rm -r -v  ".$home.$username);
system("rm -r -v  ".$profile.$username.".*");

__END__

#Achtung auf Syntax; erste Spalte, nach head Leerzeile, unformatiert mit 1 Space am Zeilenebginn
=encoding utf-8

=head1 NAME

$filename -u Benutzername

=head1 SYNOPSIS

 Löscht einen Windows/Linux Benutzer
 Optionen:
   --username, -u    .... Benutzername\n

=head1 DESCRIPTION

 Löscht einen Windows/Linux Benutzer 

=cut
