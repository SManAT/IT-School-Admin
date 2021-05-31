#!/usr/bin/perl -w
#Mag. Stefan Hagmann 2014

use File::Basename;

use warnings;
use diagnostics;
#Test pod2text Filename, podchecker Filename
use Pod::Usage;
use Getopt::Long;
use Data::Dumper;

use File::Path;
use File::Find::Rule;
use File::Copy;

#Path Seperator Support
#verwende File::Spec->catfile() zum verbinden
use File::Spec;

#Wie viele Sicherungen sollen aufgehoben werden?
my $keep = 4;

## Main Programm ##
my $verbose = 0;
my $bakdir = '';
my $savedir = ''; 
my $filename = ''; 

GetOptions(
    'backup|b=s'=> \$bakdir,
    'target|t=s'=> \$savedir,
    'name|n=s'=> \$filename,
    'verbose|v'=> \$verbose,
    'help|?'  => \$help,
);

#Alles da ? was nötig ist
pod2usage(-verbose=>99, -sections=>"SYNOPSIS|DESCRIPTION") if(($bakdir eq '')||($savedir eq '')||($filename eq ''));
#help angefordert?
pod2usage(-verbose=>1) if $help;


#Ausgabe nur bei VerboseMode
sub echo {
    print @_ if ($verbose eq 1);
}

die "Cowardly refusing to keep less than 1 backup file\n" if ($keep < 1);


#Neuen Namen der Sicherungsdatei bestimmen
sub newname {
    my ($sec,$min,$hour,$mday,$mon,$year,
              $wday,$yday,$isdst) = localtime time;
    #muss sein siehe perldoc -f localtime
    $year += 1900;
    $mon += 1;

    my $newbackup = 
    File::Spec->catfile($savedir, $filename.'-'.$mday.'-'.$mon.'-'.$year.'.000.tar.gz');
    #Nummer ausbessern und gleich testen ob es die Datei schon gibt
    $newbackup =~ s/(\d\d\d)\.tar\.gz$/substr('00'.($1+1),-3).'.tar.gz'/e while (-e $newbackup);
    return $newbackup;
}

# Ensure that the Save directory exists
eval {mkpath($savedir)};
die "Unable to find or create directory $savedir\n$@\n" if ($@);
echo "Attempting a backup of - ".$bakdir."\n";

# Backup Files ---------------------

# Choose a name for this backup
my $newbackup=File::Spec->canonpath(newname());

# Create the backup and confirm its existence
#u..Update only
if($verbose eq 1){
    system('tar cfzv '.$newbackup.' '.$bakdir);
}else{
    system('tar cfz '.$newbackup.' '.$bakdir);
}

echo "New backup created: $newbackup (" . (-s $newbackup) . " bytes)\n";

# Get a list of existing backup filenames sorted by modification time
my @backupfiles = sort {(stat $a)[9] <=> (stat $b)[9]} 
    File::Find::Rule
	->maxdepth( 1 )
	->file()
	#qr Quote-Like Operators patternmatching
	->name(qr/\d{1,2}-\d{1,2}-\d{1,4}\.\d{3}\.tar\.gz$/)
	->in($savedir); 
echo "Found a total of " . scalar(@backupfiles) . " backup files in $savedir\n";

# Recycle the oldest backup(s) if necessary
while ( scalar(@backupfiles) > $keep ) {
    echo("Unlinking oldest backup file: ". File::Spec->canonpath($backupfiles[0]) ."\n");
    unlink($backupfiles[0]) or warn "Unable to unlink $backupfiles[0]\n";
    shift @backupfiles;
}

echo "Finished\n"; 

__END__

#Achtung auf Syntax; erste Spalte, nach head Leerzeile, unformatiert mit 1 Space am Zeilenebginn
=encoding utf-8

=head1 NAME

$filename

=head1 SYNOPSIS

  doTheBackup.pl -b backupdir -t targetdir [-n name] [-v verbose]

  Options:
    --backup, -b    .... Backup Directory  
    --target, -t    .... Zielverzeichnis der Sicherungsdatei  
    --name, -n      .... Name der Sicherungsdatei  
    --verbose, -v   .... be verbose  

    Erstellt eine Sicherung von einem Verzeichnis, und legt rotierend
    mehrere Sicherungen an
    doTheBackup.pl -b /home/fred -t /backup/

=head1 DESCRIPTION

  Rotierende Sicherung von Daten

=cut
