#!/usr/local/bin/perl

=head1 NAME

ALEPHureply.cgi - Staff form for editing a reply

=cut

use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use IO::Handle;
use lib "/lims/lib/perl";

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$reply_id = "";
$submitted = "";
$query = new CGI;
$error = "  ";

$reply_id = $ENV{'QUERY_STRING'};

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
    $value =~ s/\'/\\\'/g;

    #Copy the name and value into the hash
    $input{$name} = $value;
}

$text = $query->param('text');
$id = $query->param('id');

if ($query->param('submitted')) {
    # if the form has been submitted
    # get the reply ID from the request parameter "id"
    $reply_id = $id;
    # update the reply in the database
    &insert;
    # redisplay the form
    &print_form;
} else {
    # get the reply ID form the query string
    $reply_id = $ENV{'QUERY_STRING'};
    # display the form
    &print_form;
}

=head2 print_form()

Print the HTTP header and the HTML for the page. Queries the database for the
reply with the ID C<$reply_id>.

=cut
sub print_form {

    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD>\n<TITLE>RxWeb Reply Edit</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
    print "<FORM ACTION=\"ALEPHureply.cgi\" METHOD=\"post\">\n";
    print "<center>\n";
    print "<H1>RxWeb Reply Edit Test</H1>\n";
    print "<INPUT TYPE=\"button\" VALUE=\"RxWeb Update\" onClick=\"parent.location='ALEPHform2.cgi'\">\n";

    print "<br><br>\n";
    print "<TABLE BORDER=0 width=\"60%\" CELLPADDING=2>\n";

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT text, name, DATE_FORMAT(date,'%b %e, %Y      %r'), id, parent_id, DATE_FORMAT(timestamp,'%b %e, %Y    %r') from reply where id = $reply_id";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";

    while (@row = $sth->fetchrow_array) {
        print "<TR>\n";
        print "<TD WIDTH=\"20%\" BGCOLOR=\"#FFFF99\" VALIGN=TOP>$row[1]</TD>\n";
        print "<TD WIDTH=\"30%\" BGCOLOR=\"#FFFF99\" VALIGN=TOP><FONT SIZE=-1>Created:</font>&nbsp;&nbsp;$row[2]</TD>\n";
        print "<TD WIDTH=\"30%\" BGCOLOR=\"#FFFF99\" VALIGN=TOP><FONT SIZE=-1>Updated:&nbsp;&nbsp;&nbsp;$row[5]</FONT></TD>\n";
        print "<TR><TD COLSPAN=3 ><textarea wrap=\"soft\" name=text cols=100 rows=8>$row[0]</textarea></TD>\n";
        print "</TR>\n";
        $reply_id = $row[3];
        $record = $row[4];
        $updated = $row[5];
    }

    $rc = $sth->finish;
    $rc = $dbh->disconnect;
    print "</TABLE>\n";
    print "<br><br>\n";
    print "<INPUT TYPE=\"hidden\" name=\"id\" VALUE=\"$reply_id\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
    print "<td><INPUT TYPE=submit VALUE=submit></td></tr>\n";
    print "</FORM>\n";
    print "<a href=\"ALEPHurecord.cgi?$record\">RxWeb Update Record $record<\/a>\n";
    print "<h3>$error</h3>\n";
    print "<P><h2>This function is still in development</h2>\n";
    print "You can now update the text of the reply<br>\n";
    print "by making changes in the text above and selecting submit.<br>\n";
    print "There is no email functionality associated with this update<br>\n";
    print "and there is no error checking in place yet, so proceed at your own risk!<br></p>\n";
    print "</BODY>\n</HTML>\n";

}

=head2 insert()

Update the reply with ID C<$reply_id> in the database. Sets the C<reply.text>
column to the value of C<$text> and the C<reply.timestamp> column to C<NOW()>.

Sets the C<$error> flag to "Reply has been updated.". This is used by the
L<print_form()> function to indicate to the user that the database has been
updated.

=cut
sub insert {
    # Escape the single quotes & back slashes
    $text =~ s/\\/\\\\/g;
    $text =~ s/\'/\\\'/g;

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "UPDATE reply SET text = '$text', timestamp = NOW() WHERE id = $reply_id";
    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";

    $rc = $sth->finish;
    $rc = $dbh->disconnect;
    $error = "Reply has been updated.";
}
