#!/usr/local/bin/perl 

##  2010/09/07  Hans  Replace aleph@itd.umd.edu with usmaialeph@umd.edu

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
$id = "";



print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD>\n<TITLE>RxWeb Reports</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
print "<FORM ACTION=\"ALEPHxreply.cgi\" METHOD=\"post\">\n";
print "<center>\n";
print "<H1>RxWeb Reply</H1>\n";
print "<INPUT TYPE=\"button\" VALUE=\"RxWeb Form\" onClick=\"parent.location='\/cgi-bin\/ALEPHform.cgi'\">\n";
print "<INPUT TYPE=\"button\" VALUE=\"RxWeb\" onClick=\"parent.location='ALEPHsum.cgi?id'\">\n";
print "<br><br>\n";
print "<TABLE BORDER=0 CELLPADDING=2>\n";




$value = $ENV{'QUERY_STRING'};

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);


$statement =   "SELECT people.id, report.summary, people.name, people.phone, DATE_FORMAT(report.date,'%m/ %d/%y'), people.grp, people.campus, report.status, report.text, people.email FROM people, report WHERE people.id = $value and people.id = report.id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

while (@row = $sth->fetchrow_array) {
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
    $grp = $row[5];
    $email = $row[9];
    $row_id = $row[0];
#        &fetchresponse(); # fetch the response
    print "</TR>\n";
    &fetchreply();    # fetch the replies
    print "</TR>\n";
    print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
}


$rc = $sth->finish;
$rc = $dbh->disconnect;
print "</TABLE>\n";
print "<FONT>Complete the form and configure email options below</FONT>\n";
print "<BR>\n";
print "<P>Name:&nbsp;&nbsp;<INPUT TYPE=\"text\" NAME=name SIZE=20 MAXSIZE=30></P>\n";
print "<P>Reply:&nbsp;&nbsp;<textarea wrap=\"physical\" name=reply cols=60 rows=5></textarea></P>\n";

print "<INPUT TYPE=\"hidden\" name=\"record_id\" VALUE=\"$value\">\n";
#print "&nbsp;&nbsp;<B>Email Reply?</B>\n";
#print "<INPUT TYPE=\"radio\" NAME=\"email\" VALUE=\"yes\" checked>Yes\n";
#print "<INPUT TYPE=\"radio\" NAME=\"email\" VALUE=\"no\">No<br><br>\n";
print "<input type=submit value=\"Submit Your Reply\">\n";
print "<br><br>\n";
&recipient;
&email_display;
print "</FORM>\n";
print "</BODY>\n</HTML>\n";





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



sub fetchresponse {


    $dbh_2 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_2 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from response where parent_id = '$row_id'";

    $sth_2 = $dbh_2->prepare($statement_2)
        or die "Couldn't prepare the query: $sth_2->errstr";

    $rv_2 = $sth_2->execute
        or die "Couldn't execute the query: $dbh_2->errstr";

    while (@row = $sth_2->fetchrow_array) {
        if ($row[0] eq "") {
        }else{
            print "<TR>\n";
            print "<TD COLSPAN=2 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><i><FONT SIZE=-1 COLOR=\"#A52A2A\">&nbsp;ITD Response from:&nbsp;\n";
            print "$row[0]</TD>\n";
            print "<TD COLSPAN=4 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"#A52A2A\"><i>Date:&nbsp;$row[1]&nbsp;&nbsp;&nbsp;</TD>\n";
            print "<TD COLSPAN=1 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"#A52A2A\"><i>&nbsp;$row[2]</TD>\n";
            print "</TR>\n";
        }
        $rc_2 = $sth_2->finish;
        $rc_2 = $dbh_2->disconnect;
    }
}



sub reply_type {

    if ($itd eq "yes") {
        $reply_type = "ITD Response";
        $font_color = "DarkRed";
    } else {
        $reply_type = "Reply";
        $font_color = "DarkBlue";
    }
}


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

#    print "<tr><td>Community of interest: $grp</td></tr>\n";
#    print "<tr><td>     Individual email: $email</td></tr>\n";
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
    print "<INPUT TYPE=\"hidden\" name=\"recipient\" VALUE=\"$recipient\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"cataloger\" VALUE=\"$cataloger\">\n";
    print "</form>\n";
    print "</td></tr></table>\n";
    print "</body>\n</html>\n";
}



sub email_options {

    if ($email1) {
        $rec1 = "$recipient";
    }

    if ($email2) {
        $rec2 = ",$email";
    }

    if ($email3) {
        $rec3 = ",$email3a";
    }

    if ($email4) {
        $rec4 = ",$email4a";
    }

#    $final_email_list = $rec1 . $rec2 . $rec3 . $rec4;

}




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

    if ($grp eq "Change request") {
        $recipient = "usmaialeph\@umd.edu";
    }

    if ($grp eq "other") {
        $recipient = "usmaialeph\@umd.edu";
    }

    if ($grp eq "Report request") {
        $recipient = "usmaialeph\@umd.edu";
    }

    if ($grp eq "ILL") {
        $recipient = "ilug\@umd.edu,usmaicoicircresill\@umd.edu";
    }


}


sub email_display {


    print "<TABLE border=\"0\" width=\"50%\">\n";
    print "<tr><td colspan=\"2\" align=\"left\"><b>Email Options:</b></td></tr>\n";
    print "<tr><td colspan=\"2\"><hr></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email1\" VALUE=\"email1\" checked>Community:&nbsp;&nbsp;<cite><b>$recipient</b></cite></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email2\" VALUE=\"email2\" checked>Reported by:&nbsp;&nbsp;<b><cite>$email</b></cite></td></tr>\n";

    print "<tr><td><INPUT TYPE=\"checkbox\" NAME=\"email3\" VALUE=\"email3\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email3a\"  cols=50 maxlength=50></td></tr>\n";
    print "<tr><td width=\"120\"><INPUT TYPE=\"checkbox\" NAME=\"email4\" VALUE=\"email4\">Additional email</td>\n";

    print"<td><INPUT TYPE=\"text\" NAME=\"email4a\"  cols=50 maxlength=50></td></tr>\n";
    print "<tr><td colspan=\"2\"><HR></td></tr>\n";
    print "<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Additional Community</td>\n";
    print "<td><select name=\"email5\" size=1>\n";
    print "<option>\n";
    print "<option>usmaicoiseracq\@umd.edu\n";
    print "<option>usmaicoicircresill\@umd.edu\n";
    print "<option>usmaicoicatdbmaint\@umd.edu\n";
    print "<option>usmaicoidesktech\@umd.edu\n";
    print "<option>usmaicoiuserinter\@umd.edu\n";
    print "<option>usmaicoiall\@umd.edu\n";
    print "<option>usmaialeph\@umd.edu\n";
#    print "<option>jamieb\@kitabu.umd.edu\n";
    print "</select></td>\n";
    print "</tr>\n";

    print "</TABLE><br>\n";

}
