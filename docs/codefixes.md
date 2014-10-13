Code Fixes
==========

If we decide to retain AlephRx (as opposed to switching to an off-the-shelf
product for handling these support requests), here are some ideas on how to
clean up the codebase to make it more secure and easier to maintain and
extend:

- Replace all custom parsing of HTTP requests with CGI.pm
- Replace the custom HTTP response header generation with CGI.pm
- Use DBI prepared statements instead of raw interpolation
- Replace the print-statement generation of HTML and emails with templates
- Extract the mapping of groups -> email addresses to a datafile
- Move duplicated functionality into a separate module
