Some ideas on how to clean up the codebase:

add comments to explain the flow of what is going on

extract the mapping of groups -> email addresses to a datafile

extract the db connection info into a config file

replace all custom parsing of HTTP requests with CGI.pm

replace the custom HTTP response header generation with CGI.pm

use DBI prepared statements (if supported by the version of DBD::mysql running
on itd.umd.edu) instead of raw interpolation

replace the print-statement generation of HTML with templates
