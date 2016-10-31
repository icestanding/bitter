#!/usr/bin/perl -w
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use strict;
use CGI::Session;
use CGI;
use DBI;
use CGI::Carp qw(fatalsToBrowser);

#create a new CGI object.
my $cgi = new CGI;
$CGI::DISABLE_UPLOADS = 1;          # Disable uploads
# $CGI::POST_MAX        = 512 * 1024; # limit posts to 512K max


#try to retrieve cookie.
my $sid = $cgi->cookie("CGISESSID") || undef;


#create session... If I retrieved a previous session id, reconnect to it.
#if not, create a new session.
my $session = new CGI::Session(undef, $sid, {Directory=>'c:/temp/session'});
$a = $session->param("id");
$b = $session->param("pwd");
    print header();
    print start_html();
    print "id:$a pwd:$b";
    print end_html();
