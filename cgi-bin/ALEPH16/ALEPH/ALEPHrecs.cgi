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



$filter_value = $query->param('filter_value');
$numrec = $query->param('numrec');
$record = $query->param('record');
$page_increment = $query->param('page_increment');
$sort_value = $query->param('sort_value');
$val = $query->param('sort');
$id_i = $query->param('id_i');



&print_form;

sub print_form {

    print "Content-type:  text/html\n\n";
    print "<html>\n<head>\n";
    print "<title>ALEPH16 RX Records Per Page Update</title>\n";
#    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
#    print "<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n";
    print "</head>\n<body BGCOLOR=\"#98AFC7\">\n";
    print "<center>\n";
    print "<h1>ALEPH16 RX Records Per Page Update</h1>\n";
    print "<FORM method=\"POST\" action=\"\/cgi-bin\/ALEPH16\/ALEPH\/FORM2.cgi\">\n";
    print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Maintenance Summaries\" onClick=\"parent.location='ALEPHform2.cgi?id'\"><BR><BR>\n";
    print "Select the number of records per page:&nbsp;\n";
    print "<input type=text name=numrec size=3 maxsize=3>\n";
    print "<input type=submit value=\"Update\">\n";
    print "<BR>$id_i\n";
    print "<BR>$sort\n";
    print "<BR>$filter_value\n";
    print "<INPUT TYPE=\"hidden\" name=\"record\" VALUE=\"$record\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$page_increment\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter_value\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort_value\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"val\" VALUE=\"$sort\">\n";
    print "<INPUT TYPE=\"hidden\" name=\"id_i\" VALUE=\"$id_i\">\n";
    print "<BR>\n";
    print "</FORM>\n";
    print "</body></html>\n";
}






