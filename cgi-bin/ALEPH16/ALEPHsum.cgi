#!/usr/local/bin/perl 

=head1 NAME

ALEPHsum.cgi - The user display of RxWeb Summaries

=cut

## Jamie Bush, 2004
## RxWeb version 3.1
## Name changed to RxWeb from AlephRx on 6/20/06
## stats form

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
$value = "";
$count = 0;
$limit = 0;
#$filter = "";
$val = "";
$sort = "id";

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

# assign request parameters to variables
$CHANGE = $input{'CHANGE'};
$ACTIVE = $input{'ACTIVE'};
$CIRC = $input{'CIRC'};
$SRQ = $input{'SRQ'};
$ACQ = $input{'ACQ'};
$ITM = $input{'ITM'};
$RES = $input{'RES'};
$ILL = $input{'ILL'};
$CAT = $input{'CAT'};
$PAC = $input{'PAC'};
$CLOSED = $input{'CLOSED'};
$POST = $input{'POSTPONED'};
$NEW = $input{'NEW'};
$PEND = $input{'PENDING'};
$TECH = $input{'TECH'};
$RECORD = $input{'record'};
$NEXT = $input{'NEXT'};
$PREV = $input{'PREV'};
$LAST = $input{'LAST'};
$FIRST = $input{'FIRST'};
$REPORT = $input{'REPORT'};
$p = $input{'page_increment'};
$hidden_filter = $input{'hidden_filter'};
$hidden_value = $input{'hidden_value'};
$option_value = $input{'option_value'};
$NAME = $input{'NAME'};
$DATE = $input{'DATE'};
$ID = $input{'ID'};
$CAMPUS = $input{'CAMPUS'};
$STATUS = $input{'STATUS'};
$SUMMARY = $input{'SUMMARY'};
$FUNC = $input{'FUNC'};
$id_i = $input{'id_i'};
$val = $input{'val'};
$page_number = $input{'page_number'};

$value = $ENV{'QUERY_STRING'};
#$sort = $value; 

if ($NEXT) {
    $sort = $hidden_value;
}
if ($PREV) {
    $sort = $hidden_value;
}
if ($LAST) {
    $sort = $hidden_value;
}
if ($FIRST) {
    $sort = $hidden_value;
}

&filter;

if ($filter eq  "") {
    $filter = $hidden_filter;
}

&sort_submit;
&val;
&sort_increment;
&sort_rules;

&record;
&get_row_count;
&calc_num_pages;

#&page_number;
&filter_display;
&sort_display;
&print_page_start;
&next_paging;
&prev_paging;
&first_paging;
&last_paging;
&page_rules;
&first_last;
&get_sum_record;
&print_fetch;

&print_page_end;

=head2 print_fetch()

Print the table of records. Reads data from C<$sth>, which has been executed by
L<get_sum_record()>.

=cut
sub print_fetch {
    print "<TABLE BORDER=0 CELLPADDING=2>\n";
    print "<TR>&nbsp;<TD></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"  ID  \" NAME=\"ID\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"                         Summary                         \" NAME=\"SUMMARY\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"Functional Area\" NAME=\"FUNC\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"         Name         \" NAME=\"NAME\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"Campus\" NAME=\"CAMPUS\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"     Status     \" NAME=\"STATUS\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"  Date  \" NAME=\"DATE\"></TD>\n";
    print "<TD><FONT SIZE=-3>Replies</TD></TR>\n";

    while (@row = $sth->fetchrow_array) {
        $response_count = "";
        $row_id = $row[0];
        &count_response;
        print "<TR><TD><FONT SIZE=+1 COLOR=\"#FF0000\">$response_count</FONT>\n</TD>";
        print "<TD BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1>#&nbsp;<a href=\"ALEPHsum_full.cgi?$row[0]\">$row[0]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\"><FONT SIZE=-1>&nbsp;$row[3]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1>&nbsp;$row[1]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\"><FONT SIZE=-1>&nbsp;$row[6]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1>&nbsp;$row[2]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\"><FONT SIZE=-1>&nbsp;$row[4]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1>&nbsp;$row[5]</TD>\n";
        $reply_count = "";
        $count = 0;
        &count_reply;
        print "<TD BGCOLOR=\"#FFFFF0\" ALIGN=\"CENTER\"><FONT SIZE=-1 COLOR=\"#000000\">$reply_count</TD></TR>\n";
    }
}

=head2 fetchreply()

Fetches all replies for printing.

B<XXX: Not called in this script.>

=cut
sub fetchreply {

    $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from reply where parent_id = '$row_id' ORDER BY date DESC";
    $sth_1 = $dbh_1->prepare($statement_1)
        or die "Couldn't prepare the query: $sth_1->errstr";

    $rv_1 = $sth_1->execute
        or die "Couldn't execute the query: $dbh_1->errstr";

    while (@rrow = $sth_1->fetchrow_array) {
        print "<TR>\n";
        print "<TD COLSPAN=2 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><i><FONT SIZE=-1 COLOR=\"3333CC\">&nbsp;Reply from:&nbsp;\n";
        print "$rrow[0]</TD>\n";
        print "<TD COLSPAN=4 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"3333CC\"><i>Date:&nbsp;$rrow[1]&nbsp;&nbsp;&nbsp;</TD>\n";
        print "<TD COLSPAN=1 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"3333CC\"><i>&nbsp;$rrow[2]</TD>\n";
        print "</TR>\n";
    }
    $rc_1 = $sth_1->finish;
    $rc_1 = $dbh_1->disconnect;
}

=head2 fetchresponse()

Fetches response for printing.

B<XXX: Not called in this script.>

=cut
sub fetchresponse {
    $dbh_2 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_2 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from reply where parent_id = '$row_id' and itd = 'yes'";

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

=head2 count_reply()

Get the number of replies to the report with ID given by C<$row_id>. Replies are
rows in the C<reply> table that have C<reply.itd> set to "no".

Counts using C<$count> and sets C<$reply_count> to the final value.

=cut
sub count_reply {
    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_7 =   "SELECT name from reply where parent_id = '$row_id' and itd = 'no'";
    $sth_7 = $dbh->prepare($statement_7)
        or die "Couldn't prepare the query: $sth_7->errstr";

    $rv_7 = $sth_7->execute
        or die "Couldn't execute the query: $dbh->errstr";


    while (@row = $sth_7->fetchrow_array) {
        $count++;
        $reply_count = $count;
    }

    $rc_7 = $sth_7->finish;
    $rc_7 = $dbh->disconnect;
}

=head2 count_response()

Creates a flag to display when there is an ITD/DSS response to a report. If
there is at least one reply to the report with ID C<$row_id> with C<reply.itd>
set to "yes", sets C<$response_count> to the flag "*".

Note that contrary to the name, this does not set or return a number of
responses.

=cut
sub count_response {
    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_8 =   "SELECT text from reply where parent_id = '$row_id' and itd = 'yes'";
    $sth_8 = $dbh->prepare($statement_8)
        or die "Couldn't prepare the query: $sth_8->errstr";

    $rv_8 = $sth_8->execute
        or die "Couldn't execute the query: $dbh->errstr";


    while (@rrow = $sth_8->fetchrow_array) {
        if ($rrow[0] eq ""){
        }else{
            $response_count = "*";
        }
    }

    $rc_8 = $sth_8->finish;
    $rc_8 = $dbh->disconnect;
}


=head2 response_get()

B<XXX: Not called in this script.>

=cut
sub response_get {
    if ($row[7] eq "") {
    } else {
        $response = "*";
    }
}

=head2 get_reply()

B<XXX: Not called in this script.>

=cut
sub get_reply {
    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_9 =   "SELECT name from reply where parent_id = '$row_id'";
    $sth_9 = $dbh->prepare($statement_9)
        or die "Couldn't prepare the query: $sth_9->errstr";

    $rv_9 = $sth_9->execute
        or die "Couldn't execute the query: $dbh->errstr";

    while (@srow = $sth_1->fetchrow_array) {
        $count++;
        $reply_count = '* ' x $count;
    }
    $rc_9 = $sth_9->finish;
    $rc_9 = $dbh->disconnect;
}

=head2 get_row_count()

Queries the database to get the total number of records, used to calculate the
total number of pages. The total is stored in C<$row_count>.

=cut
sub get_row_count {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_10 =   "SELECT COUNT(*) from report, people where report.supress = 'no' and report.id = people.id $filter";
    $sth_10 = $dbh->prepare($statement_10)
        or die "Couldn't prepare the query: $sth_10->errstr";

    $rv_10 = $sth_10->execute
        or die "Couldn't execute the query: $dbh->errstr";

    while (@crow = $sth_10->fetchrow_array) {
        $row_count = $crow[0];
    }
    $rc_10 = $sth_10->finish;
    $rc_10 = $dbh->disconnect;
}

=head2 calc_num_pages()

Calculates the total number pages that will be used for all the database.
Divides the C<$row_count> by 30 records per page. Rounds to the next largest
integer and stores that value in C<$num_pages>.

Unlike the C<calc_num_pages()> function in ALEPHform2.cgi, this uses a magic
number of 30 instead of the C<$numrec> variable.

=cut
sub calc_num_pages {

    $num_pages_1 = $row_count / 30;
    $num_pages_2 = sprintf("%d\n", $num_pages_1);
    if ($num_pages_1 > $num_pages_2){
        $num_pages = $num_pages_2 + 1;
    }else{
        $num_pages = $num_pages_2;
    } 
}

=head2 next_paging()

If this request is the result of the "Next Page" button being clicked (and the
C<NEXT> POST parameter being submitted), increments the page variable C<$p>, and
prints the hidden field to pass on to the next page.

=cut
sub next_paging {
    if ($NEXT) {
        $p++;
        print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
    }
}

=head2 last_paging()

If this request is the result of the "Last Page" button being clicked (and the
C<LAST> POST parameter being submitted),Sets the page variable C<$p> to one less
than C<$num_pages>, and prints the hidden field to pass on to the next page.

=cut
sub last_paging {
    if ($LAST) {
        $p = $num_pages - 1;
        print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
    }
}

=head2 first_paging()

If this request is the result of the "First Page" button being clicked (and the
C<FIRST> POST parameter being submitted), sets the page variable C<$p> to 0, and
prints the hidden field to pass on to the next page.

=cut
sub first_paging {
    if ($FIRST) {
        $p = 0;
        print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
    }
}

=head2 prev_paging()

If this request is the result of the "Previous Page" button being clicked (and
the C<PREV> POST parameter being submitted), decrements the page variable C<$p>,
prints the hidden field to pass on to the next page

=cut
sub prev_paging {
    if ($PREV) {
        $p--;
        print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
    }
}

=head2 page_rules()

Decides which of the next and previous buttons will display based on the which
page we are on, and prints the appropriate buttons. Also updates the C<$limit>
variable used in the SQL query in L<get_sum_record()>.

Unlike the C<page_rules()> function in ALEPHform2.cgi, this uses a magic number
of 30 instead of the C<$numrec> variable.

=cut
sub page_rules {
    print "<table WIDTH=\"70%\" border=0><tr>\n";

    if ($p < 1){
        # first page ($p == 0)
        # do nothing
    } else {
        # after the first page
        # print controls to go back
        print "<TD ALIGN=\"LEFT\"><INPUT TYPE=\"submit\" VALUE=\"<< First Page\" NAME=\"FIRST\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";
        print "<INPUT TYPE=\"submit\"  VALUE=\"< Previous Page\" NAME=\"PREV\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";
    }

    if ($p > $num_pages - 2) {
        # past the next to last page
        # do nothing
    }else{
        if ($value =~ /\d/) {
            end;
        } elsif ($LAST) {
            # "Last Page" was clicked
            # do nothing
        } else {
            # before the last page
            # print controls to go forward
            print "<TD ALIGN=\"RIGHT\"><INPUT TYPE=\"submit\" VALUE=\"Next Page >\" NAME=\"NEXT\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";
            print "<INPUT TYPE=\"submit\" VALUE=\"Last Page >>\" NAME=\"LAST\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";
        }
    }
    # update the limit to be used in the SQL query in get_sum_record()
    $limit = $p * 30; 

    print "<BR>\n";
    print "</td></tr></table>\n";
}

=head2 first_last()

Set the C<$limit> variable used to construct the SQL query based on which page
we are on.

=cut
sub first_last {
    if ($LAST) {
        $limit = ($num_pages - 1) * 30;
    }
    if ($FIRST) {
        $limit = 0;
    }
}

=head2 filter()

Sets the C<$filter> variable used to construct the SQL where clause in
L<get_sum_record()>, based on which filter submit button was used to POST this
request.

=cut
sub filter {

    if ($CIRC) {
        $filter = "and people.grp = 'Circulation'";
    }

    if ($PAC) {
        $filter = "and people.grp = 'Web OPAC'";
    }

    if ($SRQ) {
        $filter = "and people.grp = 'Serials'";
    }

    if ($ACQ) {
        $filter = "and people.grp = 'Acquisitions'";
    }

    if ($CAT) {
        $filter = "and people.grp = 'Cataloging'";
    }

    if ($TECH) {
        $filter = "and people.grp = 'Technical'";
    }

    if ($ITM) {
        $filter = "and people.grp = 'Item Maintenance'";
    }

    if ($RES) {
        $filter = "and people.grp = 'Reserves'";
    }

    if ($ILL) {
        $filter = "and people.grp = 'ILL'";
    }

    if ($CLOSED) {
        $filter = "and report.status = 'closed'";
    }

    if ($PEND) {
        $filter = "and report.status = 'pending'";
    }

    if ($POST) {
        $filter = "and report.status = 'postponed'";
    }

    if ($NEW) {
        $filter = "and report.status = 'new'";
    }

    if ($ACTIVE) {
        $filter = "and report.status in ('change request','new','pending','assigned','user input needed','sent to functional group')";
    }

    if ($REPORT) {
        $filter = "and people.grp = 'Report request'";
    }

    if ($CHANGE) {
        $filter = "and people.grp = 'Change request'";
    }
}

=head2 print_page_start()

Prints the HTTP header and HTML page start, filter buttons, and hidden form
fields.

=cut
sub print_page_start {

    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD>\n<TITLE>RxWeb</TITLE>\n</HEAD>\n<BODY bgcolor=\"#98AFC7\">\n";
    print "<FORM ACTION=\"ALEPHsum.cgi?id\" METHOD=\"post\">\n";
    print "<a NAME=\"top\"></a>\n";
    print "<center>\n";
    print "<FONT SIZE=\"-1\"><INPUT TYPE=\"button\" VALUE=\"RxWeb Form\" onClick=\"parent.location ='\/cgi-bin\/ALEPHform.cgi'\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</FONT>\n";
    print "<FONT SIZE=\"+3\"><STRONG>RxWeb</STRONG></FONT>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<FONT SIZE=\"-1\"><INPUT TYPE=\"button\" VALUE=\"RxWeb Statistics\" onClick=\"parent.location ='ALEPHstats.cgi'\"></FONT><br><br>\n";
    print "<FONT SIZE=\"-1\">Select one of the following to filter reports.</font>\n";
    print "<table border=\"0\" width=\"60%\" bgcolor=\"#98AFC7\">\n";
    print "<tr>\n";
    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Acquisitions\" NAME=\"ACQ\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Circulation\" NAME=\"CIRC\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Cataloging\" NAME=\"CAT\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Item Maintenance\" NAME=\"ITM\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Reserves\" NAME=\"RES\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"ILL\" NAME=\"ILL\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Serials\" NAME=\"SRQ\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";



    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Web OPAC\" NAME=\"PAC\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";



    print "<tr>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Technical\" NAME=\"TECH\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"New\" NAME=\"NEW\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Pending\" NAME=\"PENDING\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Active\" NAME=\"ACTIVE\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Change Request\" NAME=\"CHANGE\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Closed\" NAME=\"CLOSED\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Report Requests\" NAME=\"REPORT\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"All Summaries\" NAME=\"ALL\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<tr><td colspan=\"2\"><font size=\"-1\">&nbsp;&nbsp;FILTER = <b>$filter_display</b></font></td><td cellpadding=\"2\" colspan=\"1\"><font size=\"-1\">&nbsp;&nbsp;SORT = <b>$sort_display</b></font></td><td cellpadding=\"2\" colspan=\"2\"><font size=\"-1\">&nbsp;&nbsp;ORDER = <b>$option_value</b></font></td>\n";

    print "<td colspan=\"2\"><font size=\"-1\">&nbsp;&nbsp<a href=\"http://usmai.umd.edu/groups/information-technology-division-itd/workplan-folder/submit-aleph-request-rx\">Learn more about RxWeb</a></font></td>\n";
    print "<td><font size=\"-1\"><a href=\"http://usmai.umd.edu\">USMAI Alerts<a/></td>\n";
    print "</table>\n";
    print "</FORM>\n";
    print "<FORM ACTION=\"ALEPHsum_full.cgi\" METHOD=\"post\">\n";
    print "<FONT SIZE=+1 COLOR=\"#FF0000\">&nbsp;&nbsp;*</FONT><FONT SIZE=-1>&nbsp;&nbsp;Indicates an ITD response has been made.&nbsp;</FONT>\n";
#print "<FONT SIZE=+1 COLOR=\"#0000FF\">&nbsp;&nbsp;*</FONT><FONT SIZE=-1>&nbsp;&nbsp;Indicates a User reply.</FONT>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<B>Go to report # :</B>\n";
    print "<INPUT TYPE=\"text\" NAME=\"record\" SIZE=3>\n";
    print "<INPUT TYPE=\"submit\" VALUE=\"GO\">\n";
    print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<FONT SIZE=\"-1\"><INPUT TYPE=\"button\" VALUE=\"Basic Search\" onClick=\"parent.location ='ALEPHsearch.cgi'\"></FONT><br><br>\n";
    print "</FORM>\n";

    print "<FORM ACTION=\"ALEPHsum.cgi?id\" METHOD=\"post\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"hidden_filter\" VALUE=\"$filter\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"hidden_value\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"option_value\" VALUE=\"$option_value\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"id_i\" VALUE=\"$id_i\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_number\" VALUE=\"$page_number\">\n";
}

=head2 print_page_end()

Prints the end of the table, disconnects the C<$dbh>, prints hidden fields, and
the end of the HTML page.

=cut
sub print_page_end {

    print "</TABLE>\n";
    $rc = $sth->finish;
    $rc = $dbh->disconnect;
    print "<BR>\n";
    &page_rules;
    print "<INPUT TYPE=\"hidden\" name=\"val\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_number\" VALUE=\"$page_number\">\n";
    print "</FORM>\n";
    print "<CENTER><a href=\"#top\"><FONT SIZE=-1>TOP</a>\n";
    print "<BR><BR>\n";
    print "</BODY>\n</HTML>\n";

} 

=head2 record()

If C<$RECORD> is set (i.e., there was a request parameter C<record>) but is the
empty string, set it to the string "id". Then, if C<$RECORD> contains anything
that is not a digit, set C<$value> to "id". Otherwise, set C<$value> to
C<$RECORD>.

=cut
sub record {
    if ($RECORD) {
        if ($RECORD eq ""){
            $RECORD = "id";
        }
    }

    if ($RECORD) {
        if ($RECORD =~ /\D/) {
            $value = "id";
        } else {
            $value = $RECORD;
        }
    }
}

=head2 get_sum_record()

Get summary records from the database. This is the main query used to display
data on this page.

Uses the variables C<$filter>, C<$sort>, C<$option>, and C<$limit>
to construct the query. Executes the query using the statement handle C<$sth>.

Only queries records where C<report.supress = 'no'>.

=cut
sub get_sum_record {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT people.id, people.grp, people.campus, report.summary, report.status, DATE_FORMAT(report.date,'%m/%d/%y'), people.name FROM people, report WHERE report.supress = 'no' and people.id = report.id $filter order by $sort $option LIMIT $limit, 30";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";
}

=head2 sort_submit()

Set C<$sort> based on which sort button was clicked for this submission.
C<$sort> is used in the C<ORDER BY> clause in the SQL query in
L<get_sum_record()>. Also increments C<$id_i>.

=cut
sub sort_submit {
    if ($ID) {
        $sort = "report.id";
        $id_i++;
    }

    if ($SUMMARY) {
        $sort = "report.summary";
        $id_i++;
    }

    if ($NAME) {
        $sort = "people.name";
        $id_i++;
    }

    if ($DATE) {
        $sort = "report.date";
        $id_i++;
    }

    if ($CAMPUS) {
        $sort = "people.campus";
        $id_i++;
    }

    if ($STATUS) {
        $sort = "report.status";
        $id_i++;
    }

    if ($FUNC) {
        $sort = "people.grp";
        $id_i++;
    }
}

=head2 sort_rules()

Set C<$otion_value> based on the current search order used in the SQL (as stored
in the C<$option> variable). Maps "DESC" to "Descending" and "" to "Ascending".

=cut
sub sort_rules {

    if ($option eq "DESC") {
        $option_value = "Descending";
    }

    if ($option eq "") {
        $option_value = "Ascending";
    }
}

=head2 sort_increment()

Sets the value of C<$option> to "DESC" if C<$id_i> is 1 or "" otherwise.
C<$option> is used to build the SQL query.

=cut
sub sort_increment {
    if ($id_i > 1) {
        $id_i = 0;
    }

    if ($id_i eq "1") {
        $option = "";
    }

    if ($id_i eq "0") {
        $option = "DESC";
    }
}

=head2 val()

Sets the C<$id_i> variable to 0 each time a new sort key is selected.

=cut
sub val  {
    if ($val ne $sort){
        $id_i = 0;
    }
}

=head2 filter_display()

Set the C<$filter_display> variable used on the UI based on the value of the
C<$filter>.

=cut
sub filter_display  {
    if ($filter eq "and people.grp = 'Circulation'") {
        $filter_display = "Circulation";
    }

    if ($filter eq "and people.grp = 'Acquisitions'") {
        $filter_display = "Acquisitions";
    }

    if ($filter eq "and people.grp = 'Technical'") {
        $filter_display = "Technical";
    }

    if ($filter eq "and people.grp = 'Web OPAC'") {
        $filter_display = "Web OPAC";
    }

    if ($filter eq "and people.grp = 'Reserves'") {
        $filter_display = "Reserves";
    }

    if ($filter eq "and people.grp = 'ILL'") {
        $filter_display = "ILL";
    }

    if ($filter eq "and people.grp = 'Serials'") {
        $filter_display = "Serials";
    }

    if ($filter eq "and people.grp = 'Item Maintenance'") {
        $filter_display = "Item Maintenance";
    }

    if ($filter eq "and people.grp = 'Cataloging'") {
        $filter_display = "Cataloging";
    }

    if ($filter eq "and people.grp = 'Item Maintenance'") {
        $filter_display = "Item Maintenance";
    }

    if ($filter eq "") {
        $filter_display = "All Summaries";
    }

    if ($filter eq "and report.status = 'new'") {
        $filter_display = "New";
    }

    if ($filter eq "and report.status = 'pending'") {
        $filter_display = "Pending";
    }

    if ($filter eq "and report.status in ('change request','new','pending','assigned','user input needed','sent to functional group')") {
        $filter_display = "Active";
    }
    if ($filter eq "and report.status = 'postponed'") {
        $filter_display = "Postponded";
    }

    if ($filter eq "and report.status = 'closed'") {
        $filter_display = "Closed";
    }

    if ($filter eq "and people.grp = 'Report request'") {
        $filter_display = "Report Request";
    }

    if ($filter eq "and people.grp = 'Change request'") {
        $filter_display = "Change Request";
    }
}

=head2 sort_display()

Set the C<$sort_display> variable used in the UI based on the value of
C<$sort>.

=cut
sub sort_display  {

    if ($sort eq "report.id") {
        $sort_display = "ID";
    }
    if ($sort eq "report.summary") {
        $sort_display = "Summary";
    }

    if ($sort eq "report.date") {
        $sort_display = "Date";
    }

    if ($sort eq "people.name") {
        $sort_display = "Name";
    }

    if ($sort eq "people.campus") {
        $sort_display = "Campus";
    }
    if ($sort eq "people.grp") {
        $sort_display = "Functional Area";
    }

    if ($sort eq "report.status") {
        $sort_display = "Status";
    }
    if ($sort eq "id") {
        $sort_display = "ID";
    }
}
