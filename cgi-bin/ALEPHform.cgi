#!/usr/bin/perl

=head1 NAME

ALEPHform.cgi - Report Submission Form

=cut

## Jamie Bush, 2004 
## RxWeb (AlephRx) version 3.1
## name changed 6/20/06
## updated 8/10/06 "change request" converted to functional area
## web form

## 2010/09/07  Hans  Change aleph@itd.umd.edu to usmaialeph@umd.edu

use FindBin qw{$Bin};
use lib "$Bin/../lib";

use CGI;
use DBI;
use CGI::Carp qw(fatalsToBrowser);
use IO::Handle;
use lib "/lims/lib/perl";
use URI::Escape;

use AlephRx::Util;

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$rname = "";
$response = "";
$mailprog = $ENV{ALEPHRX_MAILER};
$query = new CGI;

$name = $query->param('name');
$campus = $query->param('campus');
$status = $query->param('status');
$text = $query->param('text');
$escaped_text = uri_escape( $text );
$summary = $query->param('summary');
$escaped_summary = uri_escape( $summary );
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

# set the email recipient
&recipient;

if ($query->param('submitted')) {

    $error_message = "";
    &match;
    &validate_form;

    if ($error_message ne "") {
        &display_error;
    } elsif ($error_message eq "") {
        &recipient;
        &email_config;
    } 
} else {
    &set_initial_values;
    &print_form;
}

=head2 validate_form()

Validates the data submitted to the form. If there are any matching rows, as
determined by C<match()>, or any problems with the data, this function places an
HTML-formatted error message into C<$error_message>.

=cut
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

    if ($summary eq "") {
        $error_message .= "<LI>Please enter a summary.\n";
    }

    if ($text eq "") {
        $error_message .= "<LI>Please enter the text for your report.\n";
    }

    if ($email =~ /(@.*@)|(,)|\s+|(\.\.)|(@\.)|(\.@)|(^\.)|(\.$)/ || ($email !~ /^.+\@localhost$/ && $email !~ /^.+\@\[?(\w|[-.])+\.[a-zA-Z]{2,3}|[0-9]{1,3}\]?$/)) {
        $error_message .= "<LI>Please enter a valid email address.\n";
    }
}						       						      

=head2 set_initial_values()

Initializes variables that store the submitted values.

=cut
sub set_initial_values {
    $name = "";
    $campus = "";
    $status = "new";
    $text = "";
    $escaped_text = "";
    $summary = "";
    $escapes_summary = "";
    $date = "";
    $grp = "";
    $time = "";
    $hour = "";
    $phone = "";
    $email = "";
    $cataloger = "";
}

=head2 print_form()

Prints the report form for submitting a new request. This function prints both
the HTTP header and the HTML page. It is only called if there is no C<submitted>
request parameter.

=cut
sub print_form {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>Submit a Report to AlephRx</title>\n";
    print "</head>\n<body bgcolor=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>Submit a Report to AlephRx</h1>\n";
    print "<FORM ACTION=\"ALEPHform.cgi\" METHOD=\"post\">\n";
    print "<center>\n";
    print "<INPUT TYPE=\"button\" VALUE=\"View Reports\" onClick=\"parent.location='ALEPH16/ALEPHsum.cgi?id'\"></P>\n";
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
    print "<option>LNDL\n";
    print "<option>MS\n";
    print "<option>SMCM\n";
    print "<option>SU\n";
    print "<option>TU\n";
    print "<option>UB\n";
    print "<option>UBLL\n";
    print "<option>UMBC\n";
    print "<option>UMCP\n";
    print "<option>UMES\n";
    print "<option>UMGC\n";
    print "<option>UMLL\n";
    print "<option>DSS\n";
    print "</select></td>\n";
    print "</tr>\n";
    print "<tr valign=\"top\">\n";
    print "<th bgcolor=\"#FFFF00\" align=\"right\" ><FONT SIZE=-1>Functional Area:</FONT>&nbsp;</td>\n";
    print "<td bgcolor=\"#CCCCCC\"> <select name=\"grp\" size=1>\n";
    print "<option>\n";

    for my $functional_area (@AlephRx::Util::FUNCTIONAL_AREAS) {
        print "<option>" . $functional_area->{name} . "\n";
    }

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
    print "<option>new \n";
    print "</select>\n";
    print "</td>\n";
    print "</tr>\n";

    print "<tr valign=\"top\">\n";
    print "<br>\n";
    print "</tr>\n";
    print "<tr valign=\"top\">\n";
    print "<td colspan=4><CENTER><p><FONT SIZE=-1>Please report only one problem at a time. Your report should include a complete description of the problem.\n";
    print "Please remember to include any barcodes, user names or id's you are using if applicable to the problem.<br> \n";
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
    print "<td colspan=2 align=\"center\"><input type=submit value=\"NEXT\"></td>\n";
    print "<td colspan=2 align=\"center\"><input type=reset value=\"CLEAR\"></td>\n";
    print "</tr>\n";
    print "</table>\n";
    print "</form>\n";
    print "</table>\n";
}

=head2 print_page_start()

Print the HTTP header and the start of the HTML page.

=cut
sub print_page_start {
    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>RxWeb Form</title>\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<h1>RxWeb Form</h1>\n";
    print "</body>\n</html>\n";
}

=head2 print_page_end()

Print the end of the HTML page, from the close of the body onward.

=cut
sub print_page_end {
    print "</body>\n";
    print "<HEAD>\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</HEAD></HTML>\n";
}



=head2 recipient()

Sets the recipient email (C<$recipient>) based on the selected group (C<$grp>).

=cut
sub recipient {
    $recipient = $AlephRx::Util::RECIPIENT_FOR{$grp};
}

    

=head2 match()

Checks the database for matching/duplicate reports when submitting. Sets
C<$match_rows> to the number of matching rows found.

=cut
sub match {
    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password, { RaiseError => 1 });

    $statement = "select report.text, report.date, people.phone, people.name from report, people WHERE people.id = report.id and report.text = ? and report.date = NOW() and people.phone = ? and people.name = ?";

    $sth = $dbh->prepare($statement);
    $sth->execute($text, $phone, $name);

    $match_rows = $sth->rows;
}

=head2 email_config()

Displays the form with emailing options. Calls L<email_display()> to print the
actual form for selecting email addresses. Also includes the report data as
hidden fields, to get passed on to the report confirmation page rendered by
ALEPHemail.cgi.

This form is submitted to the ALEPHemail.cgi script, which does the validation
of the email addresses and the actual emailing.

=cut
sub email_config {

    $display = "yes";
    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>Confirm AlephRx Email Notifications</title>\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "</head>\n<body bgcolor=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>Confirm AlephRx Email Notifications</h1>\n";
    print "<h3>Please confirm the Email configuration for your report </h3>\n";
    print "<FORM ACTION=\"ALEPHemail.cgi\" METHOD=\"post\">\n";
    print "<table>\n";
    &email_display;
    print "<tr><td align=\"left\">\n";
    print "<p><input TYPE=\"submit\" VALUE=\"Submit\"></p>\n";
    print "<INPUT TYPE=\"hidden\" name=\"email_config\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"submitted\" VALUE=\"yes\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"name\" VALUE=\"$name\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"text\" VALUE=\"$escaped_text\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"summary\" VALUE=\"$escaped_summary\">\n";
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


=head2 display_error()

Displays an error page when the form does not validate. The error message is
expected to be in the C<$error_message> variable.

=cut
sub display_error {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>Error Submitting a Report to AlephRx</title>\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</head>\n<body>\n";
    print "<center>\n";
    print "<h1>Error Submitting a Report to AlephRx</h1>\n";
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


=head2 email_display()

Prints the HTML of the form to select which email addresses to send to. Called
by L<email_config()>.

=cut
sub email_display {
    print "<TABLE border=\"0\" width=\"60%\">\n";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "<tr><td colspan=\"2\"><hr></td></tr>\n";
    print "<tr><td colspan=\"2\">Community:&nbsp;&nbsp;<cite><b>$recipient</b></cite></td></tr>\n";
    print "<INPUT TYPE=\"hidden\" name=\"email1\" VALUE=\"email1\">\n";
    print "<tr><td colspan=\"2\"><INPUT TYPE=\"checkbox\" NAME=\"email2\" VALUE=\"email2\" checked>Reported by:&nbsp;&nbsp;<b><cite>$email</b></cite></td></tr>\n";
    print "<tr><td><INPUT TYPE=\"checkbox\" NAME=\"email3\" VALUE=\"yes\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email3a\"  cols=80 maxlength=80></td></tr>\n";
    print "<tr><td width=\"120\"><INPUT TYPE=\"checkbox\" NAME=\"email4\" VALUE=\"yes\">Additional email</td>\n";
    print"<td><INPUT TYPE=\"text\" NAME=\"email4a\"  cols=80 maxlength=80></td></tr>\n";

    print "<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Additional Community</td>\n";
    print "<td><select name=\"email5\" size=1>\n";
    print "<option>\n";
    print "<option>usmaicoiseracq\@umd.edu\n";
    print "<option>usmaicoicircresill\@umd.edu\n";
    print "<option>usmaicoicatdbmaint\@umd.edu\n";
    print "<option>usmaicoidesktech\@umd.edu\n";
    print "<option>usmaicoiuserinter\@umd.edu\n";
    print "<option>usmaicoiall\@umd.edu\n";
    print "</select></td>\n";
    print "</tr>\n";
    print "</TABLE><br>\n";
}
