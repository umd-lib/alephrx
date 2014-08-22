#!/usr/local/bin/perl

use CGI;
use DBI;
use CGI::Carp qw(fatalsToBrowser);
use IO::Handle;
use lib "/lims/lib/perl";
use Lims::IM;






# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$id = "";
$rname = "";
$response = "";
#$recipient = "jamieb\@itd.umd.edu";
$from = "aleph\@itd.umd.edu (AlephRx)";
$mailprog = $ENV{ALEPHRX_MAILER};
$query = new CGI;







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
  #Escape the backslashes
#  $value =~ s/\\/\\\\/g;

  #Copy the name and value into the hash
    $input{$name} = $value;
}




    $name = $query->param('name');
    $id = $query->param('id');
    $campus = $query->param('campus');
    $status = $query->param('status');
    $text = $query->param('text');
    $summary = $query->param('summary');
    $date = $query->param('date');
    $grp = $query->param('grp');
    $time = $query->param('time');
    $hour = $query->param('ampm');
    $phone = $query->param('phone');
    $email = $query->param('email');
    $email1 = $query->param('email1');
    $email2 = $query->param('email2');
    $email3 = $query->param('email3');
    $email3a = $query->param('email3a');
    $email4 = $query->param('email4');
    $email4a = $query->param('email4a');
    $cataloger = $query->param('cataloger');
    $email_config = $query->param('email_config');


#to be used in email before single quotes are escaped
$summary_mail = $summary;
$name_mail = $name;
$text_mail = $text;

#escape the single quotes
$summary =~ s/\'/\\\'/g;
$name =~ s/\'/\\\'/g;
$text =~ s/\'/\\\'/g;
$cataloger =~ s/\'/\\\'/g;
$email =~ s/\'/\\\'/g;
$phone =~ s/\'/\\\'/g;
&recipient;

#escape the backslashes
#$summary =~ s/\\/\\\\/g;
#$name =~ s/\\/\\\\/g;
#$text =~ s/\\/\\\\/g;



#&im_message;


if ($query->param('submitted')) {

    $error_message = "";
    &match;
    &validate_form;

    if ($error_message ne "") {
	&display_error;

    } elsif ($error_message eq "") {
	&insert_data;
#	&display_record;
	&recipient;
	&email_config;
#	&change_recipient;
#	&mail;
    } 
    } else {
           &set_initial_values;
            &print_form;
       }



sub validate_form {

   if ($match_rows gt '0') {
	   $error_message .= "<LI>This is a duplicate record. <B>Procedure not allowed.</B> Clear the form and enter a new report. \n";
   }


   if ($grp eq "") {
	  $error_message .= "<LI>Please select a functional area.\n";
   }

   if ($campus eq "") {
	  $error_message .= "<LI>Please select a campus.\n";
   }

   if ($name eq "") {
	  $error_message .= "<LI>Please enter a name.\n";
   }

   if ($phone =~ /\d\d\d-\d\d\d-\d\d\d\d/) {
   } else {
	   $error_message .= "<LI> Please enter a valid phone number.\n";
   }

#    if ($date =~ /(01|02|03|04|05|06|07|08|09|10|11|12)\/(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)/) {
#    } else {
#	      $error_message .= "<LI>Please enter a valid date for your report.\n";
#    }
#
#    if ($time =~ /(0|1|2|3|4|5|6|7|8|9|10|11|12):(00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50|51|52|53|54|55|56|57|58|59)/) {
#    } else {
#	    $error_message .= "<LI> Please enter a valid time for your report.\n";
#    }

   if ($summary eq "") {
	  $error_message .= "<LI>Please enter a summary.\n";
   }

   if ($text eq "") {
	  $error_message .= "<LI>Please enter the text for your report.\n";
   }

   if ($email =~ /(@.*@)|(,)|\s+|(\.\.)|(@\.)|(\.@)|(^\.)|(\.$)/ || ($email !~ /^.+\@localhost$/ && $email !~ /^.+\@\[?(\w|[-.])+\.[a-zA-Z]{2,3}|[0-9]{1,3}\]?$/))             { $error_message .= "<LI>Please enter a valid email address.\n"; }
 
   
}						       						      
   

sub set_initial_values {
    $name = "";
    $id = "";
    $campus = "";
    $status = "new";
    $text = "";
    $summary = "";
    $date = "";
    $grp = "";
    $time = "";
    $hour = "";
    $phone = "";
    $email = "";
    $cataloger = "";
}

sub print_form {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>AlephRx Form</title>\n";
#    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
#    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</head>\n<body bgcolor=\"#98AFC7\">\n";
    print "<center>\n";
    print "<IMG SRC=\"\/IMG\/alephrx.jpg\">\n";
    print "<FORM ACTION=\"ALEPHform.cgi\" METHOD=\"post\">\n";
    print "<center>\n";
    print "<INPUT TYPE=\"button\" VALUE=\"AlephRx\" onClick=\"parent.location='ALEPHsum.cgi?id'\"></P>\n";
#    print "IMPORTANT: Read the <a href=\"http:\/\/www.itd.umd.edu/LIMS3/helpscreen-1.html\">Report Request</a> help screen before submitting a report.\n";
    print "<table width=\"640\" border=\"0\"><tr><td>\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"email_config\" VALUE=\"no\">\n";

    print "<table border=0>\n";

    print "<tr valign=\"top\">\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\"><FONT SIZE=-1>Reported By:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\">\n";
    print "<input type=text name=name size=20 maxlength=30></td>\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\"><FONT SIZE=-1>Email:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\">\n";
    print "<input type=text name=email size=20 maxlength=30></td>\n";
    print "</tr>\n";

    print "<tr valign=\"top\">\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\"><FONT SIZE=-1>Phone:</FONT>&nbsp;</td><td bgcolor=\"#CCCCCC\">\n"; 
    print "<input type=text name=phone size=12 maxlength=12><FONT SIZE=-1>&nbsp;301-555-1212</td>\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\" ><FONT SIZE=-1>Campus:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\"> <select name=campus size=1>\n";
    print "<option>\n";
    print "<option>BSU \n";
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
    print "</select></td>\n";
    print "</tr>\n";
    print "<tr valign=\"top\">\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\" ><FONT SIZE=-1>Functional Area:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\"> <select name=\"grp\" size=1>\n";
    print "<option>\n";
    print "<option>Acquisitions\n";
    print "<option>Cataloging\n";
    print "<option>Circulation\n";
    print "<option>Item Maintenance\n";
    print "<option>Reserves\n";
    print "<option>Serials\n";
    print "<option>Technical\n";
    print "<option>Web OPAC\n";
    print "<option>Report request\n";
    print "<option>other\n";
    print "</select>\n";
    print "</td>\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\"><FONT SIZE=-1>Submitted By:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\"> <input type=text name=cataloger size=20 maxlength=50></td>\n";
    print "</tr>\n";

    print "<tr valign=\"top\" colspan=4>\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\" ><FONT SIZE=-1>Problem Summary:</FONT>&nbsp;</td>\n"; 
    print "<td bgcolor=\"#CCCCCC\"> <input type=text name=summary size=20 maxlength=50></td>\n";
    print "<th bgcolor=\"#FFFF00\"  align=\"right\" ><FONT SIZE=-1>Report Status:</FONT>&nbsp;</td>\n"; 
    print "<td bgcolor=\"#CCCCCC\"> <select name=status size=1</td>\n";
    print "<option>new\n";
    print "<option>change request\n";
    print "</select>\n";
    print "</td>\n";
    print "</tr>\n";

    print "<tr valign=\"top\">\n";
    print "<br>\n";
    print "</tr>\n";
    print "<tr valign=\"top\">\n";
    print "<td colspan=4><CENTER><p><FONT SIZE=-1>Please report only one problem at a time. Your report should include a complete description of the problem.\n";
    print "Please remember to include any barcodes, user names or id's you are using if applicable to the problem.<br> \n";
#    print "Please select the \"Report Request\" link above for details on requesting a report.\n";
    print "</P>\n";
    print "</td>\n";
    print "</tr>\n";
    print "<tr>\n";
    print "<td colspan=4>\n";
    print "<center>\n";
    print "<B>Complete description:</B>\n";
    print "<BR>\n";
    print "<textarea wrap=\"physical\" name=text cols=60 rows=10></textarea>\n";
    print "</td>\n";
    print "<tr>\n";
    print "<td colspan=2 align=\"center\"><input type=submit value=\"SUBMIT\"></td>\n";
    print "<td colspan=2 align=\"center\"><input type=reset value=\"CLEAR\"></td>\n";
    print "</tr>\n";
#    print "<tr><td colspan=4><center><a href=\"\/LIMS3\/ALEPH_Help.html\">Help</a></td></tr>\n";
    print "</table>\n";
    print "</form>\n";
    print "</table>\n";
}


sub print_page_start {
    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>AlephRx Frm</title>\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<IMG source=\"\/IMG\/alephrx.jpg\">\n";
    print "</body>\n</html>\n";
}

sub print_page_end {
    print "</body>\n";
    print "<HEAD>\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</HEAD></HTML>\n";
}



sub display_record {

#if ($email3) { &Check_Email($email3a);}
#if ($email4) { &Check_Email($email4a);}
#
#if ($email_check > 0) {
#    &bad_email_display;
#
#} else {
#


print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD>\n<TITLE>AlephRx  Reports Summaries</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
print "<FORM ACTION=\"ALEPHsum.cgi\" METHOD=\"post\">\n";
print "<center>\n";
print "<H1>AlephRx</H1>\n";
print "<FONT SIZE=+1 COLOR=\"#FF0000\">Your have submitted report number #$last</FONT>\n";
    print "here>>$error_message>>$match_rows\n";
print "<P><INPUT TYPE=\"button\" VALUE=\"AlephRx Form\" onClick=\"parent.location ='ALEPHform.cgi'\">\n";
print "<INPUT TYPE=\"button\" VALUE=\"AlephRx\" onClick=\"parent.location='ALEPHsum.cgi?id'\"></p>\n";
print "<TABLE BORDER=0 CELLPADDING=2>\n";

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);


$statement =   "SELECT people.id, report.summary, people.name, people.phone, DATE_FORMAT(report.date,'%m/%d/%y'), people.grp, people.campus, report.status, report.text FROM people, report WHERE people.id = '$last' and people.id = report.id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

while (@row = $sth->fetchrow_array) {
	  print "<TR><TD BGCOLOR=\"#FFFF00\" COLSPAN=7><B><i>Report #</i>&nbsp;$row[0]&nbsp;&nbsp;&nbsp;&nbsp;$row[1]</B></TD></FONT></TR>\n";
	   print "<TR>\n
	   <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Name</I></TH>\n
	   <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Phone</I></TH>\n
	   <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Date</I></TH>\n
	   <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Group</I></TH>\n
	   <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Campus</I></TH>\n
	   <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Status</I></TH>\n
	   <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Text</I></TH>\n";
#        print "<TR><TD COLSPAN=8><FONT SIZE=-1><B><i>&nbsp;</TD></TR>\n";



	  print "<TR>\n";
	  print "<TD BGCOLOR=\"#E8E8E8\" VALIGN=TOP>$row[2]</TD>\n";
	  print "<TD BGCOLOR=\"#E8E8E8\" VALIGN=TOP>$row[3]</TD>\n";
	  print "<TD BGCOLOR=\"#E8E8E8\" VALIGN=TOP>$row[4]</TD>\n";
	  print "<TD BGCOLOR=\"#E8E8E8\" VALIGN=TOP>$row[5]</TD>\n";
	  print "<TD BGCOLOR=\"#E8E8E8\" VALIGN=TOP>$row[6]</TD>\n";
	  print "<TD BGCOLOR=\"#E8E8E8\" VALIGN=TOP>$row[7]</TD>\n";
	  print "<TD BGCOLOR=\"#E8E8E8\" VALIGN=TOP>$row[8]</TD>\n";
	  print "<TD VALIGN=TOP>$row[9]<FONT SIZE=-2><a href=\"ALEPHreply.cgi?$row[0]\">Reply</a></FONT></TD>\n";
	  $row_id = $row[0];
	  print "</TR>\n";
	  print "</TR>\n";
	  print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
      }
print "</TABLE>\n";
###################
#for testing
###################
#print "$final_email_list\n";
#print "1:$email1\n";
#print "2:$email2\n";
#print "3:$email3\n";
#print "3a:$email3a\n";
#print "4:$email4\n";
#print "4a:$email4a\n";
####################
$rc = $sth->finish;
$rc = $dbh->disconnect;
print "</FORM>\n";
print "</BODY>\n</HTML>\n";


#}

}



sub insert_data {


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "INSERT INTO people (name, grp, campus, phone, email) VALUES 
               ('$name','$grp','$campus','$phone','$email')";

$query1 = $statement;

$sth = $dbh->prepare($statement)
	or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	or die "Couldn't execute the query: $dbh->errstr";



$statement =   "SELECT last_insert_id()";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";

$rc = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

$last = $sth->fetchrow_array; 


$statement =   "INSERT INTO report (id, date, status, summary, text, cataloger) VALUES 
               (LAST_INSERT_ID(),NOW(),'$status','$summary','$text','$cataloger')";

$query2 = $statement;

$sth = $dbh->prepare($statement)
	or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	or die "Couldn't execute the query: $statement";


#$statement =   "INSERT into response (parent_id, name, date, text) VALUES
#		    ('$last','$rname',NOW(),'$response')";
#
#$query3 = $statement;
#
#$sth = $dbh->prepare($statement)
#    or die "Couldn't prepare the query: $dbh->errstr";
#
#$rv = $sth->execute
#    or die "Couldn't execute the query: $dbh->errstr";
#


$rc = $sth->finish;
$rc = $dbh->disconnect

}


sub mail {

    open (MAIL,"|$mailprog -t");
    print MAIL "To:$recipient\n";
#    print MAIL "Cc:$email\n";
    print MAIL "From: $from\n";
    print MAIL "Subject: #$row_id:$status:$summary_mail\n";
    print MAIL "The following AlephRx can be viewed online at:\n"; 
    print MAIL "http://www.itd.umd.edu/cgi-bin/ALEPH16/ALEPHsum_full.cgi?$row_id\n";
    print MAIL "\n";
    print MAIL "Report Submitted by: $name_mail\n";
    print MAIL "           Report# : $row_id\n";
    print MAIL "    Date of problem: $date\n";
    print MAIL "    Time of problem: $time$hour\n";
    print MAIL "   Functional Group: $grp\n";
    print MAIL "             Campus: $campus\n";
    print MAIL "             Status: $status\n";
    print MAIL "\n";
    print MAIL "     Problem Report: $text_mail\n"; 
    print MAIL "\n";
    close (MAIL);
}

sub recipient {

if ($grp eq "Circulation") {
    $recipient = "av16testers\@itd.umd.edu";
}
if ($grp eq "Technical") {
    $recipient = "av16testers\@itd.umd.edu";
}
if ($grp eq "Web OPAC") {
    $recipient = "av16testers\@itd.umd.edu";
}

if ($grp eq "Cataloging") {
    $recipient = "av16testers\@itd.umd.edu";
}

if ($grp eq "Serials") {
    $recipient = "av16testers\@itd.umd.edu";
}

if ($grp eq "Acquisitions") {
    $recipient = "av16testers\@itd.umd.edu";
}

if ($grp eq "Item Maintenance") {
    $recipient = "av16testers\@itd.umd.edu";
}

if ($grp eq "Reserves") {
    $recipient = "av16testers\@itd.umd.edu";
}

if ($grp eq "other") {
    $recipient = "av16testers\@itd.umd.edu";
}

if ($grp eq "Report request") {
    $recipient = "av16testers\@itd.umd.edu";
}
}


sub change_recipient  {

    if ($status eq "change request") {
    $recipient = "av16testers\@itd.umd.edu";
}

}


sub get_full_record {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "SELECT people.id, report.summary, people.name, people.phone, DATE_FORMAT(report.date,'%m/%d/%y'), people.grp, people.campus, report.status, report.text FROM people, report WHERE people.id = $value and people.id = report.id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";


    while (@row = $sth->fetchrow_array) {
        print "<TR><TD BGCOLOR=\"#F3F49C\" COLSPAN=7><B><i>Report #</i>&nbsp;$row[0]&nbsp;&nbsp;&nbsp;&nbsp;$row[1]</B></TD></FONT></TR>\n";

         print "<TR>\n
         <TH BGCOLOR=\"#FFCC66\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Name</I></TH>\n
         <TH BGCOLOR=\"#FFCC66\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Phone</I></TH>\n
         <TH BGCOLOR=\"#FFCC66\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Date</I></TH>\n
         <TH BGCOLOR=\"#FFCC66\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Group</I></TH>\n
         <TH BGCOLOR=\"#FFCC66\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Campus</I></TH>\n
         <TH BGCOLOR=\"#FFCC66\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Status</I></TH>\n
         <TH BGCOLOR=\"#FFCC66\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Text</I></TH>\n";

        print "<TR>\n";
        print "<TD BGCOLOR=\"#CCCCCC\" VALIGN=TOP>$row[2]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\" VALIGN=TOP>$row[3]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\" VALIGN=TOP>$row[4]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\" VALIGN=TOP>$row[5]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\" VALIGN=TOP>$row[6]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\" VALIGN=TOP>$row[7]</TD>\n";
        print "<TD BGCOLOR=\"#CCCCCC\" VALIGN=TOP>$row[8]</TD>\n";
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


sub match{

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement = "select report.summary, people.phone, people.name from report, people WHERE people.id = report.id and report.summary = '$summary' and  people.phone = '$phone' and people.name = '$name'";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    $match_rows = $sth->rows;



}




sub mail_query {

    open (MAIL,"|$mailprog -t");
    print MAIL "To: jamieb\@kitabu.umd.edu\n";
    print MAIL "From: $from\n";
    print MAIL "Subject: #query\n";
    print MAIL "$query1\n";
    print MAIL "$query2\n";
    print MAIL "$query3\n";
    close (MAIL);
}


sub im_message {

    $msg = "AlephRx Web Form Submission\r
Status: $status\r
Group: $grp\r
Name: $name\r
Summary: $summary\r
Text: ";

    $msg .= (length($text) < 120 ? $text : substr($text,0,120) . " [snip]");
}




sub email_config {

    $display = "yes";
    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>AlephRx Email Configuration</title>\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
#    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</head>\n<body bgcolor=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>AlephRx Email Configuration</h1>\n";
    print "<h3>Please confirm the Email configuration for your report </h3>\n";
    print "<FORM ACTION=\"ALEPHemail.cgi\" METHOD=\"post\">\n";
    print "<table>\n";
    &email_display;
#    print "<tr><td>Community of interest: $grp</td></tr>\n";
#    print "<tr><td>     Individual email: $email</td></tr>\n";
    print "<tr><td align=\"left\">\n";
    print "<p><input TYPE=\"submit\" VALUE=\"Confirm Email Configuration\"></p>\n";
    print "<INPUT TYPE=\"hidden\" name=\"email_config\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"id\" VALUE=\"$last\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"name\" VALUE=\"$name\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"text\" VALUE=\"$text\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"summary\" VALUE=\"$summary\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"phone\" VALUE=\"$phone\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"campus\" VALUE=\"$campus\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"status\" VALUE=\"$status\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"grp\" VALUE=\"$grp\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"email\" VALUE=\"$email\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"cataloger\" VALUE=\"$cataloger\">\n";
    print "</form>\n";
    print "</td></tr></table>\n";
    print "</body>\n</html>\n";

}





sub email_display_outdated {


    print "<TABLE border=\"0\" width=\"30%\">\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "<tr><td colspan=\"2\"><hr></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email1\" VALUE=\"email1\" checked>Community:&nbsp;&nbsp;<cite><b>$recipient</b></cite></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email2\" VALUE=\"email2\" checked>Reported by:&nbsp;&nbsp;<b><cite>$email</b></cite></td></tr>\n";
#    print "<td width=\"20\">&nbsp;</td>\n";
    print "<tr><td><INPUT TYPE=\"checkbox\" NAME=\"email3\" VALUE=\"yes\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email3a\"  cols=80 maxlength=80></td></tr>\n";
#    print "<td width=\"20\">&nbsp;</td>\n";
    print "<tr><td width=\"120\"><INPUT TYPE=\"checkbox\" NAME=\"email4\" VALUE=\"yes\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email4a\"  cols=80 maxlength=80></td></tr>\n";
    print "</TABLE><br>\n";

}


sub email_options {

    if ($email1) {
        $recipient =~ s/\s+//g;
        $recipient =~ s/,//g;
        $rec1 = "$recipient";
    }

    if ($email2) {
        $email =~ s/\s+//g;
        $email =~ s/,//g;
        $rec2 = ",$email";
    }

    if ($email3) {
        $email3a =~ s/\s+//g;
        $email3a =~ s/,//g;
        $rec3 = ",$email3a";
    }

    if ($email4) {
        $email4a =~ s/\s+//g;
        $email4a =~ s/,//g;
        $rec4 = ",$email4a,";
    }

    $final_email_list = $rec1 . $rec2 . $rec3 . $rec4 . $email5;

}




sub Check_Email

{
    if ($_[0] =~ /(@.*@)|(,)|\s+|(\.\.)|(@\.)|(\.@)|(^\.)|(\.$)/ || ($_[0] !~ /^.+\@localhost$/ && $_[0] !~ /^.+\@\[?(\w|[-.])+\.[a-zA-Z]{2,3}|[0-9]{1,3}\]?$/))             { \
																						   $email_check++; push @store, $_[0]; }
        else { }
    }


sub bad_email_display {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>AlephRx Reply</title>\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<h1>AlephRx Reply</h1>\n";
    print "<h3>Not a valid email address.</h3>\n";
    print "<table>\n";
    print "<tr><td><cite><font size=+1>\n";

    foreach $store (@store) {
	print "$store<br>\n";
    }

    print "</cite></font></td></tr></table>\n";
    print "<SCRIPT=\"Javascript\">\n";
    print "<form>\n";
    print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
    print "</form>\n";
    print "</body>\n</html>\n";

}

sub display_error {
 
	       print "Content-type:  text/html\n\n";
	       print "<html>\n<head>\n";
	       print "<title>AlephRx Web Report</title>\n";
	       print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
	       print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
	       print "</head>\n<body>\n";
	       print "<center>\n";
	       print "<h1>AlephRx Web Report</h1>\n";
	       print "<h3>You must complete the form</h3>\n";
	       print "<table>\n";
	       print "<tr><td align=\"left\">\n";
	       print "<UL>\n" , $error_message, "</UL>\n";
	       print "</td></tr></table>\n";
	       print "<SCRIPT=\"Javascript\">\n";
	       print "<form>\n";
	       print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
	       print "</form>\n";
  	       print "</body>\n</html>\n";
	   }
	 






sub email_display {


    print "<TABLE border=\"0\" width=\"30%\">\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "<tr><td colspan=\"2\"><hr></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email1\" VALUE=\"email1\" checked>Community:&nbsp;&nbsp;<cite><b>$recipient</b></cite></td></tr>\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email2\" VALUE=\"email2\" checked>Reported by:&nbsp;&nbsp;<b><cite>$email</b></cite></td></tr>\n";
#    print "<td width=\"20\">&nbsp;</td></tr>\n";


    print "<tr><td><INPUT TYPE=\"checkbox\" NAME=\"email3\" VALUE=\"yes\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email3a\"  cols=80 maxlength=80></td></tr>\n";
#    print "<td width=\"20\">&nbsp;</td>\n";
    print "<tr><td width=\"120\"><INPUT TYPE=\"checkbox\" NAME=\"email4\" VALUE=\"yes\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email4a\"  cols=80 maxlength=80></td></tr>\n";

    print "<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Additional Community</td>\n";
    print "<td><select name=\"email5\" size=1>\n";
    print "<option>\n";
    print "<option>COIseracq\@itd.umd.edu\n";
    print "<option>COIcircresill\@itd.umd.edu\n";
    print "<option>COIcatdbmaint\@itd.umd.edu\n";
    print "<option>COIdesktech\@itd.umd.edu\n";
    print "<option>COIuserinter\@itd.umd.edu\n";
    print "<option>COIall\@itd.umd.edu\n";

#    print "<option>jamieb\@kitabu.umd.edu\n";
    print "</select></td>\n";
    print "</tr>\n";

    print "</TABLE><br>\n";

}


