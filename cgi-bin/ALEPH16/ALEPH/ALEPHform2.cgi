#!/usr/local/bin/perl 

############################################################################
## update 20080109 - JB, added "dlcooper@umd.edu" as bcc, see sub bcc_create
############################################################################
## update 20080121 - JB, added assigned filters
############################################################################
## update 20080125 - JB, added deferred status filter
##      2009/09/23 - Hans - remove dlcooper
##      2009/12/04 - Hans - remove HS, add DW
##                        - Add 'Not Closed' button
##      2010/09/07 - Hans - replace aleph@itd with usmaialeph@umd.edu
##      2012/02/13 - Hans - replace MK with MH
############################################################################


use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$value = "";
$count = 0;
$mailprog = $ENV{ALEPHRX_MAILER};
$from = "usmaialeph\@umd.edu (RxWeb)";
$id = "";
$sort = "id";
$numrec = "30"; #records per page



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

    #Escape the single quotes and backslashes
#  $value =~ s/\'/\\\'/g;
#  $value =~ s/\\/\\\\/g;

    #Copy the name and value into the hash
    $input{$name} = $value;
}

$yes = $input{'yes'};
$no = $input{'no'};
$delete = $input{'delete'};
$filter_value = $input{'filter_value'};
$text = $input{'text'};
$id = $input{'record_id'}; 
$grp = $input{'grp'};
$campus = $input{'campus'};
$phone = $input{'phone'};
$name = $input{'name'};
$date = $input{'date'};
$status = $input{'status'};
$summary = $input{'summary'};
$rname = $input{'rname'};
$mresponse = $input{'response'};
$suppress = $input{'suppress'};
$mail = $input{'mail'};
$email = $input{'email'};
$cataloger = $input{'cataloger'};
$semail = $input{'semail'};

$email1 = $input{'email1'};
$email2 = $input{'email2'};
$email3 = $input{'email3'};
$email4 = $input{'email4'};
$email3a = $input{'email3a'};
$email4a = $input{'email4a'};
$email5 = $input{'email5'};

$limit = $input{'limit'};
$NEXT = $input{'NEXT'};
$PREV = $input{'PREV'};
$LAST = $input{'LAST'};
$FIRST = $input{'FIRST'};
$p = $input{'page_increment'};
$sort_value = $input{'sort_value'};
$ASSN = $input{'ASSN'};
$ASSNDW = $input{'ASSNDW'};
$ASSNHH = $input{'ASSNHH'};
$ASSNHB = $input{'ASSNHB'};
$ASSNYQ = $input{'ASSNYQ'};
$ASSNUS = $input{'ASSNUS'};
$ASSNMH = $input{'ASSNMH'};
$ASSNLS = $input{'ASSNLS'};
$CHANGE = $input{'CHANGE'};
$URGENT = $input{'URGENT'};
$CIRC = $input{'CIRC'};
$SRQ = $input{'SRQ'};
$ACQ = $input{'ACQ'};
$ITM = $input{'ITM'};
$RES = $input{'RES'};
$ILL = $input{'ILL'};
$CAT = $input{'CAT'};
$PAC = $input{'PAC'};
$DEFR = $input{'DEFR'};
$REPORT = $input{'REPORT'};
$NOTCLOSED = $input{'NOTCLOSED'};
$PRE = $input{'PRESTP'};
$NEW = $input{'NEW'};
$PURPLE = $input{'PURPLE'};
$PEND = $input{'PENDING'};
$TECH = $input{'TECH'};
$RECORD = $input{'record'};
$hidden_filter = $input{'hidden_filter'};
$hidden_value = $input{'hidden_value'};
$option_value = $input{'option_value'};
$NAME = $input{'NAME'};
$DATE = $input{'DATE'};
$ID = $input{'ID'};
$CAMPUS = $input{'CAMPUS'};
$STATUS = $input{'STATUS'};
$SUMMARY = $input{'SUMMARY'};
$FUNC = $input{'FUNC'};
$id_i = $input{'id_i'};
$id_t = $input{'id_t'};
$val = $input{'val'};

$page_number = $input{'page_number'};


$submit = $input{'submit'};
$drecord = $input{'drecord'};


#escape the single quotes
$summary =~ s/\'/\\\'/g;
$name =~ s/\'/\\\'/g;
$text =~ s/\'/\\\'/g;
$cataloger =~ s/\'/\\\'/g;
$email =~ s/\'/\\\'/g;
$phone =~ s/\'/\\\'/g;
$rname =~ s/\'/\\\'/g;
$mresponse =~ s/\'/\\\'/g;

#$email1 =~ s/\'/\\\'/g;
#$email2 =~ s/\'/\\\'/g;
#$email3 =~ s/\'/\\\'/g;
#$email4 =~ s/\'/\\\'/g;
#$email3a =~ s/\'/\\\'/g;
#$email4a =~ s/\'/\\\'/g;
#$email5 =~ s/\'/\\\'/g;




$value = $ENV{'QUERY_STRING'};
#$sort = $value;

#does not allow the insert of response when there is a name but no text
# sets the name to blank which prevents the insert.

if ($mresponse eq "") {
    $rname = "";
}



######################################
#maintains the sort value when paging
######################################

if ($NEXT) {
    $sort = $val;
}
if ($PREV) {
    $sort = $val;
}
if ($LAST) {
    $sort = $val;
}
if ($FIRST) {
    $sort = $val;
}

#####################################################
#validates the form of the additional email addresses
#####################################################

if ($email3) { &Check_Email($email3a);}
if ($email4) { &Check_Email($email4a);}




####################################################################
#  Replaces escaped single quotes with single quotes in filter only.
$filter_value =~ s/\\'/\'/g;
####################################################################

if ($no) {

    $message = "Delete aborted for record #$id<BR><BR>";

}

if ($yes) {

    $message = "Record #$id has been deleted<BR><BR>";

    &delete;

}




if ($submit){
    &match;
    if ($match_rows eq '0'){
        &updated;
        $updated_value = $updated;
    } else {
        $updated_value = "";
        $rname = "";
    }
}


if ($submit) {
    &insert;
    &sort_value;
}


if ($delete) {

    &pre_delete;

}else{ 


    if ($filter eq "") {
        $filter = $filter_value;
    }


    if ($email_check > 0) {
        &bad_email_display;
    } else {


        &recipient;
        &email_options;

        &sort_submit;
        &val;
        &update_val;
        &sort_increment;
        &sort_rules;

        &filter;
        &record;
        &get_row_count;
        &calc_num_pages;

        &filter_display;
        &sort_display;
#&page_number;
        &print_page_start_a;
        print "$updated_value\n";
        &next_paging;
        &prev_paging;
        &first_paging;
        &last_paging;
        &page_rules;
        &first_last;
        &get_sum_record;
        &print_fetch;
        &print_page_end_a;



        if ($email_count > 0) {
            $mail = "yes";
        }

        if ($match_rows ge '1'){

            $updated = "<span style=\"background-color : white\"><P><FONT COLOR=\"#FF0000\"> Record $id not updated!</span></FONT></P>"

        }else{
            if ($mail eq "yes"){
                &response_date;
                &mail;



            }
        }
    }
}



sub print_fetch {
    print "<br>\n";
    print "<TABLE WIDTH =\"70%\" BORDER=0 CELLPADDING=2 CELLSPACING=2>\n";
    print "<TR><TD></TD>\n";
    print "<TD></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"  ID  \" NAME=\"ID\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"                         Summary                         \" NAME=\"SUMMARY\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"Functional Area\" NAME=\"FUNC\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"         Name         \" NAME=\"NAME\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"Campus\" NAME=\"CAMPUS\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"     Status     \" NAME=\"STATUS\"></TD>\n";
    print "<TD><FONT SIZE=-1><B><INPUT TYPE=\"submit\" VALUE=\"  Date  \" NAME=\"DATE\"></TD>\n";

    print "<TD><FONT SIZE=-3>Replies</TD></TR>\n";
    print "</FORM>\n";
    while (@row = $sth->fetchrow_array) {
        $row_id = $row[0];
        $reply_count = "";
        $response_count = " ";
        &time_calc;
        &reply_query;
        $rcount = 0;
        &cell_background;
        print "<TR><TD><FONT SIZE=+1 COLOR=\"#FF0000\">$response_count</FONT>\n</TD>";
        print "<FORM ACTION=\"ALEPHurecord.cgi\" METHOD=\"post\">\n";
        print "<TD><FONT SIZE=-1><INPUT TYPE=\"image\" SRC=\"/IMG\/up.gif\" VALUE=\"Update\"></TD>\n";
        print "<INPUT TYPE=\"hidden\" name=\"record\" VALUE=\"$row[0]\">\n";
        print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
        print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
        print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
        print "<INPUT TYPE=\"hidden\" name=\"id_i\" VALUE=\"$id_i\">\n";
        print "<INPUT TYPE=\"hidden\" name=\"id_t\" VALUE=\"$id_i\">\n";
        print "<INPUT TYPE=\"hidden\" name=\"numrec\" VALUE=\"$numrec\">\n";
        print "</FORM>\n";
        print "<TD BGCOLOR=\"#FFFF99\"><FONT SIZE=-1>#&nbsp;<a href=\"\/cgi-bin\/ALEPH16\/ALEPHsum_full.cgi?$row[0]\">$row[0]</TD>\n";
        print "<TD BGCOLOR=\"$cellbk\"><FONT SIZE=-1>&nbsp;$row[3]</TD>\n";
        print "<TD BGCOLOR=\"#FFFF99\"><FONT SIZE=-1>&nbsp;$row[1]</TD>\n";
        print "<TD BGCOLOR=\"#F0F8FF\"><FONT SIZE=-1>&nbsp;$row[6]</TD>\n";
        print "<TD BGCOLOR=\"#FFFF99\"><FONT SIZE=-1>&nbsp;$row[2]</TD>\n";
        print "<TD BGCOLOR=\"#F0F8FF\"><FONT SIZE=-1>&nbsp;$row[4]</TD>\n";
        print "<TD BGCOLOR=\"#FFFF99\"><FONT SIZE=-1>&nbsp;$row[5]</TD>\n";
        print "<TD BGCOLOR=\"#F0F8FF\" ALIGN=\"CENTER\"><FONT SIZE=-1>$reply_count</TD></TR>\n";

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


#counts and creates flag to display when there is a reply


sub count_reply {


    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_7 =   "SELECT id from reply where parent_id = '$row_id' and itd = 'no' ";
    $sth_7 = $dbh->prepare($statement_7)
        or die "Couldn't prepare the query: $sth_7->errstr";

    $rv_7 = $sth_7->execute
        or die "Couldn't execute the query: $dbh->errstr";


    while (@row = $sth_7->fetchrow_array) {
        $count++;
        $reply_count = $count;
    }

    $rc_7 = $sth_7->finish;
    $rc_7 = $dbh->disconnect;
}


#creates flag to display when there is a response

sub count_response {


    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_8 =   "SELECT id from reply where parent_id = '$row_id' and itd = 'yes'";
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
    $statement_10 =   "SELECT COUNT(*) from report, people where report.supress = 'no' and report.id = people.id $filter";
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

#########################################################################
#calculates the total number pages that will be used for all the database
#########################################################################
sub calc_num_pages {

    $num_pages_1 = $row_count / $numrec;
    $num_pages_2 = sprintf("%d\n", $num_pages_1);
    if ($num_pages_1 > $num_pages_2){
        $num_pages = $num_pages_2 + 1;
    }else{
        $num_pages = $num_pages_2;
    } 
}

############################################################################################
#increments the page variable, prints the hidden increment value to pass on to the next page
############################################################################################
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
    print "<table WIDTH=\"70%\" border=0><tr>\n";

    if ($p < 1){
    }else{
        print "<TD ALIGN=\"LEFT\"><INPUT TYPE=\"submit\" VALUE=\"<< First Page\" NAME=\"FIRST\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";
        print "<INPUT TYPE=\"submit\"  VALUE=\"< Previous Page\" NAME=\"PREV\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";

    }
    if ($p > $num_pages-2) {
    }else{
        if ($value =~ /\d/){
            end;
        }elsif($LAST) {
        }else{

            print "<TD ALIGN=\"RIGHT\"><INPUT TYPE=\"submit\" VALUE=\"Next Page >\" NAME=\"NEXT\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";
            print "<INPUT TYPE=\"submit\" VALUE=\"Last Page >>\" NAME=\"LAST\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:beige ; color:#000; width:10em\">\n";
        }
    }
    $limit = $p * $numrec; 
    print "<BR>\n";
    print "</td></tr></table>\n";
}



sub first_last {

    if ($LAST) {
        $limit = ($num_pages - 1) * $numrec;
    }
    if ($FIRST) {
        $limit = 0;
    }
}


##########################
#sets the filter varible 
##########################

sub filter {

    if ($CIRC) {
        $filter = "and people.grp = 'Circulation'";
    }

    if ($PAC) {
        $filter = "and people.grp = 'Web OPAC'";
    }

    if ($SRQ) {
        $filter = "and people.grp = 'Serials'";
    }

    if ($ACQ) {
        $filter = "and people.grp = 'Acquisitions'";
    }

    if ($CAT) {
        $filter = "and people.grp = 'Cataloging'";
    }

    if ($TECH) {
        $filter = "and people.grp = 'Technical'";
    }

    if ($ITM) {
        $filter = "and people.grp = 'Item Maintenance'";
    }

    if ($RES) {
        $filter = "and people.grp = 'Reserves'";
    }

    if ($ILL) {
        $filter = "and people.grp = 'ILL'";
    }


    if ($DEFR) {
        $filter = "and report.status = 'deferred'";
    }

    if ($PEND) {
        $filter = "and report.status = 'pending'";
    }

    if ($NEW) {
        $filter = "and report.status = 'new'";
    }

    if ($ASSN) {
        $filter = "and report.status like 'assigned%'";
    }

    if ($ASSNHH) {
        $filter = "and report.status = 'assigned (HH)'";
    }

    if ($ASSNDW) {
        $filter = "and report.status = 'assigned (DW)'";
    }

    if ($ASSNHB) {
        $filter = "and report.status = 'assigned (HB)'";
    }

    if ($ASSNYQ) {
        $filter = "and report.status = 'assigned (YQ)'";
    }

    if ($ASSNUS) {
        $filter = "and report.status = 'assigned (US)'";
    }

    if ($ASSNMH) {
        $filter = "and report.status = 'assigned (MH)'";
    }

    if ($ASSNLS) { 
        $filter = "and report.status = 'assigned (LS)'";
    } 

    if ($CHANGE) {
        $filter = "and people.grp = 'Change request'";
    }

    if ($REPORT) {
        $filter = "and people.grp = 'Report request'";
    }

    if ($PURPLE) {
#    &reply_query;
        $filter = "and report.status = 'user input needed'";
    }

    if ($NOTCLOSED) {
        $filter = "and report.status != 'closed'";
    }

}


###########################################
#prints the page start and hidden variables 
###########################################
sub print_page_start {

    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD><BR>\n";
    print "<TITLE>RxWeb Reports Maintenance- TEST</TITLE>\n</HEAD>\n<BODY BACKGROUND=\"\/IMG\/bk2.gif\">\n";

    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";

    print "<FORM ACTION=\"ALEPHform2.cgi?id\" METHOD=\"post\">\n";
    print "<a NAME=\"top\"></a>\n";
    print "<center>\n";
    print "<H1>RxWeb Reports Staff</H1>\n";
#print "<P>Filter by:&nbsp;<INPUT TYPE=\"submit\" VALUE=\"CIRC\" NAME=\"CIRC\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"SRQ\" NAME=\"SRQ\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"PAC\" NAME=\"PAC\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"DLM\" NAME=\"DLM\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"PURPLE\" NAME=\"PURPLE\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"New\" NAME=\"NEW\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"Pending\" NAME=\"PENDING\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"Postponed\" NAME=\"POSTPONED\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"Closed\" NAME=\"CLOSED\">\n";
#print "<INPUT TYPE=\"button\" VALUE=\"All Summaries\" onClick=\"parent.location='ALEPHform2.cgi?id'\"></p>\n";
    print "<P><FONT SIZE=+1 COLOR=\"#FF0000\">&nbsp;&nbsp;*</FONT><FONT SIZE=-1>&nbsp;&nbsp;Indicates an ITD response has been made.&nbsp;</FONT>\n";
    print "<INPUT TYPE=\"button\" VALUE=\"RxWeb Form\" onClick=\"parent.location ='\/cgi-bin\/ALEPHform.cgi'\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"Report Statistics\" onClick=\"parent.location ='\/cgi-bin\/XALEPH\/ALEPHstats.cgi'\">\n";
#print "<INPUT TYPE=\"button\" VALUE=\"RxWeb\" onClick=\"parent.location='ALEPHsort.cgi?id'\">\n";
#print "<FONT SIZE=+1 COLOR=\"#0000FF\">&nbsp;&nbsp;*</FONT><FONT SIZE=-1>&nbsp;&nbsp;Indicates a User reply.</FONT></p>\n";
    print "</FORM>\n";
    print "<FORM ACTION=\"\/cgi-bin\/ALEPH\/ALEPHurecord.cgi\" METHOD=\"post\">\n";
    print "<B>Go to report # :</B>\n";
    print "<INPUT TYPE=\"text\" NAME=\"record\" SIZE=4>\n";
    print "<INPUT TYPE=\"submit\" VALUE=\"GO\">&nbsp;&nbsp;\n";
    print "<INPUT TYPE=\"button\" VALUE=\"Search\" onClick=\"parent.location='ALEPHsearch.cgi'\"></p>\n";
    print "</FORM>\n";
    print "<FORM ACTION=\"ALEPHform2.cgi?id\" METHOD=\"post\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"numrec\" VALUE=\"$numrec\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
    print "<FONT COLOR=\"#FF0000\">$message</FONT>\n";
}




sub record {

    if ($RECORD){
        if ($RECORD eq ""){
            $RECORD = "id";
        }
    }

    if ($RECORD) {
        if ($RECORD =~ /\D/) {
            $value = "id";
        }else{
            $value = $RECORD;

        }
    }
}


sub get_sum_record {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement =   "SELECT people.id, people.grp, people.campus, report.summary, report.status, DATE_FORMAT(report.date,'%m/%d/%y'), people.name, report.updated FROM people, report WHERE report.supress = 'no' and people.id = report.id $filter ORDER BY $sort $option LIMIT $limit, $numrec";



    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";



    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";

}


########################################
#inserts the data when updating a record
########################################

sub insert {

    if ($grp) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $grp = $dbh->quote($grp);
        $statement =   "UPDATE people SET people.grp = '$grp' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($status) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $status = $dbh->quote($status);
        $statement =   "UPDATE report SET report.status = '$status' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";



        $statement =   "UPDATE report set updated = NOW() where id = '$id'";

        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";




    }

    if ($text) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $text = $dbh->quote("$text");

#	$text =~ s/\'/\\\'/g;
#	$text =~ s/\\/\\\\/g;


        $statement =   "UPDATE report SET report.text = '$text' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($summary) {


        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $summary = $dbh->quote("$summary");

#	$summary =~ s/\'/\\\'/g;
#	$summary =~ s/\\/\\\\/g;


        $statement =   "UPDATE report SET report.summary = '$summary' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($campus) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $campus = $dbh->quote($campus);
        $statement =   "UPDATE people SET people.campus = '$campus' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($date) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $date = $dbh->quote("$date");
        $statement =   "UPDATE report SET report.date = '$date' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($name) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $name = $dbh->quote("$name");


        $statement =   "UPDATE people SET people.name = '$name' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($phone) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $phone = $dbh->quote("$phone");
        $statement =   "UPDATE people SET people.phone = '$phone' WHERE id = $id";
        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($rname) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $rname = $dbh->quote("$rname");
        $statement =   "INSERT into reply (parent_id, name, date, text, itd) VALUES ($id,'$rname',NOW(),'$mresponse','yes')";

        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";


        $statement =   "UPDATE report set updated = NOW() where id = $id";

        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";



    }


    if ($suppress) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#	$suppress = $dbh->quote($suppress);
        $statement =   "UPDATE report SET report.supress = '$suppress' where report.id = $id";

        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($email) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#         $email = $dbh->quote("$email");
        $statement =   "UPDATE people SET people.email = '$email' where people.id = $id";

        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }


    if ($cataloger) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
#        $cataloger = $dbh->quote($cataloger);
        $statement =   "UPDATE report SET report.cataloger = '$cataloger' where report.id = $id";

        $sth = $dbh->prepare($statement)
            or die "Couldn't prepare the query: $sth->errstr";
        $rv = $sth->execute
            or die "Couldn't execute the query: $dbh->errstr";

    }

}


sub response_date {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "SELECT date from reply where parent_id = $id and itd = 'yes' ";

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



sub updated {

    if ($rname eq "") {

        $updated = ""; 

    }else {

        $updated = "<span style=\"background-color : white\"><P><FONT COLOR=\"#FF0000\"> Record $id has been updated!</span></FONT></P>"
    }
}





sub sort_value {


    if ($NEXT) {
        $sort = $sort_value;
    }
    if ($PREV) {
        $sort = $sort_value;
    }
    if ($LAST) {
        $sort = $sort_value;
    }
    if ($FIRST) {
        $sort = $sort_value;
    }

    if ($sort_value eq ""){
        $sort_value = "id";
    }

    if ($value eq ""){
        $sort = $sort_value;
    }

}


#############################################################
# deletes the selected records from the database - not used
#############################################################
sub delete {

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

##################################################################################
#presents the selected record for deletion, offers the yes or no option.  If no is 
#selected user is taken back to summary screen 
##################################################################################
sub pre_delete  {


    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);


    $statement =   "SELECT people.id, people.grp, people.campus, people.phone, people.name, report.date, report.status, report.summary, report.text FROM people, report WHERE people.id = report.id AND people.id = $drecord";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";

    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";



    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD>\n<TITLE>RxWeb Record Maintenance</TITLE>\n</HEAD>\n<BODY BACKGROUND=\"\/IMG\/bk2.gif\">\n";
    print "<FORM ACTION=\"ALEPHform2.cgi\" METHOD=\"post\">\n";
    print "<INPUT TYPE=\"hidden\" NAME=\"record_id\" VALUE=\"$drecord\">\n";
    print "<center>\n";
    print "<P><h1>RxWeb Records Maintenance</P></h1>\n";
    print "<FONT COLOR=\"#FF0000\">You are about to delete the following record!</FONT>\n";
    print "<P><INPUT TYPE=\"submit\" VALUE=\"YES\" NAME=\"yes\">\n"; 
    print "&nbsp;&nbsp;<INPUT TYPE=\"submit\" VALUE=\"NO\" NAME=\"no\"</P>\n";
    print "<INPUT TYPE=\"hidden\" name=\"record\" VALUE=\"$row[0]\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter_value\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"numrec\" VALUE=\"$numrec\">\n";
    print "<BR>\n";
    print "<BR>\n";
    print "<TABLE BORDER=0 BGCOLOR=\"#FFFFCC\">\n";
    print "<TR>\n
    <TH>ID</TH>\n
    <TH ALIGN=LEFT>funct.area</TH>\n
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


}



sub sort_submit {


    if ($ID) {
        $sort = "report.id";
        $id_i++;
    }


    if ($SUMMARY) {
        $sort = "report.summary";
        $id_i++;
    }



    if ($NAME) {
        $sort = "people.name";
        $id_i++;
    }


    if ($DATE) {
        $sort = "report.date";
        $id_i++;
    }


    if ($CAMPUS) {
        $sort = "people.campus";
        $id_i++;
    }


    if ($STATUS) {
        $sort = "report.status";
        $id_i++;
    }


    if ($FUNC) {
        $sort = "people.grp";
        $id_i++;
    }

    if ($PRE) {
        $sort = "report.updated";
        $id_i++;
    }

}



sub sort_rules {

    if ($option eq "DESC") {
        $option_value = "Descending";
    }

    if ($option eq "") {

        $option_value = "Ascending";

    }

}


sub sort_increment {


    if ($id_i > 1) {
        $id_i = 0;
    }

    if ($id_i eq "1") {
        $option = "";
    }

    if ($id_i eq "0") {
        $option = "DESC";
    }

}




#sets the id_i variable to 0 each time a new sort key is selected

sub val  {
    if ($val ne $sort){
        $id_i = 0;
    }
}

#maintains the id_i variable when a record is update using urecord.cgi

sub update_val {

    if ($submit) {
        $id_i = $id_t;
    }
}





sub filter_display  {

    if ($filter eq "and people.grp = 'Circulation'") {
        $filter_display = "Circulation";
    }

    if ($filter eq "and people.grp = 'Acquisitions'") {
        $filter_display = "Acquisitions";
    }

    if ($filter eq "and people.grp = 'Technical'") {
        $filter_display = "Technical";
    }

    if ($filter eq "and people.grp = 'Web OPAC'") {
        $filter_display = "Web OPAC";
    }

    if ($filter eq "and people.grp = 'Reserves'") {
        $filter_display = "Reserves";
    }

    if ($filter eq "and people.grp = 'ILL'") {
        $filter_display = "ILL";
    }


    if ($filter eq "and people.grp = 'Serials'") {
        $filter_display = "Serials";
    }

    if ($filter eq "and people.grp = 'Item Maintenance'") {
        $filter_display = "Item Maintenance";
    }

    if ($filter eq "and people.grp = 'Cataloging'") {
        $filter_display = "Cataloging";
    }

    if ($filter eq "and people.grp = 'Item Maintenance'") {
        $filter_display = "Item Maintenance";
    }

    if ($filter eq "") {
        $filter_display = "All Summaries";
    }

    if ($filter eq "and report.status = 'new'") {
        $filter_display = "New";
    }

    if ($filter eq "and report.status = 'pending'") {
        $filter_display = "Pending";
    }

    if ($filter eq "and people.grp = 'Report request'") {
        $filter_display = "Report Request";
    }

    if ($filter eq "and report.status = 'postponed'") {
        $filter_display = "Postponded";
    }

    if ($filter eq "and report.status = 'deferred'") {
        $filter_display = "Deferred";
    }

    if ($filter eq "and people.grp  = 'Report request'") {
        $filter_display = "Report Request";
    }

    if ($filter eq "and people.grp = 'Change request'") {
        $filter_display = "Change Request";
    }
    if ($filter eq "and report.status != 'closed'") {
        $filter_display = "Not Closed";
    }

}


sub sort_display  {

    if ($sort eq "report.id") {
        $sort_display = "ID";
    }
    if ($sort eq "report.summary") {
        $sort_display = "Summary";
    }

    if ($sort eq "report.date") {
        $sort_display = "Date";
    }

    if ($sort eq "people.name") {
        $sort_display = "Name";
    }

    if ($sort eq "people.campus") {
        $sort_display = "Campus";
    }
    if ($sort eq "people.grp") {
        $sort_display = "Functional Area";
    }

    if ($sort eq "report.status") {
        $sort_display = "Status";
    }
    if ($sort eq "id") {
        $sort_display = "ID";
    }

    if ($sort eq "report.updated") {
        $sort_display = "Recent";
    }
}


sub page_number {

    if ($LAST) {
        $page_number = $num_pages;

    }elsif ($FIRST) {
        $page_number = 1;

    }elsif ($NEXT)  {
        $page_number++;

    }elsif ($PREV) {
        $page_number--; 

    }else {
        $page_number = 1;
    }
}





sub print_page_start_a {

    print "Content-type: text/html\n\n";
    print "<HTML>\n<HEAD>\n<TITLE>RxWeb Update</TITLE>\n</HEAD>\n<BODY BGCOLOR=\"#98AFC7\">\n";
    print "<FORM ACTION=\"ALEPHform2.cgi?id\" METHOD=\"post\">\n";
    print "<a NAME=\"top\"></a>\n";
    print "<center>\n";
    print "<FONT SIZE=\"-1\"><INPUT TYPE=\"button\" VALUE=\"RxWeb Form\" onClick=\"parent.location ='\/cgi-bin\/ALEPHform.cgi'\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</FONT>\n";
    print "<FONT SIZE=\"+3\"><STRONG>RxWeb Update</STRONG></FONT>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<FONT SIZE=\"-1\"><INPUT TYPE=\"button\" VALUE=\"RxWeb Statistics\" onClick=\"parent.location ='\/cgi-bin\/ALEPH16\/ALEPHstats.cgi'\"></FONT><br><br>\n";

    print "<FONT SIZE=\"-1\">Select one of the following to filter reports.</font>\n";

    print "<table border=\"0\" width=\"60%\" bgcolor=\"#98AFC7\">\n";
    print "<tr>\n";
    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Acquisitions\" NAME=\"ACQ\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Circulation\" NAME=\"CIRC\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Cataloging\" NAME=\"CAT\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Item Maintenance\" NAME=\"ITM\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Reserves\" NAME=\"RES\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"ILL\" NAME=\"ILL\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Serials\" NAME=\"SRQ\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";



    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Web OPAC\" NAME=\"PAC\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Technical\" NAME=\"TECH\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";



    print "<tr>\n";
    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"All Assigned\" NAME=\"ASSN\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Assigned (HB)\" NAME=\"ASSNHB\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Assigned (HH)\" NAME=\"ASSNHH\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Assigned (DW)\" NAME=\"ASSNDW\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Assigned (YQ)\" NAME=\"ASSNYQ\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Assigned (MH)\" NAME=\"ASSNMH\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Assigned (LS)\" NAME=\"ASSNLS\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n"; 

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Assigned (US)\" NAME=\"ASSNUS\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";






    print "<tr>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"New\" NAME=\"NEW\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Pending\" NAME=\"PENDING\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"PURPLE\" NAME=\"PURPLE\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";


    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Change Request\" NAME=\"CHANGE\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"RECENT\" NAME=\"PRESTP\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Deferred\" NAME=\"DEFR\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Report Request\" NAME=\"REPORT\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"All Summaries\" NAME=\"ALL\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<td width=\"100%\" align=\"center\"><INPUT TYPE=\"SUBMIT\" VALUE=\"Not Closed\" NAME=\"NOTCLOSED\" STYLE=\"font-family:sans-serif; font-size:xx-small; background:#ff0 none; color:#000; width:10em\"></td>\n";

    print "<tr><td colspan=\"2\"><font size=\"-1\">&nbsp;&nbsp;FILTER = <b>$filter_display</b></font></td><td cellpadding=\"2\" colspan=\"2\"><font size=\"-1\">&nbsp;&nbsp;SORT = <b>$sort_display</b></font></td><td cellpadding=\"2\" colspan=\"2\"><font size=\"-1\">&nbsp;&nbsp;ORDER = <b>$option_value</b></font></td><td cellpadding=\"2\" colspan=\"2\"><font size=\"-1\">&nbsp;&nbsp;Records per page = <b>$numrec</b></font></td>\n";

    print "</table>\n";
    print "</FORM>\n";
    print "<FORM ACTION=\"ALEPHurecord.cgi\" METHOD=\"post\">\n";
    print "<FONT SIZE=+1 COLOR=\"#FF0000\">&nbsp;&nbsp;*</FONT><FONT SIZE=-1>&nbsp;&nbsp;Indicates an ITD response has been made.&nbsp;</FONT>\n";
    print "<B>Go to report # :</B>\n";
    print "<INPUT TYPE=\"text\" NAME=\"record\" SIZE=3>\n";
    print "<INPUT TYPE=\"submit\" VALUE=\"GO\">\n";
    print "&nbsp;&nbsp;&nbsp;&nbsp;<FONT SIZE=\"-1\"><INPUT TYPE=\"button\" VALUE=\"Basic Search\" onClick=\"parent.location ='\/cgi-bin\/ALEPH16\/ALEPH\/ALEPHsearch.cgi'\"></FONT><br><br>\n";
    print "</FORM>\n";

    print "<FORM ACTION=\"ALEPHform2.cgi?id\" METHOD=\"post\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"hidden_filter\" VALUE=\"$filter\">\n";

    print "<INPUT TYPE=\"hidden\" name=\"option_value\" VALUE=\"$option_value\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"id_i\" VALUE=\"$id_i\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_number\" VALUE=\"$page_number\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"val\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"numrec\" VALUE=\"$numrec\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
}

sub print_page_end_a {

    print "</TABLE>\n";
#print "$final_email_list\n<br>";
    $rc = $sth->finish;
    $rc = $dbh->disconnect;
    print "<BR>\n";
    print "<FORM ACTION=\"ALEPHform2.cgi?id\" METHOD=\"post\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"record\" VALUE=\"$row[0]\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"val\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"numrec\" VALUE=\"$numrec\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"id_i\" VALUE=\"$id_i\">\n";
    &page_rules;
    print "</FORM>\n";
#print ">>$final_email_list\n";
    print "<CENTER><a href=\"#top\"><FONT SIZE=-1>TOP</a>\n";
    print "<BR><BR>\n";
    print "</BODY>\n</HTML>\n";

} 


#############################################################
# if incoming record matches existing record, insert is denied
# 2007/07/22 currently only matching in summary
#############################################################

sub match {


    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

#     $summary =~ s/\'/\\\'/g;
#    $summary = $dbh->quote("$summary");
#    $phone = $dbh->quote("$phone");
#    $name = $dbh->quote("$name");
#    $mresponse = $dbh->quote("$mresponse");
#    $rname = $dbh->quote("$rname");

    $statement = "select report.summary, people.phone, people.name, reply.text, reply.name from report, people, reply WHERE people.id = report.id and report.id = reply.parent_id and report.summary = '$summary' and reply.name = '$rname' and reply.text = '$mresponse'";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";

    $match_rows = $sth->rows;

}




sub Check_Email

{
    if ($_[0] =~ /(@.*@)|(,)|\s+|(\.\.)|(@\.)|(\.@)|(^\.)|(\.$)|(^\d+)|(\d+$)/ || ($_[0] !~ /^.+\@localhost$/ && $_[0] !~ /^.+\@\[?(\w|[-.])+\.[a-zA-Z]{2,3}|[0-9]{1,3}\]?$/))         { $email_check++; push @store, $_[0]; }
    else { }
}


sub email_options {


    if ($email1) {
        $email_count++;
        $recipient =~ s/\s+//g;
#       $recipient =~ s/,//g;
        $rec1 = "$recipient";
        $emailx = 'yes';
    }

    if ($email2) {
        $email_count++;
        $email =~ s/\s+//g;
#       $email =~ s/,//g;
        $rec2 = ",$email";
        $emailx = 'yes';
    }

    if ($email3) {
        $email_count++;
        $email3a =~ s/\s+//g;
#       $email3a =~ s/,//g;
        $rec3 = ",$email3a";
        $emailx = 'yes';
    }

    if ($email4) {
        $email_count++;
        $email4a =~ s/\s+//g;
#       $email4a =~ s/,//g;
        $rec4 = ",$email4a";
        $emailx = 'yes';
    }

    if ($email5) {
        $email_count++;
        $rec5 = ",$email5";
        $emailx = 'yes';
    }

    if ($rname eq "") { 
        $emailx = "no"; 
    }

    if ($mresponse eq "") { 
        $emailx = "no"; 
    }



    $final_email_list = $rec1 . $rec2 . $rec3 . $rec4 . $rec5;
}



sub bad_email_display {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Reply</title>\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<h1>RxWeb Reply</h1>\n";
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







sub mail {

    #removes the escape from single quote
    $text =~ s/\\'/\'/g;
    $name =~ s/\\'/\'/g;
    $stext =~ s/\\'/\'/g;
    $sname =~ s/\\'/\'/g;
    $summary =~ s/\\'/\'/g;
    #$final_email_list =~ s/\\'/\'/g;

    &bcc_create;

    if ($emailx eq "yes") {
        open (MAIL,"|$mailprog -t");
        print MAIL "To: $final_email_list\n";
        print MAIL "Bcc: $bcc\n" if $bcc;
        print MAIL <<END;
From: $from
Subject: RESPONSE:$slug#$id:$summary

--------------------------------------------------------------------------------
Please do not reply directly to this e-mail. 
To REPLY to this Rx: http://www.itd.umd.edu/cgi-bin/ALEPH16/ALEPHreply.cgi?$id
(If prompted, sign in with the standard USMAI username/password.)
--------------------------------------------------------------------------------

This is a DSS response to the RxWeb listed below

 Original Report # : $id
  Date of Report # : $date
   Functional Group: $grp
             Status: $status

END

        $dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text, itd from reply where parent_id = '$id' ORDER BY date DESC";
        $sth_1 = $dbh_1->prepare($statement_1)
            or die "Couldn't prepare the query: $sth_1->errstr";

        $rv_1 = $sth_1->execute
            or die "Couldn't execute the query: $dbh_1->errstr";

        while (@row = $sth_1->fetchrow_array) {
            $itd = $row[3];
            &reply_type;
            print MAIL <<END;
  $reply_type submitted by: $row[0]
              Date/Time: $row[1]
               $reply_type: $row[2]

-----------------------------------------------
END
        }


        $rc_1 = $sth_1->finish;
        $rc_1 = $dbh_1->disconnect;

        &text;
        print MAIL <<END;

Original Report by: $original_name
   Original Report: $original_text

-----------------------------------------------

===================================================================================
View this Rx online: http://www.itd.umd.edu/cgi-bin/ALEPH16/ALEPHsum_full.cgi?$id
END
        close (MAIL);
#	 $row_id = "";
    } else {}
}



sub reply_type {

    if ($itd eq "yes") {
        $reply_type = "Response";
        $font_color = "#FF0000";
    } else {
        $reply_type = "   Reply";
        $font_color = "#0000FF";
    }
}


##############################################
#gets the text and name of the original report
##############################################

sub text {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

    $statement = "select report.text, people.name from report, people WHERE report.id = '$id' and people.id = report.id";

    $sth = $dbh->prepare($statement)
        or die "Couldn't prepare the query: $sth->errstr";
    $rv = $sth->execute
        or die "Couldn't execute the query: $dbh->errstr";


    while (@row = $sth->fetchrow_array) {

        $original_text = $row[0];
        $original_name = $row[1];
    }

}


## sets the email recipient
sub recipient {

    if ($grp eq "Circulation") {
        $recipient = "usmaicoicircresill\@umd.edu";
        $slug = "CIRC:";
    }
    if ($grp eq "Technical") {
        $recipient = "usmaicoidesktech\@umd.edu";
        $slug = "TECH:";
    }
    if ($grp eq "Web OPAC") {
        $recipient = "usmaicoiuserinter\@umd.edu";
        $slug = "OPAC:";
    }

    if ($grp eq "Cataloging") {
        $recipient = "usmaicoicatdbmaint\@umd.edu";
        $slug = "CAT:";
    }

    if ($grp eq "Serials") {
        $recipient = "usmaicoiseracq\@umd.edu";
        $slug = "SER:";
    }

    if ($grp eq "Acquisitions") {
        $recipient = "usmaicoiseracq\@umd.edu";
        $slug = "ACQ:";
    }

    if ($grp eq "Item Maintenance") {
        $recipient = "usmaicoicircresill\@umd.edu,usmaicoicatdbmaint\@umd.edu,usmaicoiseracq\@umd.edu";
        $slug = "ITM:";
    }

    if ($grp eq "Reserves") {
        $recipient = "usmaicoicircresill\@umd.edu,usmaicoiuserinter\@umd.edu";
        $slug = "RES:";
    }

    if ($grp eq "ILL") {
        $recipient = "ilug\@umd.edu,usmaicoicircresill\@umd.edu";
        $slug = "ILL:";
    }

    if ($grp eq "other") {
        $recipient = "usmaialeph\@umd.edu";
        $slug = "OTHR:";
    }

    if ($grp eq "Report request") {
        $recipient = "usmaialeph\@umd.edu";
        $slug = "RQST:";
    }

    if ($grp eq "Change request") {
        $recipient = "usmaialeph\@umd.edu";
        $slug = "CHNG:";
    }

    if ($grp eq "AV18") {
        $recipient = "usmaialeph\@umd.edu";
        $slug = "AV18:";
    }





}

sub no_name_text_display {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Reply</title>\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<h1>RxWeb Reply</h1>\n";
    print "Error Messages will go in here\n";
    print "<SCRIPT=\"Javascript\">\n";
    print "<form>\n";
    print "<p><input TYPE=\"button\" VALUE=\" Back \" onClick=\"history.go(-1)\"></p>\n";
    print "</form>\n";
    print "</body>\n</html>\n";

}

##############################################
## sets the background color of the summary  
## cell based on the status of the report.
## This is the purple functionality.
##############################################

sub cell_background  {

    if ($row[4] eq "user input needed" and $maxstamp gt $date) {
        $cellbk = "#FF00FF" }

    elsif ($row[4] eq "pending" and $itd = "") {
        $cellbk = "#00FFFFF" }

    else {
        $cellbk = "#F0F8FF";
    }



}



############################################################
# queries the reply to collect information for display
############################################################ 


sub reply_query {



    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_8 =   "SELECT DATE_FORMAT(date,'%Y%m%d'), itd, NOW(), DATE_SUB(NOW(),INTERVAL 14 DAY), DATE_SUB(NOW(), INTERVAL 7 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY), date from reply where parent_id = '$row_id'";




    $sth_8 = $dbh->prepare($statement_8)
        or die "Couldn't prepare the query: $sth_8->errstr";

    $rv_8 = $sth_8->execute
        or die "Couldn't execute the query: $dbh->errstr";


    while (@rrow = $sth_8->fetchrow_array) {


        $now = $rrow[2];
        $twoweeksago = $rrow[3];
        $oneweekago = $rrow[4];
        $onedayago = $rrow[5];

        if ($rrow[1] eq "no") {
            $itd = "no";
            $rcount++;
            $reply_count = $rcount;
            $maxstamp = $rrow[0];
            $maxstampunix = $rrow[6];
        } else {
#$reply_count = "";
            $response_count = "*";
            $maxstamp = "";
            $maxstampunix = 0;
        }



    }

    $rc_8 = $sth_8->finish;
    $rc_8 = $dbh->disconnect;

}


sub time_calc {

    ($sec,$min,$hour,$day,$month,$year) = (localtime)[0,1,2,3,4,5]; # Get Date

    $today = sprintf("%04d%02d%02d", ($year + 1900),$month,$day);
    $onemonthago = $today -30;


}



############################################################
## constructs the bcc option for sendmail
## if aleph is part of the final email list
## then bcc will be empty, other bcc = aleph@itd.umd.edu
############################################################

sub bcc_create {

    if ($final_email_list =~ /usmaialeph\@umd.edu/i) {
        $bcc = "";
    }else{
        $bcc = "usmaialeph\@umd.edu";
    }
}
