# Prerequisites
The most Tools are written in Perl, so you had to install some libraries. Here are the steps

```
/* CPAN History & CPAN – Perl Docs */
apt-get install libterm-readline-gnu-perl perl-doc

cpan -i Bundle::CPAN

cpan -i YAML Term::ReadLine::Perl HTTP::Date Getopt::Std Getopt::Long  
Linux::usermod File::Basename Text::CSV Net::Ping DBI DBD::mysql Config::IniFiles
Data::Dumper File::Spec::Unix File::Find::Rule Log::Log4perl
```
(maybe something is missing)