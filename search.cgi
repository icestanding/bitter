#!/usr/bin/perl -w

#
#Search page Written by Chenyu Li Z3492794 
#
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use POSIX qw(strftime);


#
# Main function print all page inside
#
sub main() {
    # initial directory and set debug = 1
    $users_dir = "dataset-large/users";
    $bleats_dir = "dataset-large/bleats";
    $debug = 1;

    # check if the logout is set
    $sign = param('logout') || '';

    #create the session
    $cgi = new CGI;
    $sid = $cgi->cookie("CGISESSID") || undef;
    $session = new CGI::Session(undef, $sid, {Directory=>'/tmp'}) || undef;

    #if logout button press, do the seesion delete
    if ($sign == 1) {
        $session->delete();
    }

    #loading the session of userid
    $user= $session->param("id") || ''; 
    $pwd = $session->param("pwd") || '';

    $warning = check();
    my $mode1 = "user";
    my $mode2 = "bitter";

    # print each part of page
    if ($user eq '' or $sign == 1) {
    print login_page_header();
    $search_value = param('search');
    print <<eof;
    <ol class="breadcrumb">
  <li><a href="search.cgi?search=$search_value&mode=$mode1">User</a></li>
  <li><a href="search.cgi?search=$search_value&mode=$mode2">Bitter</a></li>
</ol>
eof
    search();
    }
    else{
        print user_header();
    $search_value = param('search');
    print <<eof;
    <ol class="breadcrumb">
  <li><a href="search.cgi?search=$search_value&mode=$mode1">User</a></li>
  <li><a href="search.cgi?search=$search_value&mode=$mode2">Bitter</a></li>
</ol>
eof
    search();

    }
    print end_html();

}


#
# check username and password 
# 
sub check{
    if (defined param('username') and defined param('password')) {
        my $username = param('username');
        my $password = param('password');
        my $path = $users_dir."/".$username;

        # check username
        if (not -e $path){
            return "Please check your username";
        }

        # give user detail.txt path
        $path = $path."/details.txt";

        # search through details.txt to get passowrd
        open (F, "$path") or die;
        my $pwd = "";
        while (<F>) {
            if ($_ =~ /^\s*password/) {
                $pwd = $_;
            }
        }

        # use regular expression to get password and check 
        $pwd =~ s/^password\://;
        $pwd =~ s/\s*//g;

            #check if the password are equal
        if ($pwd eq $password) 
        {
            # # set session to expire in 1 hour
            $session->expire("+1h");

            # store something
            $session->param("id",$username);
            $session->param("pwd",$pwd);

            # write to disk
            $session->flush();

            # create the cookie with a 1hour limit..
            my $cookie = $cgi->cookie(-name=>"CGISESSID", -value=>$session->id, -expires=>"+1h", -path=>"/");

            # set the cookie..
            # print $cgi->header(-cookie => $cookie );
            print header(-refresh => '0; url=bitter.cgi',-cookie => $cookie);
            return "";

        }
        else
        {
            return "Please check your password";
        }


    }
    
}


#
# This is the search part of bitter 
# Used for searching for specific users
#
sub search() {

    print "<H1>Key words: ", param('search'), "</H1>";
    print p();
    if (defined param('search')) {
        if (param('search') eq '') {
            return;
        }
        my $pattern = param('search');
        my $re = qr/$pattern/;
        opendir (DIR, $users_dir) or die $!;
        if(defined param('mode')){
            #if $mode is user show the user result
            if (param('mode') eq 'user') {        
                while (my $file = readdir(DIR)) {
                    if ($file =~ $re) {
                        my $un; #username
                        my $hs = ""; #user address
                        my $path = $users_dir.'/'.$file."/details.txt";
                        my $photo = $users_dir.'/'.$file."/profile.jpg";
                        open($D, $path) or die "can't open $path $!";
                        while (<$D>)
                        {
                            if ($_ =~ /^username/) {
                                $un = $_;
                            }
                            if ($_ =~ /^home_suburb/) {
                                $hs = $_;
                            }
                        }
                        $un =~ s/^username: //;
                        if ($hs eq '') {
                            $hs = "No area record";
                        }
                        else{
                            $hs =~ s/^home_suburb: //;
                        }
print <<eof
<div class="row">
  <div class="mybleat">
    <div class="thumbnail">
      <a href="otheruser.cgi?follow=$un&show=bitter&page=1"><img src="$photo" height="45" width="45"></a>
      <div class="caption">
        <h3>$un</h3>
        <p>$hs</p>
        </p>
      </div>
    </div>
  </div>
</div>    
eof
                    }
                }
            }

#giving the search result
            if (param('mode') eq 'bitter') {
                    #search the bleat by the key words and then push it number to a array
                my $path = $bleats_dir;
                opendir (B, $bleats_dir) or die "can't open $path";
                while (my $file = readdir(B)) {
                    my $bpath = $path.'/'.$file;
                    open($p, $bpath) or die "can't open $bpath";
                    while (my $line=<$p>) {
                        if ($line =~ /^in_reply_to/) {
                            last;
                        }
                        if ($line =~ /^bleat/) {
                            $line =~ s/^blest://;
                            if ($line =~ $re) {
                                push(@bleat, $file);
                                last;
                            }
                        }
                     }
                }

                    #print the bleat by time sequence
                foreach (reverse sort @bleat) {
                    my $un = "";
                    my $tim = "";
                    my $ble = "";
                    my $flag = 0;
                    open my $b, $bleats_dir.'/'.$_ or die "can not open bleats file $!";
                    while (<$b>) {
                        if ($_ =~ /^bleat/){
                            $ble = $_;
                        }
                        if ($_ =~ /^time/){
                            $tim = $_;
                        }
                        if ($_ =~ /^username: /) {
                            $un = $_;
                       }
                       # to skip the user reply
                       if ($_ =~ in_reply_to) {
                           $flag = 1;
                       }
                   }
            if ($flag == 1) {
                next;
            }
            $tim =~ s/time: //;
            my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($tim);
            my $format_time=sprintf("%d-%d-%d %d:%d:%d",$year+1900,$mon+1,$mday,$hour,$min,$sec);
           $un =~ s/^username: //;
           $ble =~ s/^bleat: //;
           $ble =~ s/bleats: //;
           my $profile_path = $users_dir.'/'.$un.'/profile.jpg';
print <<eof
<div class="row">
  <div class="mybleat">
    <div class="thumbnail">
      <img src="$profile_path" height="45" width="45">
      <div class="caption">
        <h3>$un</h3>
        <p>$ble</p>
        <p>$format_time</p>
        <p><a href="reply.cgi" class="btn btn-primary" role="button">Check Reply</a>
        </p>
      </div>
    </div>
  </div>
</div>    
eof


                }



            }
            else{
                my $path = $bleats_dir;
                opendir (B, $bleats_dir) or die "can't open $path";
                while (my $file = readdir(B)) {
                    my $bpath = $path.'/'.$file;
                    open($p, $bpath) or die "can't open $bpath";
                    while (my $line=<$p>) {
                        if ($line =~ /^in_reply_to/) {
                            last;
                        }
                        if ($line =~ /^bleat/) {
                            $line =~ s/^blest://;
                            if ($line =~ $re) {
                                push(@bleat, $file);
                                last;
                            }
                        }
                    }
                }

            }
        }
    }
}



#
# HTML placed at the top of every page
#<link href="css/bootstrap.css" rel="stylesheet" type="text/css">
sub login_page_header {
    return <<eof
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<link href="bitter.css" rel="stylesheet" type="text/css">
<link href="css/bootstrap.css" rel="stylesheet" type="text/css">

</head>
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="bitter.cgi">Cytter</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav navbar-right">
        <form class="navbar-form navbar-left" role="search" action="search.cgi">
        <div class="form-group">
          <input type="text" name="search" class="form-control" placeholder="Search">
        </div>
        <button type="submit" class="btn btn-default">Search</button>
        </form>
        <li><a href="bitter.cgi">Login</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<body>
</body>
eof
}

sub user_header {
    my $path = $users_dir."/".$user."/profile.jpg";
    return <<eof
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<link href="css/bootstrap.css" rel="stylesheet" type="text/css">
<link href="bitter.css" rel="stylesheet" type="text/css">
<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

</head>
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="bitter.cgi">Cytter</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav navbar-right">
        <form class="navbar-form navbar-left" role="search">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search">
        </div>
        <button type="submit" class="btn btn-default">Search</button>
      </form>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span class="caret"></span>
          <img alt="profile" src="$path" height="20" width="20">
          </a>
          <ul class="dropdown-menu">
            <li><a href="#">Action</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="bitter.cgi?logout=1">Logout</a></li>
          </ul>
        </li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<body>
</body>
eof
}


# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}

main();

