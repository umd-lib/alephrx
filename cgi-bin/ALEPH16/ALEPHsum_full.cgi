#!/usr/bin/perl 

=head1 NAME

ALEPHsum_full.cgi - Report details page

=head1 DESCRIPTION

This script displays the full record for a given report: all the report data as
well as all of the replies. It also contains a link to the form to reply to the
report.

=cut

## Jamie Bush, 2004
## RxWeb (AlephRx) version 3.1
## name changed 6/20/06
## stats form

use DBI;
use CGI;

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
$RECORD = $input{'record'};
$p = $input{'page_increment'};

$value = $ENV{'QUERY_STRING'};

&record;
&validate;
&print_page_start;

if ($error_message eq "")  {
    # there was no problem with the report ID
    &get_full_record;
} else {
    print "<B>$error_message</B>\n";
}

&print_page_end;

=head2 fetchreply()

Fetch and print all replies and responses to the report with ID C<$row_id>.

Calls L<reply_type()> to alter the UI to distinguish between user replies and
staff responses.

Calls L<escapeXML()> to entity-escape the C<reply.text> column.

=cut
sub fetchreply {

    $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password, { RaiseError => 1 });
    $statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text, itd from reply where parent_id = ? ORDER BY date DESC";
    $sth_1 = $dbh_1->prepare($statement_1);
    $sth_1->execute($row_id);

    while (@rrow = $sth_1->fetchrow_array) {

        $rrow[2] = &escapeXml($rrow[2]);
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

=head2 print_page_start()

Prints start of page

=cut
sub print_page_start {
    my $number = $error_message ? "Not Found" : "#$value";
    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD>\n<TITLE>Report $number - AlephRx</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
    print "<FORM ACTION=\"ALEPHsum.cgi?id\" METHOD=\"post\">\n";
    print "<a NAME=\"top\"></a>\n";
    print "<center>\n";
    print "<H1>AlephRx Report $number</H1>\n";
    print "<INPUT TYPE=\"button\" VALUE=\"Submit a Report\" onClick=\"parent.location ='../ALEPHform.cgi'\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"View Reports\" onClick=\"parent.location='ALEPHsum.cgi?id'\">\n";
    print "</FORM>\n";
    print "<FORM ACTION=\"ALEPHsum_full.cgi\" METHOD=\"post\">\n";
    print "<B>Go to report # :</B>\n";
    print "<INPUT TYPE=\"text\" NAME=\"record\" SIZE=3>\n";
    print "<INPUT TYPE=\"submit\" VALUE=\"GO\">\n";
    print "</FORM>\n";
    print "<TABLE BORDER=0 CELLPADDING=2>\n";
}


=head2 print_page_end()

Prints end of page

=cut
sub print_page_end {
    print "</TABLE>\n";
    $sth->finish;
    $dbh->disconnect;
    print "</BODY>\n</HTML>\n";
} 

=head2 record()

This sets the value of C<$value> to "id" if it is blank. C<$value> is used in
the url to display a record.

=cut
sub record {

    if ($RECORD){
        if ($RECORD eq ""){
            $RECORD = "id";
        }
    }

    if ($RECORD) {
        if ($RECORD =~ /\D/) {
            $value = "id";
        }else{
            $value = $RECORD;

        }
    }
}

=head2 get_full_record()

Queries the database for the full record for display. The report ID is taken
from C<$value>. Prints the report fields, then calls L<fetchreply()> to fetch
and print the replies and responses to this report.

Calls L<escapeXml()> to do entity-escaping of the C<report.text> column.

=cut
sub get_full_record {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password, { RaiseError => 1 });

    $statement =   "SELECT people.id, report.summary, people.name, people.phone, DATE_FORMAT(report.date,'%m/%d/%y'), people.grp, people.campus, report.status, report.text FROM people, report WHERE people.id = ? and people.id = report.id";
    $sth = $dbh->prepare($statement);
    $sth->execute($value);

    while (@row = $sth->fetchrow_array) {
        print " <TR><TD COLSPAN=7 ALIGN=RIGHT VALIGN=TOP><a href=\"ALEPHreply.cgi?$row[0]\">Reply to This Report</a></FONT></TD></TR>\n";
        print "<TR><TD BGCOLOR=\"#FFFF00\" COLSPAN=7><B><i>Report #</i>&nbsp;$row[0]&nbsp;&nbsp;&nbsp;&nbsp;$row[1]</B></TD></FONT></TR>\n";

        $row[8] = &escapeXml($row[8]);
        $row[8] =~ s/\n/<BR>/g;

        print "<TR>\n
        <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Name</I></TH>\n
        <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Phone</I></TH>\n
        <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Date</I></TH>\n
        <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Func. Area</I></TH>\n
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
        print "</TR>\n";
        # fetch the replies
        &fetchreply();
        print "</TR>\n";
        print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
        print "<TR><TD>$reply_count</TD></TR>\n";
    }
}

=head2 validate()

Validates whether a record number has been submitted in the "go to report" box
and sets the C<$error_message>.

=cut
sub validate {

    if ($RECORD =~ /\d/) {
        $error_message = "";
    }else{
        $error_message = "You must enter a record number!";
    }
    if ($value =~ /\d/) {
        $error_message = "";
    }else{
        $error_message = "You must enter a record number!";
    }

}

=head2 reply_type()

Determines if a reply is from DSS or not and sets the display color
(C<$font_color>) and the text (C<$reply_type>).

=cut
sub reply_type {

    if ($itd eq "yes") {
        $reply_type = "DSS Response";
        $font_color = "DarkRed";
    } else {
        $reply_type = "Reply";
        $font_color = "DarkBlue";
    } 
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
