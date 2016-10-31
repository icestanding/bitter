#!/usr/bin/perl -w
#
#Yusa Written by Chenyu Li Z3492794 
#
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;

sub user_page {
    my $username = $_[0];
    # print "$username";
    my $path = $users_dir."/".$username;
    my $details_filename = $path."/details.txt";
    open my $p, "$details_filename" or die "can not open $details_filename: $!";
    $details = join '', <$p>;
    close $p;
    print img({-src => "$path/profile.jpg"});
    my $next_user = $n + 1;
    return <<eof
<div class="bitter_user_details">
$details
</div>
eof
}