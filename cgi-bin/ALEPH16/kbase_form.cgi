#!/usr/local/bin/perl

## Jamie Bush, 2007
## RxWeb KB (AlephRx) version 3.1
## KB web form

use CGI;
use DBI;
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
$id = "";
$query = new CGI;
$added = "";

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

    $subject = $query->param('subject');
    $id = $query->param('id');
    $summary = $query->param('summary');
    $create_date = $query->param('date');
    $text = $query->param('text');
    $ref = $query->param('ref');
    $service = $query->param('service');



if ($query->param('submitted')) {

    $error_message = "";
    &match;
    &validate_form;


    if ($error_message ne "") {
	&display_error;

    } elsif ($error_message eq "") {
	&insert_data;
         &print_form;
    } 
    } else {
           &set_initial_values;
           &print_form;

       }

&print_page_end;


##########################################
# validates the data submitted on the form
##########################################

sub validate_form {

   if ($match_rows gt '0') {

	    $error_message .= "<LI>This is a duplicate record. Clear the form and enter a new record. \n";
   }

   if ($subject eq "") {
	  $error_message .= "<LI>Please enter a subject.\n";
   }

   if ($service eq "") {
	  $error_message .= "<LI>Please select a service.\n";
   }

   if ($summary eq "") {
	  $error_message .= "<LI>Please enter a summary.\n";
   }

   if ($text eq "") {
       $error_message .= "<LI>Please enter the text for your report.\n";
   }

  if ($create_date =~ /(19|20)\d\d([-  \/.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])/) { 
  }else{
      $error_message .= "<LI>Please enter a valid date.\n";
   }


   
}						       						      
   

sub set_initial_values {

    $id = "";
    $subject = "";
    $service = "";
    $summary = "";
    $text = "";
    $create_date = "";
    $ref = "";
}

#######################################################
## prints the form if no "sumitted" variable is present
#######################################################

sub print_form {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Knowledge Base Form</title>\n";
    print "</head>\n<body bgcolor=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>RxWeb Knowledge Base Form</h1>\n";
    print "<FORM ACTION=\"kbase_form.cgi\" METHOD=\"post\">\n";
    print "<center>\n";
#    print "<INPUT TYPE=\"button\" VALUE=\"RxWeb\" onClick=\"parent.location='\/cgi-bin\/ALEPH16\/ALEPHsum.cgi?id'\"></P>\n";
    print "<table width=\"640\" border=\"0\"><tr><td>\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
#    print "<table border=0>\n";

    print "<tr valign=\"top\">\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\"><FONT SIZE=-1>Service:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\"> <select name=service size=1>\n";
    print "<option>\n";
    print "<option>Aleph\n";
    print "<option>ILLiad\n";
    print "<option>ITD\n";  
    print "<option>USMAI\n"; 
    print "<option>CPC\n";
    print "<option>RSTG\n";
    print "<option>UITG\n";
    print "<option>ASTG\n";    
    print "</select></td>\n";
    print "</tr>\n";
    print "<tr valign=\"top\">\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\"><FONT SIZE=-1>Date of creation:&nbsp;</td>\n"; 
    print "<td bgcolor=\"#CCCCCC\"><input type=text name=date size=8>&nbsp;&nbsp&nbsp;format:&nbsp;YYYY-MM-DD</FONT></td>\n";
    print "</tr>\n";
    print "<tr valign=\"top\">\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\"><FONT SIZE=-1>Subject:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\"> <input type=text name=subject size=20 maxlength=50></td>\n";
    print "</tr>\n";

    print "<tr valign=\"top\" colspan=4>\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\" ><FONT SIZE=-1>Summary:</FONT>&nbsp;</td>\n"; 
    print "<td bgcolor=\"#CCCCCC\"> <input type=text name=summary size=40 maxlength=50></td>\n";
    print "</tr>\n";

    print "<tr valign=\"top\">\n";


    print "<th bgcolor=\"#FFFF00\" align=\"right\" ><FONT SIZE=-1>Reference:</FONT>&nbsp;</td>\n"; 
    print "<td bgcolor=\"#CCCCCC\"> <input type=text name=ref size=20></td>\n";

    print "<br>\n";
    print "</tr>\n";
    print "<tr valign=\"top\">\n";
    print "</P>\n";
    print "</td>\n";
    print "</tr>\n";
    print "<tr>\n";
    print "<td colspan=4>\n";
    print "<center>\n";
    print "<B>Knowledge Base Information:</B>\n";
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
    print "$added\n";
}


sub print_page_start {
    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Form</title>\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<h1>RxWeb Form</h1>\n";

}

sub print_page_end {
    print "</body>\n";
    print "<HEAD>\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</HEAD></HTML>\n";
}





######################################
## inserts the form data into database
######################################

sub insert_data {


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);



$statement =   "SELECT last_insert_id()";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";

$rc = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

#$last = $sth->fetchrow_array; 

while (@row = $sth->fetchrow_array) {
    $id = $row[0];
}


$added = "<span style=\"background-color : white\"><P><FONT COLOR=\"#FF0000\"> Record $id has been added!<\/span><\/FONT><\/P>";


$text = $dbh->quote("$text");
$create_date = $dbh->quote("$create_date");
$service = $dbh->quote("$service");
$subject = $dbh->quote("$subject");
$summary = $dbh->quote("$summary");
$ref = $dbh->quote("$ref");


$statement =   "INSERT INTO kbase (id, service, subject, create_date, add_date,summary,text,ref) VALUES 
               (LAST_INSERT_ID(),$service,$subject,$create_date,NOW(),$summary,$text,$ref) ";

$query1 = $statement;



$sth = $dbh->prepare($statement)
	or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
	or die "Couldn't execute the query: $dbh->errstr";


$rc = $sth->finish;
$rc = $dbh->disconnect;


}




########################################################
## checks for matching/duplicate reports when submitting 
########################################################

sub match {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement = "select summary, subject, service, create_date from kbase  WHERE summary = '$summary' and subject = '$subject' and service = '$service' and create_date = '$create_date'";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    $match_rows = $sth->rows;



}




###########################################################
## displays error messaging when the form does not validate
###########################################################

sub display_error {
 
	       print "Content-type:  text/html\n\n";
	       print "<html>\n<head>\n";
	       print "<title>RxWeb Knowledge Base Form</title>\n";
	       print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
	       print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
	       print "</head>\n<body>\n";
	       print "<center>\n";
	       print "<h1>RxWeb Knowledge Base Form</h1>\n";
	       print "<h3>You have made a serious error in the form!</h3>\n";
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
	 



sub print_record {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Knowledge Base Record</title>\n";
    print "</head>\n<body bgcolor=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>RxWeb Knowledge Base Record</h1>\n";
    print "<center>\n";
#    print "<INPUT TYPE=\"button\" VALUE=\"RxWeb\" onClick=\"parent.location='\/cgi-bin\/ALEPH16\/ALEPHsum.cgi?id'\"></P>\n";


}


############################################
## selects full record for display  
############################################

sub get_full_record {

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "SELECT id, service, create_date, subject, summary,ref, text from kbase WHERE id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";



while (@row = $sth->fetchrow_array) {
        print "<TR><TD BGCOLOR=\"#FFFF00\" COLSPAN=7><B><i>Report #</i>&nbsp;$row[0]&nbsp;&nbsp;&nbsp;&nbsp;$row[0]</B></TD></FONT></TR>\n";

         print "<TR>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Record</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Name</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Phone</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Date</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Func. Area</I></TH>\n
         <TH BGCOLOR=\"#CCCCCC\"><FONT SIZE=-1><I>Campus</I></TH>\n

        print "<TR>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[0]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[1]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[2]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[3]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[4]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[5]</TD>\n";
        print "<TD BGCOLOR=\"#FFFFF0\" VALIGN=TOP>$row[6]</TD>\n";
        print "</TR>\n";
        print "</TR>\n";
        print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
    }
}



















