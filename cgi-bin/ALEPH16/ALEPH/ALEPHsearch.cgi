#!/usr/bin/perl

=head1 NAME

ALEPHsearch.cgi - Staff basic search page

=cut

use CGI;
use DBI;
use CGI::Carp qw(fatalsToBrowser);

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$id = "";
$query = new CGI;

$field = $query->param('field');
$term = $query->param('term');
$submitted = $query->param('submitted');

# start the page and print the search form
&print_form;

if ($submitted eq "yes") {
    if ($term eq "") {
        # the search term must be non-empty
        print "<B>You must enter a search term!</B><BR><BR>\n";
    } else {
        &do_search;
        &display_results;
    }
}

&print_page_end;

=head2 print_form()

Print the HTTP header, the beginning of the HTML page, and the search form.

=cut
sub print_form {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>Search - AlephRx</title>\n";
    print "</head>\n<body BGCOLOR=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>AlephRx Search</h1>\n";
    print "<FORM method=\"POST\" action=\"ALEPHsearch.cgi\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"View Reports for Staff\" onClick=\"parent.location='ALEPHform2.cgi?id'\"><BR><BR>\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
    print "Select the field to search:&nbsp;\n";
    print "<select name=\"field\" size=1>\n";
    print "<option>summary\n";
    print "<option>text\n";
    print "<option>name\n";
    print "<option>reply\n";
    print "</select>\n";
    print "<BR><BR>\n";
    print "Enter a single search term and submit<BR><BR>\n";
    print "<input type=text name=term size=20>\n";
    print "<input type=submit>\n";
    print "<BR>\n";
    print "<input TYPE=\"hidden\" NAME=\"hidden_filter\" VALUE=\"$hidden_filter\">\n"; 
    print "</FORM>\n";
}

=head2 print_page_end()

Print the end of the HTML page.

=cut
sub print_page_end {
    print "</body></html>\n";
}

=head2 do_search()

Construct and execute an SQL query to search the database. If C<$field> is
"reply", then it searches the columns C<reply.text> and C<reply.name>.
Otherwise, it uses C<$field> as the column name to search. The search term
(C<$term>) can appear anywhere in the column (i.e., the SQL uses a C<LIKE
'%$term%'> predicate).

The executed statement handle is in C<$sth>, and the number of rows found is
stored in C<$nr>.

=cut
sub do_search {
    # escape the single quotes
    $term =~ s/\'/\\\'/g;
    $field =~ s/\'/\\\'/g;

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password, { RaiseError => 1 });

    if ($field eq "reply") {
        $statement =   "SELECT DISTINCT people.id, report.summary, DATE_FORMAT(report.date,'%m/%d/%y'), people.name, people.grp, report.status from people, report, reply where (reply.text LIKE '%$term%' or reply.name LIKE '%$term%') and reply.parent_id = report.id and report.id = people.id order by people.id";
    } else {
        $statement =   "SELECT people.id, report.summary, DATE_FORMAT(date,'%m/%d/%y'), people.name, people.grp, report.status from people, report where $field LIKE '%$term%' and report.id = people.id order by people.id";
    }

    $sth = $dbh->prepare($statement);
    $sth->execute;

    $nr = $sth->rows;
}

=head2 display_results()

Print the number of results. Then, if there are 1 or more results, print the
table of actual results. Within the table, the summary text for each result
links to the staff record update form for that report (ALEPHurecord.cgi).

=cut
sub display_results {

    print "Your search found <B>$nr</B> records<BR><BR>\n";

    if ($nr gt "0") {
        print "<table border=\"0\" cellpadding=\"4\">\n";
        print "<TR><TH ALIGN=LEFT>ID</td><TH ALIGN=LEFT>SUMMARY</TD><TH ALIGN=LEFT>DATE</TD><TH ALIGN=LEFT>NAME</TD><TH ALIGN=LEFT>GROUP</TD><TH ALIGN=LEFT>STATUS</TD></TR>\n";

        print "<TR><TD></TD></TR>\n";

        while (@row = $sth->fetchrow_array) {

            print "<TR bgcolor=\"#FFFFCC\"><TD>$row[0]&nbsp;</TD>\n";
            print "<TD><a href=\"ALEPHurecord.cgi?$row[0]\">$row[1]</a></td>\n";
            print "<TD>$row[2]&nbsp;</TD>\n";
            print "<TD>$row[3]&nbsp;</TD>\n";
            print "<TD>$row[4]</TD>\n";
            print "<TD>$row[5]</TD>\n";
            print "</TR>\n";

        }
        print "<TR><TD></TD></TR>\n";
        print "</table>\n";
    }

    $rc = $sth->finish;
    $rc = $dbh->disconnect;
}
