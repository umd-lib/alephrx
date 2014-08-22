#!/usr/local/bin/perl 

use DBI;
use CGI;
#use CGI::Carp qw(fatalsToBrowser);

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
#$sort = $input{'sort'};
$row_id = $id;

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

print "Content-type: text/html\n\n";


if ($id){

if ($id =~ /\D/){
    print "<HTML>\n<HEAD>\n<TITLE>ALEPH Maintenance</TITLE>\n</HEAD>\n<BODY>\n";
    print "<CENTER><H3>You must enter a valid report #</H3>\n";
    print "<form>\n";
    print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
    print "</form>\n";
    print "</CENTER>\n";
} elsif ($id eq ""){
    print "<HTML>\n<HEAD>\n<TITLE>ALEPH Maintenance</TITLE>\n</HEAD>\n<BODY>\n";
    print "<CENTER><H3>You must enter a valid report #</H3>\n";
    print "<form>\n";
    print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
    print "</form>\n";
    print "</CENTER>\n";
} elsif ($id > $max_id){
    print "<HTML>\n<HEAD>\n<TITLE>ALEPH Maintenance</TITLE>\n</HEAD>\n<BODY>\n";
    print "<CENTER><H3>You must enter a valid report #</H3>\n";
    print "<form>\n";
    print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
    print "</form>\n";
    print "</CENTER>\n";
 }else {

print "<HTML>\n<HEAD>\n<TITLE>ALEPH Reports Maintenance - Record $id</TITLE>\n</HEAD>\n<BODY BACKGROUND=\"\/IMG\/bk2.gif\">\n";
print "<center>\n";
print "<H1>ALEPH Reports Maintenance - Record $id</H1>\n";
print "<FORM ACTION=\"\/cgi-bin\/ALEPH\/ALEPHform2.cgi\" METHOD=post>\n";
print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Summaries\" onClick=\"parent.location='\/cgi-bin\/ALEPHsum.cgi?id'\">\n";
#print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Reports\" onClick=\"parent.location='\/cgi-bin\/ALEPHsort.cgi?id'\">\n";
print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Maintenance - Summaries\" onClick=\"parent.location='ALEPHform2.cgi?id'\"></p>\n";
#print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Maintenance - Full Reports\" onClick=\"parent.location='ALEPHform2.cgi?'\"></p>\n";
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "SELECT people.grp, people.campus, people.phone, people.name, report.date, report.status, report.summary, report.text, report.supress FROM people, report WHERE people.id = report.id and people.id = $id";

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

$dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement_1 =   "SELECT name, text from response where response.parent_id  = $id";

$sth_1 = $dbh_1->prepare($statement_1)
    or die "Couldn't prepare the query: $sth_1->errstr";
$rv_1 = $sth_1->execute
    or die "Couldn't execute the query: $dbh_1->errstr";

@row = $sth_1->fetchrow_array;
$rname = $row[0];
$mresponse = $row[1];


print "<INPUT TYPE=\"hidden\" NAME=\"record_id\" VALUE=\"$id\">\n";
print "<INPUT TYPE=\"hidden\" NAME=\"page_increment\" VALUE=\"$p\">\n";
print "<INPUT TYPE=\"hidden\" NAME=\"filter_value\" VALUE=\"$filter_value\">\n";
print "<INPUT TYPE=\"hidden\" NAME=\"sort_value\" VALUE=\"$sort_value\">\n";
#print "<INPUT TYPE=\"hidden\" NAME=\"sort\" VALUE=\"$sort\">\n";
print "<INPUT TYPE=\"hidden\" NAME=\"submit\" VALUE=\"yes\">\n";
print "<TABLE BORDER=0>\n";
print "<b>Group:</b>\n";
print "<select name=\"grp\" size=1>\n";
print "<option>$grp\n";
print "<option>CIRC\n";
print "<option>CIRC2\n";
print "<option>SRQ\n";
print "<option>DLM\n";
print "<option>PAC\n";
print "<option>ITD\n";
print "<option>ALL\n";
print "</select>\n";
print "<B>Campus:</B>\n";
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
print "<B>Status:</B>\n";
print "<select name=\"status\" size=1>\n";
print "<option>$status\n";
print "<option>new\n";
print "<option>pending\n";
print "<option>postponed\n";
print "<option>closed\n";
print "</select>\n";
print "<B>Suppress:</B>\n";
print "<select name=\"suppress\" size=1>\n";
print "<option>$suppress\n";
print "<option>yes\n";
print "<option>no\n";
print "</select>\n";
print "<B>Phone:</B>\n";
print "<input type=text wrap=\"physical\" name=phone size=12 value=$phone>\n";
print "<P>\n";
print "<B>Name:</B>\n";
print "<textarea wrap=\"physical\" name=name maxlength=30>$name</textarea>\n";
#print "<P>\n";
print "<B>Date:</B>\n";
print "<textarea wrap=\"physical\" name=date cols=12 maxlength=12>$date</textarea>\n";
print "<B>Summary:</B>\n";
print "<textarea wrap=\"physical\" name=summary cols=30 maxlength=20>$summary</textarea>\n";
print "<BR><BR><B>Text:</B>\n";
print "<textarea wrap=\"physical\" name=text cols=80 rows=5>$text</textarea><br>\n";
#############################
&fetchreply;
#############################
print "<BR>\n";
print "Enter your name and response below. Select \"Yes\" or \"No\" to email.<BR><BR>\n";
print "<B>Name:</B>\n";
print "<textarea wrap=\"physical\" name=rname cols=30 maxlength=30>$rname</textarea>\n";
print "<BR><BR>\n";
print "<B>Response:</B>\n";
print "<textarea wrap=\"soft\" name=response cols=80 rows=5>$mresponse</textarea>\n";
print "<BR><BR>\n";
print "<INPUT TYPE=submit VALUE=submit>\n";
print "&nbsp;&nbsp;<B>Email Response?</B>\n";
print "<INPUT TYPE=\"radio\" NAME=\"email\" VALUE=\"yes\" checked>Yes\n";
print "<INPUT TYPE=\"radio\" NAME=\"email\" VALUE=\"no\">No\n";
print "</TR>\n";
print "</TABLE><br>\n";
print "<INPUT TYPE=\"hidden\" NAME=\"filter_value\" VALUE=\"$filter_value\">\n";
print "</FORM>\n";
}
}
$rc = $sth->finish;
$rc = $dbh->disconnect;
$rc_1 = $sth_1->finish;
$rc_1 = $dbh_1->disconnect;
print "</BODY>\n</HTML>\n";


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


sub fetchreply {

    $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from reply where parent_id = '$row_id'";
$sth_1 = $dbh_1->prepare($statement_1)
    or die "Couldn't prepare the query: $sth_1->errstr";

$rv_1 = $sth_1->execute
    or die "Couldn't execute the query: $dbh_1->errstr";

    while (@rrow = $sth_1->fetchrow_array) {
    print "<table border=0 width=600>\n";
    print "<tr><td width=\"200\"><i><b><font color=\"#003399\" size=-1>Reply from:&nbsp;&nbsp;$rrow[0]</td>\n";
    print "<td width=\"400\"><i><b><font color=\"#003399\" size=-1>$rrow[1]<br></td></tr>\n";
    print "<tr><td colspan=2><i><font color=\"#003399\" size=-1>$rrow[2]</td></tr>\n";
    print "<br></table>\n";
    }
    $rc_1 = $sth_1->finish;
    $rc_1 = $dbh_1->disconnect;
}





















