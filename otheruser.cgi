#!/usr/bin/perl -w

#
#Yusa Written by Chenyu Li Z3492794 
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
    my $warning = "";
    $lookinguser = param('follow');

    # check if the logout is set
    $sign = param('logout') || '';
    $send = param('sendmessage') || '';

    # create the session
    $cgi = new CGI;
    $sid = $cgi->cookie("CGISESSID") || undef;
    $session = new CGI::Session(undef, $sid, {Directory=>'/tmp'}) || undef;
 
    # if logout button press, do the seesion delete
    if ($sign == 1) {
        $session->delete();
    }
    # loading the session of userid
    $user= $session->param("id") || ''; 
    $pwd = $session->param("pwd") || '';


    $warning = check();
    

    # print each part of page
    if ($user eq '' or $sign == 1) {
    print login_page_header();
    $column1 = 'bitter';
    $column2 = 'follower';
    $column3 = 'following';
    user_page();
    print page_trailer();
    }
    else{
    $column1 = 'bitter';
    $column2 = 'follower';
    $column3 = 'following';
    print user_header();

#     print <<eof;
#     <ol class="breadcrumb">
#   <li><a href="bitter.cgi?show=$column1&page=1">Bitter</a></li>
#   <li><a href="bitter.cgi?show=$column3&page=1"">Following</a></li>
# </ol>
# eof
        user_page();
        print page_trailer();
    }

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
            print header(-refresh => "1; url=bitter.cgi?show=bitter&page=1",-cookie => $cookie);
            exit;

        }
        else
        {
            return "Please check your password";
        }


    }
    
}


#
# Logout function for user to log out 
#
#
sub logout_button
{
    my $html = "";
    $html .= start_form();
    $html .= "<input type=\"hidden\" name=\"logout\" value=\"1\">";
    $html .= submit(value => Logout);
    $html .= end_form();
    return $html;
}


#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
    # this part for user detail
    my @time;
    my $username = param('follow');
    my $path = $users_dir."/".$username;
    my $details_filename = $path."/details.txt";
    my $listening = "";
    open my $p, "$details_filename" or die "can not open $details_filename: $!";
    while (<$p>){
        if ($_ =~ /^listens/) {
            $listening = $_;
        }
    }
    close $p;
    open my $p, "$details_filename" or die "can not open $details_filename: $!";
    $details = join '', <$p>;
    close $p;
    if ($user ne '') {
        my $userfollowing = "";
        my $mypath = $users_dir.'/'.$user.'/details.txt';  
        open $mp, $mypath or die "can not open such file $path $!";
        while (my $line = <$mp>) {
            if ($line =~ /^listen/) {
                $userfollowing = $line;
            }
        }
        my $path = $users_dir."/".$username;
        if ($userfollowing =~ $lookinguser) {
   print <<eof;
<div class="myprofile">
<div class="myimg">
<img src="$path/profile.jpg" width="70" height="100">
<h3 class="myh3">$username</h3>
</div>
<div class="send_beatter">
<form>
<p>
<div class="dropdown">
  <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
    Following
    <span class="caret"></span>
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
    <li><a href="bitter.cgi?show=following&page=1&unfollow=$username">Unfollow</a></li>
  </ul>
</div>
</form>
</div>
</div>
eof
        }
        else{

 print <<eof;
<div class="myprofile">
<div class="myimg">
<img src="$path/profile.jpg" width="70" height="100">
<h3 class="myh3">$username</h3>
</div>
<div class="send_beatter">
<div class="dropdown">
  <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
    Unfollow
    <span class="caret"></span>
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
    <li><a href="bitter.cgi?show=following&page=1&following=$username">Follow</a></li>
  </ul>
</div>
</div>
</div>
eof

        }

}
else{
    my $path = $users_dir."/".$username;
print <<eof;
<div class="myprofile">
<div class="myimg">
<img src="$path/profile.jpg" width="70" height="100">
<h3 class="myh3">$username</h3>
</div>
<div class="send_beatter">
<form>
<p>
</form>
</div>
</div>
eof

}

    print <<eof;
    <ol class="breadcrumb">
  <li><a href="otheruser.cgi?show=$column1&follow=$lookinguser&page=1">Bitter</a></li>
  <li><a href="otheruser.cgi?show=$column3&follow=$lookinguser&page=1">Following</a></li>
</ol>
eof
    # Add full bleats timeline 
    open my $b, "$path/bleats.txt" or die "can not open bleats file $!";
    while (<$b>) {
        push(@time, $_);
    }
    close $b;
    $listening =~ s/^listens://;
    @listen = split / /, $listening;

#
# paging the bitter only this specil user following
#
#
    if (param('show') eq 'bitter') {
    
        my $num = 10; # xx items per page
        my $total = 0; 
        my $con = 0; #count the number
        my $con_reply = 0; # count the number of reply
        my $page = param('page');
        my $lowbond = ($page - 1) * $num ;
        my $highbond = $page * $num;
        my $bit = "";
        my $tim = "";
        my $us = "";
        foreach (reverse sort @time) {
            $con += 1;
            my $flag = 0; #if the bleat is reply bleat skip it and set flag to 1
            open my $b, $bleats_dir.'/'.$_ or die "can not open bleats file $!";
            my $idnum = $_;
            while (<$b>) {
                if ($_ =~ /^bleat/) {
                    $bit = $_;
                }
                if ($_ =~ /^time/) {
                    $tim = $_;
               }
                if ($_ =~ /^username/) {
                    $us = $_;
                }
                if ($_=~ /^in_reply_to/) {
                    $flag = 1;
                    $con = $con - 1;
                }
           }
           if ($flag == 1) {
               $con_reply = $con_reply + 1;
               next;
           }
            if ($con < $lowbond ) {
                next;
            }
            if ($con > $highbond) {
                next;
            }
            $tim =~ s/time: //;
            my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($tim);
            my $format_time=sprintf("%d-%d-%d %d:%d:%d",$year+1900,$mon+1,$mday,$hour,$min,$sec);
           $us =~ s/^username: //;
           $bit =~ s/^bleat: //;
           $bit =~ s/bleats: //;
           my $profile_path = $users_dir.'/'.$us.'/profile.jpg';
print <<eof
<div class="row">
  <div class="mybleat">
    <div class="thumbnail">
      <img src="$profile_path" height="45" width="45">
      <div class="caption">
        <h3>$us</h3>
        <p>$bit</p>
        <p>$format_time</p>
        <p><a href="reply.cgi?messageid=$idnum" class="btn btn-primary" role="button">Check Reply</a>
        </p>
      </div>
    </div>
  </div>
</div>    
eof
        }
        my $count = @time;
        my $count = $count - $con_reply;
        # paging
        if ($count % $num) {
        $total = int($count/$num);
        }
        else {
        $total = $count / $num ;
        }
        if ($page == 1){
print <<eof;
<div class="mybleat">
<nav>
  <ul class="pagination">
eof
    foreach (1..$total+1)
    {
        print <<eof
<li><a href="otheruser.cgi?show=bitter&page=$_&follow=$lookinguser">$_</a></li>
eof
    }
    my $next = $page + 1;
    print <<eof
    <li>
      <a href="otheruser.cgi?show=bitter&page=$next&follow=$lookinguser" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
</div>
eof
        }

        elsif($page == $total + 1){
        my $previous = $page - 1;
print <<eof;
<div class="mybleat">
<nav>
  <ul class="pagination">
    <li>
      <a href="otheruser.cgi?show=bitter&page=$previous&follow=$lookinguser" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
eof
    foreach (1..$total+1)
    {
        print <<eof
<li><a href="otheruser.cgi?show=bitter&page=$_&follow=$lookinguser">$_</a></li>
eof
    }
    print <<eof
  </ul>
</nav>
</div>
eof
        }
        else{
        my $previous = $page - 1;
print <<eof;
<div class="mybleat">
<nav>
  <ul class="pagination">
    <li>
      <a href="#" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
eof

    foreach (1..$total+1)
    {
        print <<eof
<li><a href="otheruser.cgi?show=bitter&page=$_&follow=$lookinguser">$_</a></li>
eof
    }
    my $next = $page + 1;
    print <<eof
    <li>
      <a href="otheruser.cgi?show=bitter&page=$next&follow=$lookinguser" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
</div>
eof
        }

    }

# 
#
#
# paging the the person the user following
#
#
    elsif (param('show') eq 'following') {
        my $num = 9; # xx items per page
        my $total = 0; 
        my $con = 0; #count the number
        my $page = param('page');
        my $lowbond = ($page - 1) * $num ;
        my $highbond = $page * $num;
        my $space = 0; #count the '' situation in array
        @listen = split / /, $listening;
        foreach my $follow (@listen)
        {
            my $un; #username
            my $hs = ""; #user address
            if ($follow eq ''){
                $space += 1;
            next;
            }
            $con += 1;
            if ($con > $highbond) {
                next;
            }
            if ($con < $lowbond){
                next;
            }
            my $name = $follow;
            $name =~ s/^\s+//g;
            $name =~ s/\s+$//g;
            my $followpath = $users_dir.'/'.$name.'/details.txt';
            open $fd, $followpath or die "can't open this file path is $followpath $!";
            while (<$fd>) {
                if ($_ =~ /^username/) {
                    $un = $_;
                }
                if ($_ =~ /^home_suburb/) {
                    $hs = $_
                }
            }
            $un =~ s/^username: //;
            if ($hs eq '') {
                $hs = "No area record";
            }
            else{
                $hs =~ s/^home_suburb: //;
            }
           my $profile_path = $users_dir.'/'.$name.'/profile.jpg';
print <<eof
<div class="row">
  <div class="mybleat">
    <div class="thumbnail">
     <a href="otheruser.cgi?show=bitter&follow=$un&page=1"><img src="$profile_path" height="45" width="45"></a>
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
        my $count = @listen;
        my $count = $count - $space;
        # paging
        if ($count % $num) {
        $total = int($count/$num);
        }
        else {
        $total = $count / $num ;
        }
        if ($page == 1){
            if ($total == 0){
print <<eof;
<div class="mybleat">
<nav>
  <ul class="pagination">
<li><a href="otheruser.cgi?show=following&page=1&follow=$lookinguser">1</a></li>
  </ul>
</nav>
</div>
eof
            }
else{
print <<eof;
<div class="mybleat">
<nav>
  <ul class="pagination">
eof
    foreach (1..$total + 1)
    {
        print <<eof
<li><a href="otheruser.cgi?show=following&page=$_&follow=$lookinguser">$_</a></li>
eof
    }
    my $next = $page + 1;
    print <<eof
    <li>
      <a href="otheruser.cgi?show=following&page=$next&follow=$lookinguser" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
</div>
eof
}
        }
        elsif($page == $total + 1){

        my $previous = $page - 1;
print <<eof;
<div class="mybleat">
<nav>
  <ul class="pagination">
    <li>
      <a href="otheruser.cgi?show=following&page=$previous&follow=$lookinguser" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
eof
    foreach (1..$total + 1)
    {
        print <<eof
<li><a href="otheruser.cgi?show=following&page=$_&follow=$lookinguser">$_</a></li>
eof
    }
    print <<eof
  </ul>
</nav>
</div>
eof
        }
        else{

        my $previous = $page - 1;
print <<eof;
<div class="mybleat">
<nav>
  <ul class="pagination">
    <li>
      <a href="#" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
eof

    foreach (1..$total + 1)
    {
        print <<eof
<li><a href="otheruser.cgi?show=following&page=$_&follow=$lookinguser">$_</a></li>
eof
    }
    my $next = $page + 1;
    print <<eof
    <li>
      <a href="otheruser.cgi?show=following&page=$next&follow=$lookinguser" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
</div>
eof
        }


    }



}




main();


#
# HTML placed at the top of every page
#<link href="css/bootstrap.css" rel="stylesheet" type="text/css">
sub login_page_header {
    return <<eof
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<link href="css/bootstrap.css" rel="stylesheet" type="text/css">
<link href="bitter.css" rel="stylesheet" type="text/css">
<link href="css/bootstrap.min.css" rel="stylesheet" type="text/css">
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
        <form class="navbar-form navbar-left" role="search" action="search.cgi">
        <div class="form-group">
          <input type="text" name="search" class="form-control" placeholder="Search">
          <input type="hidden" name="mode" value="user">
        </div>
        <button type="submit" class="btn btn-default">Search</button>
        </form>
            <li><a href="bitter.cgi">Login</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<body bgcolor="#000000">
<div>
eof
}


# <li>
# <a>
# <form action="">
# <input type="hidden" name="logout" value="1">
# <button type="button" style="background-color:Transparent;border-color:Transparent;border-style:None;" >
# Logout
# </button>
# </a>
# </li>

sub user_header {
    my $path = $users_dir."/".$user."/profile.jpg";
    return <<eof
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<link href="css/bootstrap.css" rel="stylesheet" type="text/css">
<link href="bitter.css" rel="stylesheet" type="text/css">
<link href="css/bootstrap.min.css" rel="stylesheet" type="text/css">
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
        <form class="navbar-form navbar-left" role="search" action="search.cgi">
        <div class="form-group">
          <input type="text" name="search" class="form-control" placeholder="Search">
          <input type="hidden" name="mode" value="user">
        </div>
        <button type="submit" class="btn btn-default">Search</button>
      </form>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span class="caret"></span>
          <img alt="profile" src="$path" height="20" width="20">
          </a>
          <ul class="dropdown-menu">
            <li><a href="#">Action</a></li>
            <li><a href="#">Another action</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="bitter.cgi?logout=1">Logout</a></li>
          </ul>
        </li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<body>
<div>
eof
}


# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
sub page_trailer {
    my $html = "</div>";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}
