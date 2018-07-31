#!/usr/bin/perl
#Copyright 2012 Mag. Stefan Hagmann

use Getopt::Std;
use Linux::usermod;
use File::Basename;

#get your own filename
my $progname=basename("$0");
my $file="userbackup.csv";

sub info_print{
    print "$progname [-u username -p klartextpasswort] [-f datei] [-e] [-i]\n";
    print "=============================\n";
    print "Perl Script um einen User anzulegen, Hash = SHA-512\n";
    print "Entweder einzeln ,mit -u oder -p oder über eine Datei mit -f\n";
    print "Die Datei ist dabei eine CSV mit username;hashCode;home\n";
    print "-u  ... Username\n";
    print "-p  ... Klartextpasswort (steht auch in History!)\n";
    print "-f  ... Datei mit username;passwort KLARTEXT (Passwörter steht auch in History!)\n";
    print "-e  ... Sicherung in CSV Datei, kann später wieder verwendet werden\n";
    print "-i  ... Gesicherte CSV Datei importieren, Hashes werden übernommen\n";
    exit;
}

#Parameterauswertung
#: = verlangt einen Wert
getopts('u:p:f:ei');


#keine Argumente
if(!defined($opt_u) && !defined($opt_p) && !defined($opt_f) && !$opt_e && !$opt_i){
   info_print();
}

#legt einen Benutzer an
sub createUser{
  my $name=shift;
  my $pass=shift;
  $path = "/home/$name";
  chomp($name);
  my $hash = qx#mkpasswd --hash=sha-512 $pass#;
  chomp($hash);
  $cmd = "useradd -m -d '".$path."' -p '".$hash."' -s '/bin/bash' ".$name;
  qx#$cmd#;
  print $cmd."\n";
}

# Perl trim function to remove whitespace from the start and end of the string
sub trim($)
{
    my $string = shift;
    $string =~ s/^\s+//;
    $string =~ s/\s+$//;
    return $string;
}

if(defined($opt_u) && defined($opt_p) && !defined($opt_f)){
  createUser($opt_u, $opt_p);
}

if(!defined($opt_u) && !defined($opt_p) && defined($opt_f)){
  #gibt es die Datei?
  if (! -e $opt_f){
    print "File not found ".$opt_f."!\n";
    exit (0);
  }

  open(FILE, $opt_f);
  while (<FILE>) {
    chomp;
    ($user, $passwd) = split(/;/);
    $user=trim($user);
    $passwd=trim($passwd);
    createUser($user, $passwd);
    print $user." ".$passwd."\n";
  }
  close(FILE);
}


if($opt_e){
  exportUsers();
}

if($opt_i){
  importUsers();
}

#sichert die User in eine Datei
sub exportUsers(){
  my @data;
  print "Erstelle eine Sicherung aller Benutzer in $file \n";
  
  open(PASSWD, '/etc/passwd');
  while (<PASSWD>) {
    chomp;
    ($login, $passwd, $uid, $gid, $gcos, $home, $shell) = split(/:/);
    if($uid >= 1000 && $login ne "nobody"){
      $str = $login.";".$home.";".$uid;
      push(@data, $str);
#      print $str."\n";
    }
  }
  close(PASSWD);

  open(SHADOW, '/etc/shadow');
  #Passwörter laden und Zeilen ersetzen
  #Place =~ s/searchstring/replacestring/gi;

  my @stack;
  while (<SHADOW>) {
    chomp;
    
    ($login, $passwd, $a, $b, $c, $d, $e) = split(/:/);
    $str = $login.";".$passwd;
    push(@stack, $str);
  }
  close(SHADOW);
  
  #Abgleich der beiden Arrays
  #Suchen und ersetzen zu login;passwd;home;uid
  open(file, ">$file");
  for  (@data) 
  {
    my $str1 = $_;
    for (@stack){
      my $str2 = $_;  #name;passwd
      #Usernamen extrahieren
      @d = split(";", $str1);
      $name = @d[0].";";
      $home = @d[1];
      @d = split(";", $str2);
      $name2 = @d[0].";";
      
      if($name eq $name2){
	  #print $name."    ".$str2."\n";
	  #name;passwd; anhängen home;
	  $wert = $str2.";".$home."\n";
	  print $wert;
	  print file $wert;
      }
    }  #for
  }    #for
  close (file);
}

#importiert die User aus eine Datei
sub importUsers(){
  #useradd -d homedir -p encryptedpass
  print "Wie heisst die Datei (".$file."):\t";
  chomp($in = <STDIN>);
  if($in eq "")  { $name = $file; }
  else           { $name = $in; }
  
  #gibt es die Datei?
  if (! -e $name){
    print "File not found ".$name."!\n";
    exit (0);
  }
  
  open(FILE, $name);
  while (<FILE>) {
    chomp;
    ($user, $passwd, $path) = split(/;/);
    $cmd = "useradd -m -d ".$path." -p ".$passwd." -s '/bin/bash' ".$user;
    print $cmd."\n";
    system($cmd);
    #/etc/shadow Datei; Zeile mit User ausbessern; Passwort mit Hash ersetzen
    #funktioniert nicht ueber useradd, weil hash irgendwie falsch ist
    replaceHash($user, $passwd);
  }
  close(FILE);
}

sub replaceHash(){
  $user = shift;
  $pnew = shift;
  
  #Shadow laden
  open(SHADOW, '/etc/shadow');
  my @stack;
  while (<SHADOW>) {
    chomp;
    $line = $_;
    ($login, $passwd, $a, $b, $c, $d, $e) = split(/:/);
    #User suchen
    if($login =~ /$user/){
      #User gefunden, Hash ersetzen
      $line = $login.":".$pnew.":".$a.":".$b.":".$c.":".$d.":".$e."::";
    }
    push(@stack, $line);
  }
  close(SHADOW);
  
  #ShadowDatei ersetzen
  open(DATEI,">/etc/shadow");  # oeffne Datei zum Schreiben
  foreach $line (@stack) { 
    print DATEI "$line\n";
  }
  close(DATEI);
}





