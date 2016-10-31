#!/usr/bin/perl -w

#
#Logout function Written by Chenyu Li Z3492794 
#
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use POSIX qw(strftime);

$cgi = new CGI;
$sid = $cgi->cookie("CGISESSID") || undef;
$session = new CGI::Session(undef, $sid, {Directory=>'/tmp'}) || undef;
$session->delete();