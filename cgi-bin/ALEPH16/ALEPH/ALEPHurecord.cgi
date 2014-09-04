#!/usr/local/bin/perl 

=head1 NAME

ALEPHurecord.cgi - Staff report update form

=cut

################################################
## updated 20080121 JB, added assigned statuses
################################################
## updated 20080125 JB, added deferred status
##  2009/12/04  Hans  change remove HS, add DW
##  2010/09/07  Hans  change aleph@itd.umd.edu to usmaialeph@umd.edu
##  2012/02/13  Hans  replace MK with MH, removed YQ
################################################

use DBI;
use CGI;

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$id = "";

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

    #Copy the name and value into the hash
    $input{$name} = $value;
}

$value = $ENV{'QUERY_STRING'};

$id = $input{'record'}; 
$REPORT = $input{'report'};
$limit = $input{'limit'};
$p = $input{'page_increment'};
$filter_value = $input{'filter_value'};
$sort_value = $input{'sort_value'};
$id_i = $input{'id_i'};
$id_t = $input{'id_t'};

if ($value) {
    # we got our report # from the query string
    $row_id = $value;
} else {
    # otherwise, it comes from the record parameter in the request body
    $row_id = $id;
}

$email1 = $input{'email1'};
$email2 = $input{'email2'};
$email3a = $input{'email3a'};
$email4a = $input{'email4a'};
$email3 = $input{'email3'};
$email4 = $input{'email4'};
$email5 = $input{'email5'};

if ($email3) { &Check_Email($email3a);}
if ($email4) { &Check_Email($email4a);}

&max_id;

if ($REPORT) {
    $id = $REPORT;
}

if ($id eq "") {
    if ($value) {
        $id = $value;
    }else {
        $id = "m";
    }
}

&print_form;

=head2 print_form()

Checks to see if C<$id> is a valid report number. If so, displays the form to
update the report with ID C<$id>. Calls L<fetchreply()> to print the list of
replies to this report.

If C<$id> is not a valid report number, display an error page.

=cut
sub print_form {

    print "Content-type: text/html\n\n";

    if ($id) {

        if ($id =~ /\D/){
            print "<HTML>\n<HEAD>\n<TITLE>RxWeb Update</TITLE>\n</HEAD>\n<BODY>\n";
            print "<CENTER><H3>You must enter a valid report #</H3>\n";
            print "<form>\n";
            print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
            print "</form>\n";
            print "</CENTER>\n";
        } elsif ($id eq ""){
            print "<HTML>\n<HEAD>\n<TITLE>RxWeb Update</TITLE>\n</HEAD>\n<BODY>\n";
            print "<CENTER><H3>You must enter a valid report #</H3>\n";
            print "<form>\n";
            print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
            print "</form>\n";
            print "</CENTER>\n";
        } elsif ($id > $max_id){
            print "<HTML>\n<HEAD>\n<TITLE>RxWeb Update</TITLE>\n</HEAD>\n<BODY>\n";
            print "<CENTER><H3>You must enter a valid report #</H3>\n";
            print "<form>\n";
            print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
            print "</form>\n";
            print "</CENTER>\n";
        }else {

            print "<HTML>\n<HEAD>\n<TITLE>RxWeb Update - Record $id</TITLE>\n <STYLE type=\"text\/css\">
            <!-- input, textarea, select { font-family: Times, serif; font-size: 12pt; color: #000000; background-color: #ff66ff\"; } -->
            </STYLE></HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
            print "<center>\n";
            print "<H1>RxWeb Update - Record $id</H1>\n";
            print "<FORM ACTION=\"ALEPHform2.cgi\" METHOD=post>\n";
            print "<INPUT TYPE=\"button\" VALUE=\"RxWeb\" onClick=\"parent.location='..\/ALEPHsum.cgi?id'\">\n";
            print "<INPUT TYPE=\"button\" VALUE=\"RxWeb Update\" onClick=\"parent.location='ALEPHform2.cgi?id'\"></p>\n";
            $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
            $statement =   "SELECT people.grp, people.campus, people.phone, people.name, report.date, report.status, report.summary, report.text, report.supress, report.cataloger, people.email, DATE_FORMAT(report.timestamp,'%m/%d/%y     %l:%i %p') FROM people, report WHERE people.id = report.id and people.id = $id";

            $sth = $dbh->prepare($statement)
                or die "Couldn't prepare the query: $sth->errstr";
            $rv = $sth->execute
                or die "Couldn't execute the query: $dbh->errstr";

            @row = $sth->fetchrow_array;
            $grp = $row[0];
            $campus = $row[1];
            $phone = $row[2];
            $name = $row[3];
            $date = $row[4];
            $status = $row[5];
            $summary = $row[6];
            $text = $row[7];
            $suppress = $row[8];
            $cataloger = $row[9];
            $email = $row[10];
            $report_timestamp = $row[11];

            &recipient;

            print "<INPUT TYPE=\"hidden\" NAME=\"record_id\" VALUE=\"$id\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"page_increment\" VALUE=\"$p\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"filter_value\" VALUE=\"$filter_value\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"sort_value\" VALUE=\"$sort_value\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"submit\" VALUE=\"yes\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"id_i\" VALUE=\"$id_i\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"id_t\" VALUE=\"$id_t\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"email1\" VALUE=\"$email1\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"email2\" VALUE=\"$email2\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"email3\" VALUE=\"$email3\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"email3a\" VALUE=\"$email3a\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"email4\" VALUE=\"$email4\">\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"email4a\" VALUE=\"$email4a\">\n";
            print "<TABLE BORDER=0 width=\"70%\">\n";
            print "<TR>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<b>Group:</b>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<select name=\"grp\">\n";
            print "<option>$grp\n";
            print "<option>Acquisitions\n";
            print "<option>Cataloging\n";
            print "<option>Circulation\n";
            print "<option>Item Maintenance\n";
            print "<option>Reserves\n";
            print "<option>Serials\n";
            print "<option>Technical\n";
            print "<option>Web OPAC\n";
            print "<option>Report request\n";
            print "<option>Change request\n";
            print "<option>other\n";
            print "</select>\n";
            print "</TD>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Submitted by:</b>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<INPUT TYPE=\"text\" NAME=\"cataloger\"  size=30 value=\"$cataloger\"></td>\n";
            print "</TD>\n";
            print "</TR>\n";
            print "<TR>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Campus:</B>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<select name=\"campus\" size=1>\n";
            print "<option>$campus";
            print "<option>BSU\n";
            print "<option>CES\n";
            print "<option>CSC\n";
            print "<option>FSU\n";
            print "<option>HS/HSL\n";
            print "<option>MS\n";
            print "<option>SMCM\n";
            print "<option>SU\n";
            print "<option>TU\n";
            print "<option>UB\n";
            print "<option>UBLL\n";
            print "<option>UMBC\n";
            print "<option>UMCP\n";
            print "<option>UMES\n";
            print "<option>UMLL\n";
            print "<option>UMUC\n";
            print "<option>ITD\n";
            print "</select>\n";
            print "</TD>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Name:</B>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<INPUT TYPE=\"text\" NAME=\"name\"  size=30 value=\"$name\">\n";
            print "</TD>\n";
            print "</TR>\n";
            print "<TR>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Status:</B>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<select name=\"status\" size=1>\n";
            print "<option>$status\n";
            print "<option>new\n";
            print "<option>closed\n";
            print "<option>pending\n";
            print "<option>deferred\n";
            print "<option>assigned\n";
            print "<option>assigned (HB)\n";
            print "<option>assigned (HH)\n";
            print "<option>assigned (DW)\n";
            print "<option>assigned (MH)\n";
            print "<option>assigned (LS)\n";
            print "<option>assigned (US)\n";
            print "<option>user input needed\n";
            print "<option>sent to func.group\n";
            print "<option>marked for enhancement\n";
            print "<option>change request\n";
            print "</select>\n";
            print "</TD>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Email:</b>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<INPUT TYPE=\"text\" NAME=\"email\"  size=50 value=\"$email\">\n";
            print "</TD>\n";
            print "</TR>\n";
            print "<TR>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Suppress:</B>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<select name=\"suppress\" size=1>\n";
            print "<option>$suppress\n";
            print "<option>yes\n";
            print "<option>no\n";
            print "</select>\n";
            print "</TD>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Date:</B>\n";
            print "</TD><TD>\n";
            print "<input type=text wrap=\"physical\" name=date size=10 value=\"$date\">\n";
            print "</TD>\n";
            print "</TR>\n";
            print "<TR>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Phone:</B>\n";
            print "</TD><TD WIDTH=\"10%\">\n";
            print "<input type=text wrap=\"physical\" name=phone size=12 value=\"$phone\">\n";
            print "<P>\n";
            print "</TD>\n";
            print "<TD ALIGN=RIGHT WIDTH=\"5%\">\n";
            print "<B>Summary:</B>\n";
            print "</TD><TD>\n";
            print "<input type=text wrap=\"physical\" name=summary size=50 value=\"$summary\">\n";
            print "</TD>\n";
            print "</TR>\n";
            print "</table>\n";
            print "<TABLE BORDER=0 width=\"70%\" cellpadding=\"8\">\n";
            print "<TR><TD WIDTH=\"50%\" colspan=4 bgcolor=white>\n";
            print "\n";
            print "<b>Report:</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font size=-1>$report_timestamp</font><br>\n";
            print "<textarea cols=\"140\" rows=\"10\" name=\"text\" wrap=\"virtual\">$text</textarea>\n";
            print "</table>\n";
            #############################
            &fetchreply;
            #############################
            print "<BR><BR>\n";
            print "<table border=\"0\" width=\"70%\">\n";
            print "<tr><td width=\"15\"><B><font size=\"-1\">Name:</B></font></td>\n";
            print "<td><INPUT TYPE=\"text\" NAME=\"rname\"  cols=50 maxlength=50 tabindex=\"1\"></td>\n";
            print "<td><font size=\"-1\">Check email configuration below and select submit:</font></td>\n";
            print "<tr><td width=\"15\"><B><font size=\"-1\">Response:</B></font></td>\n";
            print "<td colspan=\"3\"><textarea wrap=\"soft\" name=response cols=100 rows=5 tabindex=\"2\"></textarea></td></tr>\n";

            &email_display;

            print "<td><INPUT TYPE=submit VALUE=submit tabindex=\"5\"></td></tr>\n";
            print "<INPUT TYPE=\"hidden\" NAME=\"filter_value\" VALUE=\"$filter_value\">\n";
            print "</FORM>\n";
        }
    }
    $rc = $sth->finish;
    $rc = $dbh->disconnect;
    $rc_1 = $sth_1->finish;
    $rc_1 = $dbh_1->disconnect;
    print "</BODY>\n</HTML>\n";
}

=head2 max_id()

Get the highest report number currently in the database, and set C<$max_id> to
that value.

=cut
sub max_id {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT MAX(id) from report";

    $sth_4 = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth_4->errstr";
    $rv_4 = $sth_4->execute
        or die "Couldn't execute the query: $dbh->errstr";

    while(@row = $sth_4->fetchrow_array) {
        $max_id = $row[0];
    }
}

=head2 fetchreply()

Retrieve and print all of the replies to the report with ID C<$row_id> in
reverse chronological order. Called by L<print_form()>. Uses L<escapeXml()> to
do basic entity escaping of the C<reply.text> column returned from the
database.

=cut
sub fetchreply {

    $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text, itd, id from reply where parent_id = '$row_id' ORDER BY date DESC";
    $sth_1 = $dbh_1->prepare($statement_1)
        or die "Couldn't prepare the query: $sth_1->errstr";

    $rv_1 = $sth_1->execute
        or die "Couldn't execute the query: $dbh_1->errstr";

    while (@rrow = $sth_1->fetchrow_array) {

        ###################################
        $rrow[2] = &escapeXml($rrow[2]);
        ###################################
        ## Added by Ben 10/17/07
        ###################################

        $rrow[2] =~ s/\n/<BR>/g;

        $itd = $rrow[3];
        &reply_type;
        print "<table border=0 width=\"70%\" cellspacing=\"0\" cellpadding=\"8\">\n";
        print "<tr><td width=\"20%\"><font color=$font_color size=-1><b>$rrow[1]</td>\n";
        print "<td width=\"80%\"><font size=-1 color=$font_color><b>$reply_type from:&nbsp;&nbsp;$rrow[0]</td></tr>\n";
        print "<tr><td colspan=3 $bgcolor><i><font size=-1><font size=-1>$rrow[2]</td>\n";
        print "<td $bgcolor valign=\"bottom\"><font size=-1>\n";
        print "<a href=\"ALEPHureply.cgi?$rrow[4]\">edit</a>\n";
        print "</font></td></tr>\n";
        print "<tr><td colspan=3></td></tr>\n";
        print "</table>\n";
    }
    $rc_1 = $sth_1->finish;
    $rc_1 = $dbh_1->disconnect;
}

=head2 reply_type()

Sets the C<$reply_type> and C<$font_color> based on whether C<$itd> is "yes" or
not. If yes, the reply type is a "Response" and the color is red. Otherwise, the
reply type is "Reply" and the color is blue. The C<$reply_type> is also
formatted with extra padding to align correctly in the email.

=cut
sub reply_type {
    if ($itd eq "yes") {
        $reply_type = "ITD Response";
        $font_color = "DarkRed";
        $bgcolor = "bgcolor=#FFFF99";
    } else {
        $reply_type = "Reply";
        $font_color = "DarkBlue";
        $bgcolor = "bgcolor=#FFFF99";
    }
}

=head2 Check_Email()

Checks if its first argument is a valid email address. If it is not, it
increments the C<$email_check> counter, and pushes the bad string onto the
C<@store> array.

=cut
sub Check_Email {
    if ($_[0] =~ /(@.*@)|(,)|\s+|(\.\.)|(@\.)|(\.@)|(^\.)|(\.$)|(^\d+)|(\d+$)/ || ($_[0] !~ /^.+\@localhost$/ && $_[0] !~ /^.+\@\[?(\w|[-.])+\.[a-zA-Z]{2,3}|[0-9]{1,3}\]?$/)) {
        $email_check++;
        push @store, $_[0];
    } else {
    }
}

=head2 recipient()

Sets the email C<$recipient> based on the functional area (C<$grp>).

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
        $recipient = "usmaicoicatdbmaint\@umd.edu,usmaicoicircresill\@umd.edu,usmaicoiseracq\@umd.edu";
    }

    if ($grp eq "Reserves") {
        $recipient = "usmaicoicircresill\@umd.edu,usmaicoiuserinter\@umd.edu";
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

    if ($grp eq "ILL") {
        $recipient = "ilug\@umd.edu,usmaicoicircresill\@umd.edu";
    }

    if ($grp eq "AV18") {
        $recipient = "usmaialeph\@umd.edu";
    }
}

=head2 email_display()

Prints the HTML of the form to select which email addresses to send to. Called
by L<print_form()>.

=cut
sub email_display {

    print "<TABLE border=\"0\" width=\"50%\">\n";
    print "<tr><td colspan=\"2\" align=\"left\"><b>Email Options:</b></td></tr>\n";
    print "<tr><td colspan=\"2\"><hr></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email1\" VALUE=\"email1\" checked>Community:&nbsp;&nbsp;<cite><b>$recipient</b></cite></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email2\" VALUE=\"email2\" checked>Reported by:&nbsp;&nbsp;<b><cite>$email</b></cite></td></tr>\n";
    print "<tr><td><INPUT TYPE=\"checkbox\" NAME=\"email3\" VALUE=\"email3\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email3a\"  cols=50 maxlength=50 tabindex=\"3\"></td></tr>\n";
    print "<tr><td width=\"120\"><INPUT TYPE=\"checkbox\" NAME=\"email4\" VALUE=\"email4\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email4a\"  cols=50 maxlength=50 tabindex=\"4\"></td></tr>\n";

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
    print "<option>libitstaff\@umd.edu\n";
    print "</select></td>\n";
    print "</tr>\n";

    print "</TABLE><br>\n";
}

=head2 escapeXml()

Takes a single string argument, replaces "&", "<", and ">" with the appropriate
XML character entities, and returns the modified string.

=cut
sub escapeXml {
    my $text = shift;

    $text =~ s/&/&amp;/g;
    $text =~ s/</&lt;/g;
    $text =~ s/>/&gt;/g;

    return $text;
}
