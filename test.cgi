#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

print header, start_html('Login');
warningsToBrowser(1);

$id = param('id') || '';
$password = param('pwd') || '';

if ($id && $password){
	print "$id $password";
}
else{
	print <<eof
<form method="post" action="">
<input type="text" name="id" value="">
<input type="text" name="pwd" value="">
<input type="submit" value="submit">
</form>
eof
}
print end_html();