#!/usr/local/bin/perl

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
$index = $query->param('index');
$term1 = $query->param('term1');
$term2 = $query->param('term2');
$term3 = $query->param('term3');
$term4 = $query->param('term4');
$term5 = $query->param('term5');
$submitted = $query->param('submitted');


&index;
&print_form;


if ($submitted eq "yes") {
    if ($term1 eq "") {
	print "<B>You must enter a search term!</B><BR><BR>\n";
    }else{
    &do_search;
    &display_results;
}
}


&print_page_end;


sub print_form {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Keyword Search</title>\n";
#    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
#    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</head>\n<body BGCOLOR=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>RxWeb Maintenance Keyword Search</h1>\n";
    print "In development.  Comments to: <cite>gjbush\@umd.edu<\/cite>\n";
    print "<FORM method=\"POST\" action=\"\/cgi-bin\/ALEPH16\/ALEPH\/ALEPHfulltext.cgi\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"RxWeb Maintenance Summaries\" onClick=\"parent.location='ALEPHform2.cgi?id'\"><BR><BR>\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";

    print "<hr>\n";

    print "Select the field to search:&nbsp;\n";
    print "<select name=\"index\" size=1>\n";
    print "<option>text\n";
    print "<option>reply\n";
    print "<option>name\n";
    print "<option>date\n";
    print "</select>\n";
    print "<BR><BR>\n";


    print "Enter a keyword\n";

    print "<input type=text name=term1 size=20><br>\n";
#    print "<input type=text name=term2 size=20><br>\n";
#    print "<input type=text name=term3 size=20><br>\n";
#    print "<input type=text name=term4 size=20><br>\n";
#    print "<input type=text name=term5 size=20>\n";
    print "<BR>\n";
    print "<BR>\n";
    print "<input type=submit>\n";
    print "<hr>\n";
    print "<BR>\n";
    print "<input TYPE=\"hidden\" NAME=\"hidden_filter\" VALUE=\"$hidden_filter\">\n"; 
    print "</FORM>\n";
    &print_terms;
}


sub print_page_end {
    print "</body></html>\n";
}

sub do_search {

#escape the single quotes
$term1 =~ s/\'/\\\'/g;
$term2 =~ s/\'/\\\'/g;
$term3 =~ s/\'/\\\'/g;
$term4 =~ s/\'/\\\'/g;
$term5 =~ s/\'/\\\'/g;
$field =~ s/\'/\\\'/g;


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);



if ($index eq "text")  {

$statement =   "SELECT people.id, report.summary, DATE_FORMAT(date,'%m/%d/%y'), people.name, people.grp, report.status from $table WHERE MATCH($search_index) AGAINST ('$term1') and report.id = people.id";
}

if ($index eq "reply") {

$statement =   "SELECT people.id, report.summary, DATE_FORMAT(reply.date,'%m/%d/%y'), people.name, people.grp, report.status from reply,report,people WHERE MATCH(reply.text,reply.name) AGAINST ('$term1') and report.id = people.id and people.id = reply.parent_id"

}

if ($index eq "date") {

$statement =   "SELECT people.id, report.summary, DATE_FORMAT(reply.date,'%m/%d/%y'), people.name, people.grp, report.status from reply,report,people WHERE (reply.date like '%$term1%' or report.date like '%$term1%') and report.id = people.id and people.id = reply.parent_id"

}





$sth = $dbh->prepare($statement)
	 or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	 or die "Couldn't execute the query: $dbh->errstr";

$nr = $sth->rows;

}


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


sub print_terms {

    print "<b>index:<\/b>$index<BR>\n";
    print "<b>sindex:<\/b>$search_index<BR>\n";
    print "<b>table:<\/b>$table<BR>\n";
    print "<b>kw1:<\/b>$term1<BR>\n";
    print "<b>kw2:<\/b>$term2<BR>\n";
    print "<b>kw3:<\/b>$term3<BR>\n";
    print "<b>kw4:<\/b>$term4<BR>\n";
    print "<b>kw5:<\/b>$term5<BR>\n";
    print "<BR><BR>\n";

}


sub index {

if ($index eq "text") { $search_index = "summary,text" and $table = "report,people" } ;
if ($index eq 'reply') { $search_index = 'text,name' and $table = "report,people,reply" };
if ($index eq 'date') { $search_index = 'report.date,reply.date' };
if ($index eq 'name') { $search_index = 'people.name,reply.name' };

}









