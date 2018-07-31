#Mag. Stefan Hagmann 2014
package MySamba4Tools; 

use Config::IniFiles;
use Data::Dumper;
use warnings;
use diagnostics;

#Exportiere Function Names 
#Aufruf statt LDAPTools::get_List_from_LDAP() ist dann get_List_from_LDAP()
#use Exporter;
#@ISA = ('Exporter');
#@EXPORT = qw(get_DN);

#Config File
my $pmpath=File::Basename::dirname(Cwd::realpath(__FILE__));
tie my %ini, 'Config::IniFiles', (-file => $pmpath."/config.ini");
my %Config = %{$ini{"Domain"}};
my $baseDN=$Config{BASE_DN};
my $smbPath=$Config{SMB_PATH};

#volle DN, Pfad zur ldb, Username
sub get_DN{
  my $username=shift;
  my $lib=$smbPath."sam.ldb";
  my $erg=`(ldbsearch --url=$lib cn=$username | grep dn)`;

  #Match suchen
  my @matches = split(" ", $erg);
  chomp $matches[1];

  return $matches[1];
}

#DN
sub get_VornameFromCN{
  my $username=shift;
  #in Arbeit
  my $lib=$smbPath."sam.ldb";
  my $erg=`(ldbsearch --url=$lib cn=$username | grep -i givenName)`;
  #Match suchen
  @matches = split(" ", $erg);
  chomp $matches[1];

  return $matches[1];
}

sub get_NachnameFromCN{
  my $username=shift;
  #in Arbeit
  my $lib=$smbPath."sam.ldb";
  my $erg=`(ldbsearch --url=$lib cn=$username | grep -i -w ^sn)`;
  #Match suchen
  @matches = split(" ", $erg);
  chomp $matches[1];

  return $matches[1];
}

sub get_EmailFromCN{
  my $username=shift;
  #in Arbeit
  my $lib=$smbPath."sam.ldb";
  my $erg=`(ldbsearch --url=$lib cn=$username | grep -i mail)`;
  #Match suchen
  @matches = split(" ", $erg);
  chomp $matches[1];

  return $matches[1];
}

#my @matches = $str =~ /=(\w+)/g;

