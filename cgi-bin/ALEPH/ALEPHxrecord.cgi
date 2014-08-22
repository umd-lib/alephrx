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

$id = $input{'record_id'};
$yes = $input{'yes'};
$no = $input{'no'};


if ($yes){
    $print = "Record $id has been deleted";

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "DELETE from people WHERE id = $id";
$sth = $dbh->prepare($statement)
	  or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	  or die "Couldn't execute the query: $dbh->errstr";


$statement =   "DELETE from report WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

$statement =   "DELETE from response WHERE parent_id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";


}

if ($no){
    $print = "Delete for record $id has been aborted";
}




$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "SELECT people.id, people.grp, people.campus, people.phone, people.name, report.date, report.status,
		 report.summary, report.supress, report.text FROM people, report WHERE people.id = report.id order by report.id";

$sth = $dbh->prepare($statement)
	 or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	 or die "Couldn't execute the query: $dbh->errstr";




print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD>\n<TITLE>ALEPH Reports Maintenance</TITLE>\n</HEAD>\n<BODY>\n";
print "<center>\n";
print "<H1>ALEPH Reports Maintenance</H1>\n";
print "<FORM>\n";
print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Summaries\" onClick=\"parent.location='\/cgi-bin\/ALEPHsum.cgi?id'\">\n";
print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Reports\" onClick=\"parent.location='\/cgi-bin\/ALEPHsort.cgi?id'\"></p>\n";
print "<FONT SIZE=+1 COLOR=\"#FF0000\">$print</FONT>\n";
print "<TABLE BORDER=0>\n";
print "<BR>\n";
print "<BR>\n";
print "<TR>\n
	  <TD BGCOLOR=\"#FFFFCC\"></TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">id</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">grp</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">campus</a></TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">phone</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">name</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">date</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">status</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">summary</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">suppress</TD>\n
	 <TD BGCOLOR=\"#FFFFCC\">text</TD>\n";

while (@row = $sth->fetchrow_array) {
	 print "<TR>\n";
	 print "<TD VALIGN=TOP WIDTH=41 ><a href=\"ALEPHurecord.cgi?$row[0]\"><IMG SRC=\"\/IMG\/up.gif\" height=12 width=40></a>\n";
	 print "<a href=\"ALEPHdrecord.cgi?$row[0]\"><IMG SRC=\"\/IMG\/del.gif\" height=12 width=40></a></TD>\n";

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
print "</FORM>\n";
print "</TABLE>\n";
print "</center>\n";
$rc = $sth->finish;
$rc = $dbh->disconnect;
print "</BODY>\n</HTML>\n";



###########################

&get_row_count;
&calc_num_pages;
&page_start;
&page_rules
&display_statement;
&display_records_paging;
&print_page_end;


sub display_statement {

$statement =   "SELECT people.id, people.grp, people.campus, people.phone, people.name, report.date, report.status,
		 report.summary, report.supress, report.text, response.name FROM people, report, response WHERE people.id = report.id and people.id = response.parent_id order by report.id LIMIT $limit, 30";

$sth = $dbh->prepare($statement)
	 or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	 or die "Couldn't execute the query: $dbh->errstr";

}



sub page_start {

    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD>\n<TITLE>ALEPH Reports Maintenance</TITLE>\n</HEAD>\n<BODY>\n";
    print "<a NAME=\"top\"></a>\n";
    print "<center>\n";
    print "<H1>ALEPH Reports Maintenance</H1>\n";
    print "<FORM ACTION=\"ALEPHurecord.cgi\" METHOD=POST>\n";
    print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Maintenance  - Summaries\" onClick=\"parent.location='\/cgi-bin\/ALEPH\/ALEPHform2.cgi?id'\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Maintenance - Full Reports\" onClick=\"parent.location='\/cgi-bin\/ALEPH\/ALEPHform2.cgi?'\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Reports\" onClick=\"parent.location='\/cgi-bin\/ALEPHsum.cgi?id'\"></p>\n";
    print "<B>Go to report # :</B>\n";
    print "<INPUT TYPE=\"text\" NAME=\"report\" SIZE=3>\n";
    print "<INPUT TYPE=\"submit\" VALUE=\"GO!\">\n";
    print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<FONT SIZE=+1 COLOR=\"#FF0000\">*</FONT>&nbsp;Indicates a response has been submitted\n";
    print "<BR><BR>\n";
    print "</FORM>\n";
    print "<P><FONT COLOR=\"#FF0000\"> Record $id has been updated!</FONT></P>\n";
    print "<FORM ACTION=\"ALEPHform2.cgi\" METHOD=POST>\n";
}


sub display_records {

print "<TABLE CELLPADDING=3 BORDER=0>\n";
print "<TR>\n
	  <TD></TD>\n
	  <TD COLSPAN=2 BGCOLOR=\"#FFFFCC\"></TD>\n
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1><a href=\"ALEPHform2.cgi?id\">id</TD>\n
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1><a href=\"ALEPHform2.cgi?grp\">grp</TD>\n
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1><a href=\"ALEPHform2.cgi?status\">status</TD>\n 
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1><a href=\"ALEPHform2.cgi?date\">date</TD>\n
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1>suppress</TD>\n
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1>summary</TD>\n
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1><a href=\"ALEPHform2.cgi?people.name\">name</TD>\n
	  <TD BGCOLOR=\"#FFFFCC\"><b><FONT SIZE=-1><a href=\"ALEPHform2.cgi?campus\">campus</a></TD>\n";

while (@row = $sth->fetchrow_array) {

    $rep = "";

    if ($row[10]=~ /\S/) {
	 $rep = "*";
    }

	 print "<TR><TD><FONT SIZE=+1 COLOR=\"#FF0000\">$rep</TD>\n";
	 print "<TD VALIGN=TOP WIDTH=41 ><a href=\"ALEPHurecord.cgi?$row[0]\"><IMG SRC=\"\/IMG\/up.gif\" height=12 width=40></a></TD>\n";
	 print "<TD><a href=\"ALEPHdrecord.cgi?$row[0]\"><IMG SRC=\"\/IMG\/del.gif\" height=12 width=40></a></TD>\n";

	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[0]</TD>\n";
	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[1]</TD>\n";
	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[6]</TD>\n";
	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[5]</TD>\n";
	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[8]</TD>\n";
	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[7]</TD>\n";
	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[4]</TD>\n";
	 print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[2]</TD>\n";
	 print "</TR>\n";
	 $row_id = $row[0];
	 print "</TR>\n";
}
}



sub print_page_end {

print "</FORM>\n";
print "</TABLE>\n";
print "<P>\n";
print "<FONT SIZE=-2><center><a href=\"#top\">TOP</a>\n";
print "</P>\n";
print "</center>\n";
$rc = $sth->finish;
$rc = $dbh->disconnect;
&page_rules;
print "</BODY>\n</HTML>\n";

}



sub fetchresponse {


$dbh_2 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_2 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from response where parent_id = '$row_id'";

$sth_2 = $dbh_2->prepare($statement_2)
    or die "Couldn't prepare the query: $sth_2->errstr";

$rv_2 = $sth_2->execute
    or die "Couldn't execute the query: $dbh_2->errstr";

	  while (@newrow = $sth_2->fetchrow_array) {
	      if ($newrow[0] eq "") {next;
      }else{
    print "<TR>\n";
    print "<TD></TD>\n";
    print "<TD COLSPAN=4 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><i><FONT SIZE=-1 COLOR=\"#A52A2A\">&nbsp;ITD Response:&nbsp;\n";
    print "$newrow[0]</TD>\n";
    print "<TD COLSPAN=2 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"#A52A2A\"><i>Date:&nbsp;$newrow[1]&nbsp;&nbsp;&nbsp;</TD>\n";
    print "<TD COLSPAN=3 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"#A52A2A\"><i>&nbsp;$newrow[2]</TD>\n";
    print "</TR>\n";
    $rdate = $newrow[1];
}
$rc_2 = $sth_2->finish;
$rc_2 = $dbh_2->disconnect;
}
}


###################

sub display_records_paging {

$sort = $value; 

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
}



if ($filter eq  "") {
    $filter = $hidden_filter;
}

&get_row_count;
&calc_num_pages;
&next_paging;
&prev_paging;
&first_paging;
&last_paging;
&page_rules;
&first_last;
#&get_sum_record;
&print_fetch;



sub print_fetch {

print "<TABLE BORDER=0 CELLPADDING=2>\n";
#print "<TR>&nbsp;<TD></TD>\n";
#print "<TR>&nbsp;<TD></TD>\n";
print "<TR>&nbsp;<TD></TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"ALEPHsum.cgi?id\">ID</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B>Summary</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"ALEPHsum.cgi?grp\">Group</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"ALEPHsum.cgi?campus\">Campus</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"ALEPHsum.cgi?status\">Status</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"ALEPHsum.cgi?report.date\">Date</TD></TR>\n";

while (@row = $sth->fetchrow_array) {
   	     $response = "";
   	     &response_get;
	     print "<TR><TD><FONT SIZE=+1 COLOR=\"#FF0000\">$response</FONT>\n</TD>";
  	     print "<TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1>#&nbsp;<a href=\"ALEPHsum_full.cgi?$row[0]\">$row[0]</TD>\n";
	     print "<TD BGCOLOR=\"#BEE4BE\"><FONT SIZE=-1>&nbsp;$row[3]</TD>\n";
	     print "<TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1>&nbsp;$row[1]</TD>\n";
	     print "<TD BGCOLOR=\"#BEE4BE\"><FONT SIZE=-1>&nbsp;$row[2]</TD>\n";
	     print "<TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1>&nbsp;$row[4]</TD>\n";
	     print "<TD BGCOLOR=\"#BEE4BE\"><FONT SIZE=-1>&nbsp;$row[5]</TD>\n";
   	     $row_id = $row[0];
   	     $reply_count = "";
	     $count = 0;
      	     &count_reply;
             print "<TD><FONT SIZE=+1 COLOR=\"#0000FF\">$reply_count</TD></TR>\n";

     }
}


#
#fetches all replies for printing
#

sub fetchreply {

$dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from reply where parent_id = '$row_id'";
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

#
#fetches reponse for printing
#
sub fetchresponse {


$dbh_2 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_2 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from response where parent_id = '$row_id'";

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


sub count_reply {


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_7 =   "SELECT name from reply where parent_id = '$row_id'";
$sth_7 = $dbh->prepare($statement_7)
    or die "Couldn't prepare the query: $sth_7->errstr";

$rv_7 = $sth_7->execute
    or die "Couldn't execute the query: $dbh->errstr";


	  while (@row = $sth_7->fetchrow_array) {
              $count++;
	      $reply_count = '* ' x $count;
	  }

$rc_7 = $sth_7->finish;
$rc_7 = $dbh->disconnect;
}


#creates flag to display when there is a response

sub count_response {


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_8 =   "SELECT name from response where parent_id = '$row_id'";
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


sub response_get {

    if ($row[6] eq "") {
    }else{
	$response = "*";
    }
}


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

#
#queries the database to get the total number of records, used to calculate the
#total number of pages 
#
sub get_row_count {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_10 =   "SELECT COUNT(*) from report, people where report.id = people.id $filter";
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

#
#calculates the total number pages that will be used for all the database
#
sub calc_num_pages {

    $num_pages_1 = $row_count / 30;
    $num_pages_2 = sprintf("%d\n", $num_pages_1);
    if ($num_pages_1 > $num_pages_2){
	$num_pages = $num_pages_2 + 1;
    }else{
    $num_pages = $num_pages_2;
    } 
}

#
#increments the page variable, prints the hidden increment value to pass on to the next page
#
sub next_paging {

    if ($NEXT) {
              $p++;
              print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
}
}

#
#
sub last_paging {

    if ($LAST) {
              $p = $num_pages - 1;
              print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
}
}


#
#
sub first_paging {

    if ($FIRST) {
              $p = 0;
              print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
}
}



#
#decrements the page variable, prints the hidden increment value to pass on to the next page
#
sub prev_paging {

    if ($PREV) {
  	       $p--;
               print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";

}
}


#
#page_rules decides how the next and previous buttons will display.
#
sub page_rules {
     if ($p < 1){
     }else{
     print "<FONT SIZE=-1><INPUT TYPE=\"submit\" VALUE=\"<< FIRST PAGE\" NAME=\"FIRST\">\n";
     print "<INPUT TYPE=\"submit\"  VALUE=\"< PREVIOUS PAGE\" NAME=\"PREV\"></FONT>\n";

 }
     if ($p > $num_pages-2) {
     }else{
	 if ($value =~ /\d/){
    end;
}elsif($LAST) {
  }else{

     print "<FONT SIZE=-1><INPUT TYPE=\"submit\" VALUE=\"NEXT PAGE >\" NAME=\"NEXT\">\n";
     print "<INPUT TYPE=\"submit\" VALUE=\"LAST PAGE >>\" NAME=\"LAST\"></FONT>\n";
 }
 }
$limit = $p * 30; 
     print "<BR>\n";
 }



sub first_last {

if ($LAST) {
    $limit = ($num_pages - 1) * 30;
}
if ($FIRST) {
    $limit = 0;
}
}




#print "<FORM ACTION=\"ALEPHsum.cgi?id\" METHOD=\"post\">\n";
#print "<INPUT TYPE=\"hidden\" name=\"hidden_filter\" VALUE=\"$filter\">\n";
#print "<INPUT TYPE=\"hidden\" name=\"hidden_value\" VALUE=\"$sort\">\n";




#$limit = 30;

sub fetchrow {
while (@row = $sth->fetchrow_array) {
print 
        print "<TR><TD BGCOLOR=\"#F3F49C\" COLSPAN=7><B><i>Report #</i>&nbsp;$row[0]&nbsp;&nbsp;&nbsp;&nbsp;$row[1]</B></TD></FONT></TR>\n";

         print "<TR>\n
	 <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Name</I></TH>\n
	 <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Phone</I></TH>\n
	 <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Date</I></TH>\n
	 <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Group</I></TH>\n
	 <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Campus</I></TH>\n
	 <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Status</I></TH>\n
	 <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Text</I></TH>\n";

     	print "<TR>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[2]</TD>\n";
	print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[3]</TD>\n";
	print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[4]</TD>\n";
	print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[5]</TD>\n";
	print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[6]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[7]</TD>\n";
	print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[8]</TD>\n";
	print "<TD VALIGN=TOP>$row[9]<FONT SIZE=-2><a href=\"ALEPHreply.cgi?$row[0]\">Reply</a></FONT></TD>\n";
        $row_id = $row[0];
        &fetchresponse(); # fetch the response
	print "</TR>\n";
        &fetchreply();    # fetch the replies
 	print "</TR>\n";
	print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
	print "<TR><TD>$reply_count</TD></TR>\n";
    }
}


sub get_sum_record {

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "SELECT people.id, people.grp, people.campus, report.summary, report.status, DATE_FORMAT(report.date,'%m/%d/%y'), response.name FROM people, report, response WHERE report.supress = 'no' and people.id = report.id and people.id = response.parent_id $filter order by $sort LIMIT $limit, 30";

$sth = $dbh->prepare($statement)
	 or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	 or die "Couldn't execute the query: $dbh->errstr";

}


###################

















