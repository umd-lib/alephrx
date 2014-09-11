#!/usr/local/bin/perl 

=head1 NAME

ALEPHreply.cgi - User reply form

=cut

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

# the report ID is given by the query string
$value = $ENV{'QUERY_STRING'};

# print the HTTP header and the beginning of the page
print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD>\n<TITLE>Reply to Report #$value - AlephRx</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
print "<FORM ACTION=\"ALEPHxreply.cgi\" METHOD=\"post\">\n";
print "<center>\n";
print "<H1>AlephRx Reply to Report #$value</H1>\n";
print "<INPUT TYPE=\"button\" VALUE=\"Submit a Report\" onClick=\"parent.location='../ALEPHform.cgi'\">\n";
print "<INPUT TYPE=\"button\" VALUE=\"View Reports\" onClick=\"parent.location='ALEPHsum.cgi?id'\">\n";
print "<br><br>\n";
print "<TABLE BORDER=0 CELLPADDING=2>\n";

# get the full record for this report
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password, { RaiseError => 1 });

$statement =   "SELECT people.id, report.summary, people.name, people.phone, DATE_FORMAT(report.date,'%m/ %d/%y'), people.grp, people.campus, report.status, report.text, people.email FROM people, report WHERE people.id = ? and people.id = report.id";
$sth = $dbh->prepare($statement);
$sth->execute($value);

# display the full record
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
    print "</TR>\n";
    # fetch the replies
    &fetchreply();
    print "</TR>\n";
    print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
}

$sth->finish;
$dbh->disconnect;
print "</TABLE>\n";
print "<FONT>Complete the form and configure email options below</FONT>\n";
print "<BR>\n";
print "<P>Name:&nbsp;&nbsp;<INPUT TYPE=\"text\" NAME=name SIZE=20 MAXSIZE=30></P>\n";
print "<P>Reply:&nbsp;&nbsp;<textarea wrap=\"physical\" name=reply cols=60 rows=5></textarea></P>\n";

print "<INPUT TYPE=\"hidden\" name=\"record_id\" VALUE=\"$value\">\n";
print "<br><br>\n";
&recipient;
&email_display;
print "<input type=submit value=\"Submit Your Reply\">\n";
print "</FORM>\n";
print "</BODY>\n</HTML>\n";

=head2 fetchreply()

Fetch and print all replies and responses to the report with ID C<$row_id>.

Calls L<reply_type()> to alter the UI to distinguish between user replies and
staff responses.

=cut
sub fetchreply {

    $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password, { RaiseError => 1 });
    $statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text, itd from reply where parent_id = ? ORDER BY date DESC";
    $sth_1 = $dbh_1->prepare($statement_1);
    $sth_1->execute($row_id);

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
    $sth_1->finish;
    $dbh_1->disconnect;
}

=head2 reply_type()

Determines if a reply is from ITD or not and sets the display color
(C<$font_color>) and the text (C<$reply_type>).

=cut
sub reply_type {

    if ($itd eq "yes") {
        $reply_type = "ITD Response";
        $font_color = "DarkRed";
    } else {
        $reply_type = "Reply";
        $font_color = "DarkBlue";
    }
}

=head2 recipient()

Sets the recipient email (C<$recipient>) based on the C<people.grp> (C<$grp>)
column in this report.

=cut
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

=head2 email_display()

Prints the HTML of the form to select which email addresses to send to.

=cut
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
    print "</select></td>\n";
    print "</tr>\n";

    print "</TABLE><br>\n";
}
