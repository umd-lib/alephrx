#!/usr/local/bin/perl

## Jamie Bush, 2004
## RxWeb (AlephRx) version 3.1
## name changed 6/20/06
## basic query

use CGI;
use DBI;

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


&print_form;


if ($submitted eq "yes") {
    if ($term eq "") {
	&error;
    }else {
    &do_search;
    &display_results;
}
}

&print_page_end;


########################################
## Prints the search page form
########################################

sub print_form {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Search</title>\n";
#    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
#    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</head>\n<body BGCOLOR=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>RxWeb Basic Search</h1>\n";
    print "<FORM method=\"POST\" action=\"ALEPHsearch.cgi\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"RxWeb Reports\" onClick=\"parent.location='ALEPHsum.cgi?id'\"></P>\n";
    print "Select the field to search:&nbsp;\n";
    print "<select name=\"field\" size=1>\n";
    print "<option>summary\n";
    print "<option>text\n";
    print "<option>name\n";
    print "<option>reply\n";
    print "</select>\n";
#    print "<BR><BR>\n";
#    print "Enter your single search term and submit\n";
    print "<input type=text name=term size=20>\n";
    print "<input type=submit>\n";
    print "<BR>\n";
    print "</FORM>\n";
}


#########################################
## Prints the end of the page
#########################################

sub print_page_end {
    print "</body></html>\n";
}



##########################################
## Performs the search
##########################################

sub do_search {

#escape the single quotes
$term =~ s/\'/\\\'/g;
$field =~ s/\'/\\\'/g;

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);



if ($field eq "reply") {

$statement =   "SELECT DISTINCT people.id, report.summary, DATE_FORMAT(report.date,'%m/%d/%y'), people.name, people.grp, report.status from people, report, reply where (reply.text LIKE '%$term%' or reply.name LIKE '%$term%') and reply.parent_id = report.id and report.id = people.id order by people.id"; 

} else {


$statement =   "SELECT people.id, report.summary, DATE_FORMAT(date,'%m/%d/%y'), people.name, people.grp, report.status from people, report where $field LIKE '%$term%' and report.id = people.id order by people.id";
}




$sth = $dbh->prepare($statement)
	 or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	 or die "Couldn't execute the query: $dbh->errstr";

$nr = $sth->rows;

}


#########################################
## Prints the results of the search
#########################################

sub display_results {

    print "Your search found <B>$nr</B> records<BR><BR>\n";
 
    if ($nr gt "0") {
    print "<table border=\"0\" cellpadding=\"4\">\n";
    print "<TR><TH ALIGN=LEFT>ID</td><TH ALIGN=LEFT>SUMMARY</TD><TH ALIGN=LEFT>DATE</TD><TH ALIGN=LEFT>NAME</TD><TH ALIGN=LEFT>GROUP</TD><TH ALIGN=LEFT>STATUS</TD></TR>\n";

    print "<TR><TD></TD></TR>\n";

while (@row = $sth->fetchrow_array) {

   print "<TR bgcolor=\"#E9E9E9\"><TD>$row[0]&nbsp;</TD>\n";
   print "<TD><a href=\"ALEPHsum_full.cgi?$row[0]\">$row[1]</a></td>\n";
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


#######################################
## Prints the error message
#######################################

sub error {


    print "<b>You must enter a search term!</b>\n";

}















