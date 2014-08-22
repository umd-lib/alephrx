#!/usr/local/bin/perl 

## 2010/09/07  Hans  Replace aleph@itd.umd.edu with usmaialeph@umd.edu


use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$nameid = "";
$mailprog = $ENV{ALEPHRX_MAILER};
$from = "usmaialeph\@umd.edu (RxWeb)";
$replies = "replies.dat";
@store = ();

$input_size = $ENV { 'CONTENT_LENGTH' };
read ( STDIN, $form_info, $input_size );
@input_pairs = split (/[&;]/, $form_info);


%input = ();

foreach $pair (@input_pairs) {
  #Convert plusses to spaces
  $pair =~ s/\+/ /g;

  #Split the name and value pair
  ($name, $value) = split (/=/, $pair);

  #Decode the URL encoded name and value 
  $name =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;   
  $value =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;   

  #Escape the single quotes 
#  $value =~ s/\'/\\\'/g;
  #Escape the backslashes
#  $value =~ s/\\/\\\\/g;

  #Copy the name and value into the hash
  $input{$name} = $value;
}




$parent_id = $input{'record_id'};
$name = $input{'name'};
$text = $input{'reply'};
$email = $input{'email'};
$email1 = $input{'email1'};
$email2 = $input{'email2'};
$email3a = $input{'email3a'};
$email4a = $input{'email4a'};
$email3 = $input{'email3'};
$email4 = $input{'email4'};
$email5 = $input{'email5'};


if ($email3) { &Check_Email($email3a);}
if ($email4) { &Check_Email($email4a);}

if ($email_check > 0) {
    &bad_email_display;

} else {

if ($text eq "") {

&validate_reply();

} else {


$name =~ s/\\/\\\\/g;
$name =~ s/\'/\\\'/g;
$text =~ s/\\/\\\\/g;
$text =~ s/\'/\\\'/g;


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "INSERT INTO reply (parent_id, name, date, text, itd) VALUES 
               ('$parent_id','$name', NOW(), '$text', 'no')";

#$query1 = $statement;
#&mail_query;


$sth = $dbh->prepare($statement)
	or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	or die "Couldn't execute the query: $dbh->errstr";



$statement =   "UPDATE report set updated = NOW() where id = '$parent_id'";


$sth = $dbh->prepare($statement)
	or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	or die "Couldn't execute the query: $dbh->errstr";




print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD>\n<TITLE>RxWeb</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
print "<FORM ACTION=\"XREPLY.cgi\" METHOD=\"post\">\n";
print "<center>\n";
print "<H1>RxWeb Reply</H1>\n";
print "<INPUT TYPE=\"button\" VALUE=\"RxWeb Form\" onClick=\"parent.location='\/cgi-bin\/ALEPHform.cgi'\">\n";
print "<INPUT TYPE=\"button\" VALUE=\"RxWeb\" onClick=\"parent.location='ALEPHsum.cgi?id'\"></p>\n";
print "<TABLE BORDER=0 CELLPADDING=2>\n";


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);


$statement =   "SELECT people.id, report.summary, people.name, people.phone, DATE_FORMAT(report.date,'%m/%d/%y'), people.grp, people.campus, report.status, report.text, people.email FROM people, report WHERE people.id = $parent_id and people.id = report.id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

while (@row = $sth->fetchrow_array) {
        print " <TR><TD COLSPAN=7 ALIGN=RIGHT VALIGN=TOP><a href=\"ALEPHreply.cgi?$row[0]\">Reply to This Report</a></FONT></TD></TR>\n";
        print "<TR><TD BGCOLOR=\"#FFFF00\" COLSPAN=7><B><i>Report #</i>&nbsp;$row[0]&nbsp;&nbsp;&nbsp;&nbsp;$row[1]</B></TD></FONT></TR>\n";

         print "<TR>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Name</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Phone</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Date</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Group</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Campus</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Status</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Text</I></TH>\n";

        print "<TR>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[2]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[3]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[4]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[5]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[6]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[7]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[8]</TD>\n";
        $row_id = $row[0];
	$ssummary = $row[1];
	$sname = $row[2];
	$sphone = $row[3];
	$sdate = $row[4];
	$grp = $row[5];
	$scampus = $row[6];
	$sstatus = $row[7];
	$stext = $row[8];
	$email = $row[9];

#        &fetchresponse(); # fetch the response
        print "</TR>\n";
        &fetchreply();    # fetch the replies
        print "</TR>\n";
        print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
    }


$rc = $sth->finish;
$rc = $dbh->disconnect;

print "</TABLE>\n";
print "<BR><BR>\n";
print "</FORM>\n";
&recipient;
&slug;
print "$email_check<br>\n";
&email_options;
#print "$final_list\n";
print "</BODY>\n</HTML>\n";
&reply_date;
if ($email_count > 0) {
&mail;
}
}
}






sub fetchreply {

    $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text, itd from reply where parent_id = '$row_id' ORDER BY date DESC";
$sth_1 = $dbh_1->prepare($statement_1)
    or die "Couldn't prepare the query: $sth_1->errstr";

$rv_1 = $sth_1->execute
    or die "Couldn't execute the query: $dbh_1->errstr";

    while (@rrow = $sth_1->fetchrow_array) {

	$rrow[2] =~ s/\n/<BR>/g;
	$itd = $rrow[3];
	&reply_type;
	print "<TR>\n";
	print "<TD COLSPAN=2 BGCOLOR=\"#E8E8E8\" VALIGN=TOP><i><FONT SIZE=-1 COLOR=\"$font_color\">&nbsp;$reply_type from:&nbsp;\n";
	print "$rrow[0]</TD>\n";
	print "<TD COLSPAN=4 BGCOLOR=\"#E8E8E8\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"$font_color\"><i>Date:&nbsp;$rrow[1]&nbsp;&nbsp;&nbsp;</TD>\n";
	print "<TD COLSPAN=1 BGCOLOR=\"#E8E8E8\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"$font_color\"><i>&nbsp;$rrow[2]</TD>\n";
	print "</TR>\n";
    }
    $rc_1 = $sth_1->finish;
    $rc_1 = $dbh_1->disconnect;
}






sub validate_reply {

     print "Content-type:  text/html\n\n";
     print "<html>\n<head>\n";
     print "<title>RxWeb Report Reply</title>\n";
     print "</head>\n<body>\n";
     print "<center>\n";
     print "<h1>RxWeb Reply</h1>\n";
     print "<h3>Please enter a reply.</h3>\n";
     print "<table>\n";
     print "<tr><td align=\"left\">\n";
     print "<UL>\n" , $error_message , "</UL>\n";
     print "</td></tr></table>\n";
     print "<SCRIPT=\"Javascript\">\n";
     print "<form>\n";
     print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
     print "</form>\n";
     print "</body>\n</html>\n";

 }


sub bad_email_display {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Reply</title>\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<h1>RxWeb Reply</h1>\n";
    print "<h3>Not a valid email address.</h3>\n";
    print "$final_list\n";
    print "<table>\n";
    print "<tr><td><cite><font size=+1>\n";

foreach $store (@store) {
    print "$store<br>\n";
    }

    print "</cite></font></td></tr></table>\n";
    print "<SCRIPT=\"Javascript\">\n";
    print "<form>\n";
    print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
    print "</form>\n";
    print "</body>\n</html>\n";

}


sub mail {

#removes the escape from single quote

$text =~ s/\\'/\'/g;
$name =~ s/\\'/\'/g;
$stext =~ s/\\'/\'/g;
$sname =~ s/\\'/\'/g;
$ssummary =~ s/\\'/\'/g;


    if ($emailx eq "yes") {
	open (MAIL,"|$mailprog -t");
        print MAIL <<END;
To: $final_list
Bcc: usmaialeph\@umd.edu
From: $from
Subject: REPLY:$slug#$row_id:$ssummary

--------------------------------------------------------------------------------
Please do not reply directly to this e-mail. 
To REPLY to this Rx: http://www.itd.umd.edu/cgi-bin/ALEPH16/ALEPHreply.cgi?$row_id
(If prompted, sign in with the standard USMAI username/password.)
--------------------------------------------------------------------------------

This is a REPLY to the RxWeb listed below:

  Original Report # : $row_id
   Date of Report # : $sdate
    Functional Group: $grp
              Status: $sstatus

END

        $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text, itd from reply where parent_id = '$row_id' ORDER BY date DESC";
        $sth_1 = $dbh_1->prepare($statement_1)
            or die "Couldn't prepare the query: $sth_1->errstr";

        $rv_1 = $sth_1->execute
            or die "Couldn't execute the query: $dbh_1->errstr";

        while (@row = $sth_1->fetchrow_array) {
            $itd = $row[3];
            &reply_type;
            print MAIL <<END;
 $reply_type submitted by: $row[0]
       Date/Time submitted: $row[1]
                     Reply: $row[2]

-----------------------------------------------
END
        }
        $rc_1 = $sth_1->finish;
        $rc_1 = $dbh_1->disconnect;

        print MAIL <<END;

Original Report by: $sname
   Original Report: $stext

-----------------------------------------------

===================================================================================
View this Rx online: http://www.itd.umd.edu/cgi-bin/ALEPH16/ALEPHsum_full.cgi?$row_id
END
        close (MAIL);
        $row_id = "";
    } 
}



sub reply_date {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "SELECT date from reply where parent_id = $parent_id";

$sth_6 = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth_6->errstr";
$rv_6 = $sth_6->execute
    or die "Couldn't execute the query: $dbh->errstr";

    while (@row = $sth_6->fetchrow_array) {
	$rdate = $row[0];
    }
    $rc_6 = $sth_6->finish;
    $rc_6 = $dbh->disconnect;
}



sub mail_query {

    open (MAIL,"|$mailprog -t");
    print MAIL "To: jamieb\@kitabu.umd.edu\n";
    print MAIL "From: $from\n";
    print MAIL "Subject: #query\n";
    print MAIL "$query1\n";
    print MAIL "$query2\n";
    print MAIL "$query3\n";
    close (MAIL);
}






sub reply_type {

    if ($itd eq "yes") {
        $reply_type = "ITD Response";
        $font_color = "DarkRed";
    } else {
        $reply_type = "       Reply";
        $font_color = "DarkBlue";
    }
}



###########################################

sub email_config {


    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Email Configuration</title>\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</head>\n<body bgcolor=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>RxWeb Email Configuration</h1>\n";
    print "<h3>Please confirm the Email configuration for your report </h3>\n";
    print "<table>\n";

    &email_display;

    print "<tr><td align=\"left\">\n";
    print "<FORM ACTION=\"\/cgi-bin\/ALEPHform.cgi\" METHOD=\"post\">\n";
    print "<p><input TYPE=\"submit\" VALUE=\"Confirm Email Configuration\"></p>\n";
    print "<INPUT TYPE=\"hidden\" name=\"email_config\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"name\" VALUE=\"$name\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"text\" VALUE=\"$text\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"summary\" VALUE=\"$summary\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"phone\" VALUE=\"$phone\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"campus\" VALUE=\"$campus\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"status\" VALUE=\"$status\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"grp\" VALUE=\"$grp\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"email\" VALUE=\"$email\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"cataloger\" VALUE=\"$cataloger\">\n";
    print "</form>\n";
    print "</td></tr></table>\n";
    print "</body>\n</html>\n";


}





sub email_options {


    if ($email1) {
	$email_count++;
        $recipient =~ s/\s+//g;         
        $rec1 = "$recipient";
        
	$emailx = 'yes';
    }

    if ($email2) {
	$email_count++;
        $email =~ s/\s+//g;
        $rec2 = ",$email";
	$emailx = 'yes';
    }

    if ($email3) {
	$email_count++;
        $email3a =~ s/\s+//g; 
        $rec3 = ",$email3a";
	$emailx = 'yes';
    }

    if ($email4) {
	$email_count++;
        $email4a =~ s/\s+//g; 
        $rec4 = ",$email4a";
	$emailx = 'yes';
    }

    if ($email5) {
	$rec5 = ",$email5";
	$email_count++;
	$emailx = 'yes';
    }

    $final_list = $rec1 . $rec2 . $rec3 . $rec4 . $rec5;
}


sub Check_Email 

{
    #removes whitespace before validation
#    $email =~ s/\s+//g;    
#    $email3a =~ s/\s+//g;
#    $email4a =~ s/\s+//g;
#    (\w[-._\w]*\w@\w[-._\w]*\w\.\w{2,3})
#    ^[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]@[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,4}$

#    if ($_[0] =~ /(\w[-._\w]*\w@\w[-._\w]*\w\.\w{2,3})/) { $email_check++; push @store, $_[0]; }
#    else { }
# }


#    if ($_[0] =~ /(\d+)/) { $email_check++; push @store, $_[0]; }
#    else { }
#    }

     if ($_[0] =~ /(@.*@)|(,)|\s+|(\.\.)|(@\.)|(\.@)|(^\.)|(\.$)|(^\d+)|(\d+$)/ || ($_[0] !~ /^.+\@localhost$/ && $_[0] !~ /^.+\@\[?(\w|[-.])+\.[a-zA-Z]{2,3}|[0-9]{1,3}\]?$/))             { $email_check++; push @store, $_[0]; }
	else { }
    }



#     if ($_[0] =~ /(@.*@)|(,)|\s+|(\.\.)|(@\.)|(\.@)|(^\.)|(\.$)/)             { $email_check++; push @store, $_[0]; }
#	else { }
#    }




sub recipient {

if ($grp eq "Circulation") {
    $recipient = "usmaicoicircresill\@umd.edu";
}
if ($grp eq "Technical") {
    $recipient = "usmaicoidesktech\@umd.edu";
}
if ($grp eq "Web OPAC") {
    $recipient = "usmaicoiuserinter\@umd.edu";
}

if ($grp eq "Cataloging") {
    $recipient = "usmaicoicatdbmaint\@umd.edu";
}

if ($grp eq "Serials") {
    $recipient = "usmaicoiseracq\@umd.edu";
}

if ($grp eq "Acquisitions") {
    $recipient = "usmaicoiseracq\@umd.edu";
}

if ($grp eq "Item Maintenance") {
    $recipient = "usmaicoicircresill\@umd.edu,usmaicoicatdbmaint\@umd.edu,usmaicoiseracq\@umd.edu";
}

if ($grp eq "Reserves") {
    $recipient = "usmaicoicircresill\@umd.edu,usmaicoiuserinter\@umd.edu";
}

if ($grp eq "ILL") {
    $recipient = "ilug\@umd.edu,usmaicoicircresill\@umd.edu";
}


if ($grp eq "other") {
    $recipient = "usmaialeph\@umd.edu";
}

if ($grp eq "Report request") {
    $recipient = "usmaialeph\@umd.edu";
}
if ($grp eq "Change request") {
    $recipient = "usmaialeph\@umd.edu";
}
}



sub slug {

if ($grp eq "Circulation") {
    $slug = "CIRC:";
}
if ($grp eq "Technical") {
    $slug = "TECH:";
}
if ($grp eq "Web OPAC") {
    $slug = "OPAC:";
}

if ($grp eq "Cataloging") {
    $slug = "CAT:";
}

if ($grp eq "Serials") {
    $slug = "SER:";
}

if ($grp eq "Acquisitions") {
    $slug = "ACQ:";
}

if ($grp eq "Item Maintenance") {
    $slug = "ITM:";
}

if ($grp eq "Reserves") {
    $slug = "RES:";
}

if ($grp eq "ILL") {
    $slug = "ILL:";
}


if ($grp eq "other") {
    $slug = "OTHR:";
}

if ($grp eq "Report request") {
    $slug = "RQST:";
}
}















