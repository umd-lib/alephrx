#!/usr/local/bin/perl

## Jamie Bush, 2004
## RxWeb (AlephRx) version 3.1
## name changed 6/20/06
## stats form

#####################################################
## This is a statistical page which list
## basic statistics out using a series of SQL queries
#####################################################

use CGI;
use DBI;

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";


&query_six;
&page_start;
&query_one;
&query_two;
&query_three;
&query_four;
&query_five;
&page_end;

sub query_one {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT report.date, count(*) from report, people where people.id = report.id and report.supress = 'no' and report.date > '20051231' group by report.date";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";
    print "<TR>\n";
    print "<TD VALIGN=TOP>\n";
    print "<H3>Reports by Date</H3>\n";
    print "<TABLE BORDER=0 CELLPADDING=2>\n";
    print "<TR>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Date</I></TH>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Reports</I></TH>\n";


    while (@row = $sth->fetchrow_array) {
        print "<TR>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[0]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP ALIGN=\"right\"><FONT SIZE=-1>$row[1]</TD>\n";
        print "</TR>\n";
    }

    print "</TABLE>\n";
}

sub query_two {

#$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT people.campus, count(*) from people, report where people.id = report.id and report.supress = 'no' group by people.campus";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";
    print "<TD VALIGN=TOP>\n";
    print "<H3>Reports by Campus</H3>\n";
    print "<TABLE BORDER=0 CELLPADDING=2>\n";
    print "<TR>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Campus</I></TH>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Reports</I></TH>\n";


    while (@row = $sth->fetchrow_array) {
        print "<TR>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[0]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP ALIGN=\"right\"><FONT SIZE=-1>$row[1]</TD>\n";
        print "</TR>\n";
    }

    print "</TABLE>\n";
    print "</TD>\n";
}

sub query_three {

#$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT people.grp, count(*) from people, report where people.id = report.id and report.supress = 'no' group by people.grp";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";
    print "<TD VALIGN=TOP>\n";
    print "<H3>Reports by Group</H3>\n";
    print "<TABLE BORDER=0 CELLPADDING=2>\n";
    print "<TR>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Group</I></TH>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Reports</I></TH>\n";


    while (@row = $sth->fetchrow_array) {
        print "<TR>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[0]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP ALIGN=\"right\"><FONT SIZE=-1>$row[1]</TD>\n";
        print "</TR>\n";
    }

    print "</TABLE>\n";
    print "</TD>\n";
}

sub query_four {

#$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT people.name, count(*) from people, report where people.id = report.id and report.supress = 'no' group by people.name";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";
    print "<TD VALIGN=TOP>\n";
    print "<H3>Reports by User</H3>\n";
    print "<TABLE BORDER=0 CELLPADDING=2>\n";
    print "<TR>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Name</I></TH>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Reports</I></TH>\n";


    while (@row = $sth->fetchrow_array) {
        print "<TR>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[0]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP ALIGN=\"right\"><FONT SIZE=-1>$row[1]</TD>\n";
        print "</TR>\n";
    }

    print "</TABLE>\n";
    print "</TD>\n";
}

sub query_five {

#$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT report.status, count(*) from report, people where people.id = report.id and report.supress = 'no' group by report.status";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";
    print "<TD VALIGN=TOP>\n";
    print "<H3>Reports by Status</H3>\n";
    print "<TABLE BORDER=0 CELLPADDING=2>\n";
    print "<TR>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Status</I></TH>\n
    <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Reports</I></TH>\n";


    while (@row = $sth->fetchrow_array) {
        print "<TR>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[0]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP ALIGN=\"right\"><FONT SIZE=-1>$row[1]</TD>\n";
        print "</TR>\n";
    }

    print "</TABLE>\n";
    print "</TD>\n";
    print "</TR>\n";
}


sub query_six {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "SELECT COUNT(*) from report, people where report.id = people.id and report.supress = 'no' ";
    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";

    $rv_10 = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";

    while (@crow = $sth->fetchrow_array) {
        $row_count = $crow[0];
    }
}

sub page_start {

    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD>\n<TITLE>RxWeb Statistics</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
    print "<FORM>\n";
    print "<center>\n";
    print "<H1>RxWeb Statistics</H1>\n";
    print "<P><INPUT TYPE=\"button\" VALUE=\"RxWeb Form\" onClick=\"parent.location ='\/cgi-bin\/ALEPHform.cgi'\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"RxWeb\" onClick=\"parent.location='ALEPHsum.cgi?id'\"></p>\n";
    print "</FORM>\n";
#print "</center>\n";
    print "<h2>Total Reports = $row_count</h2>\n";
    print "<TABLE CELLPADDING=20>\n";
}

sub page_end {


    $rc = $sth->finish;
    $rc = $dbh->disconnect;
    print "</TABLE>\n";
    print "</BODY>\n</HTML>\n";

}
