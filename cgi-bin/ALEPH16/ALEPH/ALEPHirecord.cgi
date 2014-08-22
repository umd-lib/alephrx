#!/usr/local/bin/perl 

use DBI;
#use CGI::Carp qw(fatalsToBrowser);
use CGI;

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$id = "";
$mailprog = $ENV{ALEPHRX_MAILER};
$from = "limstest\@itd.umd.edu (ALEPH Web Report)";
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

  #Escape the single quotes 
  $value =~ s/\'/\\\'/g;

  #Copy the name and value into the hash
  $input{$name} = $value;
}

$id = $input{'record_id'};
$grp = $input{'grp'};
$campus = $input{'campus'};
$phone = $input{'phone'};
$name = $input{'name'};
$date = $input{'date'};
$status = $input{'status'};
$summary = $input{'summary'};
$text = $input{'text'};
$rname = $input{'rname'};
$response = $input{'response'};
$suppress = $input{'suppress'};
$email = $input{'email'};
$mail = $input{'mail'};
$cataloger = $input{'cataloger'};
#$limit = $input{'limit'};

$NEXT = $input{'NEXT'};
$PREV = $input{'PREV'};
$LAST = $input{'LAST'};
$FIRST = $input{'FIRST'};
$p = $input{'page_increment'};
$hidden_filter = $input{'hidden_filter'};
$hidden_value = $input{'hidden_value'};


&get_row_count;
&calc_num_pages;
&insert;
&page_start;
&sort;
&page_rules
&display_records_paging;
&print_page_end;


&recipient;

if ($rname eq "") {
}else{
if ($mail eq "yes"){
    &response_date;
    &mail;
}
}




sub insert {

if ($grp) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE people SET people.grp = '$grp' WHERE id = $id";
$sth = $dbh->prepare($statement)
	   or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	   or die "Couldn't execute the query: $dbh->errstr";

}


if ($status) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE report SET report.status = '$status' WHERE id = $id";
$sth = $dbh->prepare($statement)
	    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	    or die "Couldn't execute the query: $dbh->errstr";

}

if ($text) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE report SET report.text = '$text' WHERE id = $id";
$sth = $dbh->prepare($statement)
	    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	    or die "Couldn't execute the query: $dbh->errstr";

}

if ($summary) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE report SET report.summary = '$summary' WHERE id = $id";
$sth = $dbh->prepare($statement)
	    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	    or die "Couldn't execute the query: $dbh->errstr";

}

if ($campus) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE people SET people.campus = '$campus' WHERE id = $id";
$sth = $dbh->prepare($statement)
	    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	    or die "Couldn't execute the query: $dbh->errstr";

}

if ($date) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE report SET report.date = '$date' WHERE id = $id";
$sth = $dbh->prepare($statement)
	    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	    or die "Couldn't execute the query: $dbh->errstr";

}

if ($name) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE people SET people.name = '$name' WHERE id = $id";
$sth = $dbh->prepare($statement)
	    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	    or die "Couldn't execute the query: $dbh->errstr";

}

if ($phone) {
$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "UPDATE people SET people.phone = '$phone' WHERE id = $id";
$sth = $dbh->prepare($statement)
	    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
	    or die "Couldn't execute the query: $dbh->errstr";

}

if ($rname) {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "UPDATE response SET response.name ='$rname', response.text = '$response', response.date = NOW() where parent_id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

}

if ($suppress) {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "UPDATE report SET report.supress ='$suppress' where report.id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

}

if ($cataloger) {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "UPDATE report SET report.cataloger ='$cataloger' where report.id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";


}
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
    print "&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<FONT SIZE=+1 COLOR=\"#FF0000\">*</FONT>&nbsp;Indicates a response has been submitted\n";
    print "&nbsp;&nbsp;&nbsp;<FONT SIZE=-1><B>Record Count = $row_count</B></FONT>\n";
    print "<BR>\n";
    print "</FORM>\n";
    print "<P><FONT COLOR=\"#FF0000\"> Record $id has been updated!</FONT></P>\n";
    print "<FORM ACTION=\"ALEPHform2.cgi\" METHOD=POST>\n";
    print ">>$cataloger<<<br>\n";
}



sub print_page_end {

print "</TABLE>\n";
$rc = $sth->finish;
$rc = $dbh->disconnect;
print "<BR>\n";
&page_rules;
print "</FORM>\n";
print "<FONT SIZE=-2><center><a href=\"#top\">TOP</a>\n";
print "</center>\n";
print "</BODY>\n</HTML>\n";

}



#sub mail {
#
#    if ($email eq "yes") {
#	  open (MAIL,"|$mailprog -t");
#	  print MAIL "To: $recipient\n";
#	  print MAIL "From: $from\n";
#	  print MAIL "Subject: RE:#$id:$summary\n";
#	  print MAIL "This is a RESPONSE to the ALEPH Web Report listed below\n";
#	  print MAIL "http:\/\/www.itd.umd.edu\/cgi-bin\/ALEPHsum_full.cgi?$id\n";
#	  print MAIL "\n";
#	  print MAIL "\n";
#	  print MAIL "Response Submitted by: $rname\n";
#	  print MAIL "     Date of Response: $rdate\n";
#	  print MAIL "     Functional Group: $grp\n";
#	  print MAIL "   Original Report # : $id\n";
#	  print MAIL "\n";
#	  print MAIL "Response: $response\n";
#	  print MAIL "\n";
#	  print MAIL "<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>\n";
#	  print MAIL "\n";
#	  print MAIL "             Report #: $id\n";
#	  print MAIL "                 Date: $date\n"; 
#	  print MAIL "         Submitted by: $name\n";
#	  print MAIL "\n";
#	  print MAIL "\n";
#	  print MAIL "Report: $text\n";
#	  print MAIL "\n";
#	  CLOSE (MAIL);
#	  $row_id = "";
#     } else {
#	  end;}
#}
#

sub mail {

    if ($email eq "yes") {
        open (MAIL,"|$mailprog -t");
        print MAIL "To: $recipient\n";
        print MAIL "From: $from\n";
        print MAIL "Subject: RE:#$id:$summary\n";
        print MAIL "This is a RESPONSE to the ALEPH Web Report listed below\n";
        print MAIL "http:\/\/www.itd.umd.edu\/cgi-bin\/ALEPHsum_full.cgi?$id\n";
        print MAIL "\n";
        print MAIL "\n";
        print MAIL "Response Submitted by: $rname\n";
        print MAIL "     Date of Response: $rdate\n";
        print MAIL "     Functional Group: $grp\n";
        print MAIL "   Original Report # : $id\n";
        print MAIL "\n";
        print MAIL "Response: $response\n";
        print MAIL "\n";
        print MAIL "<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>\n";
        print MAIL "\n";
        print MAIL "             Report #: $id\n";
	print MAIL "                 Date: $date\n";
        print MAIL "         Submitted by: $name\n";
        print MAIL "\n";
        print MAIL "\n";
        print MAIL "Report: $text\n";
        print MAIL "\n";
        CLOSE (MAIL);
        $row_id = "";
    } else {
        end;}
}




sub recipient {

    if ($grp eq "Circulation") {
	$recipient = "jamieb\@itd.umd.edu";
    }
    if ($grp eq "Technical") {
	$recipient = "jamieb\@itd.umd.edu";
    }
    if ($grp eq "Web OPAC") {
	$recipient = "jamieb\@itd.umd.edu";
    }

    if ($grp eq "Cataloging") {
	$recipient = "jamieb\@itd.umd.edu";
    }

    if ($grp eq "Serials") {
	$recipient = "jamieb\@itd.umd.edu";
    }

    if ($grp eq "Acquisitions") {
	$recipient = "jamieb\@itd.umd.edu";
    }

    if ($grp eq "Item Maintenance") {
	$recipient = "jamieb\@itd.umd.edu";
    }

    if ($grp eq "Reserves") {
	$recipient = "jamieb\@itd.umd.edu";
    }

    if ($grp eq "other") {
	$recipient = "jamieb\@itd.umd.edu";
    }

}



sub response_date {

	$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
	$statement =   "SELECT date from response where parent_id = $id";

$sth_6 = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth_6->errstr";
$rv_6 = $sth_6->execute
    or die "Couldn't execute the query: $dbh->errstr";

	while (@row = $sth_6->fetchrow_array) {
	    $rdate = $row[0];
    }
$rc_6 = $sth_6->finish;
$rc_2 = $dbh->disconnect
    }



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


sub sort {

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement =   "SELECT people.id, people.grp, people.campus, people.phone, people.name, report.date, report.status, report.summary, report.supress, response.name FROM people, report, response WHERE people.id = report.id and people.id = response.parent_id order by people.id LIMIT $limit, 30";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";
 print "<TABLE BORDER=0 CELLPADDING=3>\n";
 print "<TR>\n
	   <TD></TD>\n
	   <TD></TD>\n
	   <TD></TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b><a href=\"ALEPHform2.cgi?id\">id</TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b><a href=\"ALEPHform2.cgi?grp\">grp</TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b><a href=\"ALEPHform2.cgi?status\">status</TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b><a href=\"ALEPHform2.cgi?date\">date</TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b>suppress</TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b>summary</TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b><a href=\"ALEPHform2.cgi?people.name\">name</TD>\n
	   <TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1><b><a href=\"ALEPHform2.cgi?campus\">campus</a></TD>\n
	   </TR>\n";

    while (@row = $sth->fetchrow_array) {

	  $rep = "";

	  if ($row[9]=~ /\S/) {
	      $rep = "*";
	  }

	  print "<TR><TD><FONT SIZE=+1 COLOR=\"#FF0000\">$rep</TD>\n";
	  print "<TD VALIGN=BOTTOM WIDTH=41 ><a href=\"ALEPHurecord.cgi?$row[0]\"><IMG SRC=\"\/IMG\/up.gif\" height=12 width=40 ALT=\"update\"></a>\n";
	  print "<TD VALIGN=TOP><a href=\"ALEPHdrecord.cgi?$row[0]\"><IMG SRC=\"\/IMG\/del.gif\" height=12 width=40 ALT=\"delete\"></a></TD>\n";


	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[0]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[1]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[6]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[5]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[8]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[7]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[4]</TD>\n";
	  print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1>$row[2]</TD>\n";

	  print "</TR>\n";
	  $row_id = $row[0];
    }
}



#sub filter {
#
#    if ($CIRC) {
#	 $filter = "and people.grp = 'CIRC'";
#    }
#
#    if ($PAC) {
#	 $filter = "and people.grp = 'PAC'";
#    }
#
#    if ($SRQ) {
#	 $filter = "and people.grp = 'SRQ'";
#    }
#    
#    if ($DLM) {
#	 $filter = "and people.grp = 'DLM'";
#    }
#    
#    if ($CLOSED) {
#	 $filter = "and report.status = 'closed'";
#    }
#    
#    if ($PEND) {
#	 $filter = "and report.status = 'pending'";
#    }
#    
#    if ($POST) {
#	 $filter = "and report.status = 'postpone'";
#    }
#    
#    if ($NEW) {
#	 $filter = "and report.status = 'new'";
#    }
#    
#    if ($TECH) {
#	 $filter = "and people.grp = 'TECH'";
#    }
#}
#
#
