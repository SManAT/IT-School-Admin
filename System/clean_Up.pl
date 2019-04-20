#!/usr/bin/env perl
#Mag. Stefan Hagmann 20019

use Getopt::Std;
use Linux::usermod;
use File::Basename;
use Getopt::Long;
use Data::Dumper;
use FindBin;
use File::Find::Rule;

use warnings;
use diagnostics;
#Test pod2text Filename, podchecker Filename
use Pod::Usage;

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


sub search_and_destroy {
  my $pattern=shift();
  my $dirPath=shift();
  my $go=shift();

  my $rule =  File::Find::Rule->new;
  $rule->name( qr/$pattern/i );
  $rule->maxdepth(2);
  $rule->mindepth(2);

  my @files = $rule->in($dirPath);
  foreach my $item (@files) {
    $cmd="rm -r -v  ".$item;
    print($cmd."\n");
    if($go==1){
      system($cmd);
    }
  }
  return;
}
 


#Arbeitsverzeichnis ermitteln
my $absDir="$FindBin::Bin/$FindBin::Script";
my $dirPath = dirname($absDir);
print "Path is: ".$dirPath."\n";


#Read Regex File
my $file = 'regex.cleanup';
open(my $fh, '<:encoding(UTF-8)', $file)
  or die "Could not open file '$filename' $!";
 
while (my $pattern = <$fh>) {
  chomp $pattern;
  search_and_destroy($pattern, $dirPath, $go);
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

 Optionen:
   --go, -g    .... Jetzt wirklich machen


=head1 DESCRIPTION

  AD Windows/Linux Rechte setzen, Restore Tool

=cut

