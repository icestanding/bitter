#!/usr/bin/perl -w

#writing by Chenyu Li Z3492794
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;

print header();
print start_html();
print "<form action='auth.cgi' method='post'>";
print "<table align='center' width='600' border='0' cellspacing='0' cellpadding='0' class='kuang'>";
    print "<tr><td height='30' align='right'>UserName:";
    print "<td align='left'><input type='text' name='username' size='30'/></td></tr>";
    print "<tr><td height='30' align='right'>Password:</td>";
    print "<td align='left'><input type='Password' name='password' size='30'/></td></tr>";
    print "<tr>";
    print "<td height='50' colspan='2' align='center'><input type='submit' value='login' />    <input type='reset' value='reset' /></td>";
    print "</tr>";
print "</table>";       
print "</form>"; 
print end_html();

# print start_html();
# print "<head><title>登录测试页面</title>";
# print "<meta http-equiv='Content-Type' content='text/html; charset=GB2312' />";

# print "<form action='auth.cgi' method='post'>";
# print "<table align='center' width='600' border='0' cellspacing='0' cellpadding='0' class='kuang'>";
#     print "<tr><td height='30' align='right'>UserName:";
#     print "<td align='left'><input type='text' name='username' size='30'/></td></tr>";
#     print "<tr><td height='30' align='right'>Password:</td>";
#     print "<td align='left'><input type='Password' name='password' size='30'/></td></tr>";
#     print "<tr>";
#     print "<td height='50' colspan='2' align='center'><input type='submit' value='login' />    <input type='reset' value='reset' /></td>";
#     print "</tr>";
# print "</table>";       
# print "</form>";  