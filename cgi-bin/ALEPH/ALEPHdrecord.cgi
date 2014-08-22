#!/usr/local/bin/perl 

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

$record = $ENV{'QUERY_STRING'};

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);


$statement =   "SELECT people.id, people.grp, people.campus, people.phone, people.name, report.date, report.status,
		 report.summary, report.text FROM people, report WHERE people.id = report.id AND people.id = $record";

$sth = $dbh->prepare($statement)
	 or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	 or die "Couldn't execute the query: $dbh->errstr";



print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD>\n<TITLE>ALEPH Record Maintenance</TITLE>\n</HEAD>\n<BODY>\n";
print "<FORM ACTION=\"ALEPHxrecord.cgi\" METHOD=\"post\">\n";
print "<INPUT TYPE=\"hidden\" NAME=\"record_id\" VALUE=\"$record\">\n";
print "<center>\n";
print "<P><h1>ALEPH Records Maintenance</P></h1>\n";
print "<FONT SIZE=+1 COLOR=\"#FF0000\">You are about to delete the following record!</FONT>\n";
print "<P><INPUT TYPE=\"submit\" VALUE=\"YES\" NAME=\"yes\">\n";
print "&nbsp;&nbsp;<INPUT TYPE=\"submit\" VALUE=\"NO\" NAME=\"no\"</P>\n";
print "<BR>\n";
print "<BR>\n";
print "<TABLE BORDER=0 BGCOLOR=\"FFFCC\">\n";
print "<TR>\n
	  <TH>ID</TH>\n
	  <TH ALIGN=LEFT>group</TH>\n
	  <TH ALIGN=LEFT>campus</TH>\n
	  <TH ALIGN=LEFT>phone</TH>\n
	  <TH ALIGN=LEFT>name</TH>\n
	  <TH ALIGN=LEFT>date</TH>\n
	  <TH ALIGN=LEFT>status</TH>\n
	  <TH ALIGN=LEFT>summary</TH>\n
	  <TH ALIGN=LEFT>text</TH>\n";

while (@row = $sth->fetchrow_array) {
	  print "<TR>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[0]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[1]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[2]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[3]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[4]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[5]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[6]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[7]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[8]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[9]</TD>\n";
	  print "</TR>\n";
      }

$rc = $sth->finish;
$rc = $dbh->disconnect;


print "</TABLE>\n";
print "</FORM>\n";
print "<BR>\n";
print "</BODY>\n</HTML>\n";
















