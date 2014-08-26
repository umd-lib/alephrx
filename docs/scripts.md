AlephRx CGI Scripts
===================

General Notes
-------------

Uses global variables.

Linear control structure.

Uses `CGI::Carp 'fatalsToBrowser'` to automatically generate error pages when
dying.

All of the scripts assume that the URL path starts with **/cgi-bin** and that
static images are stored in **/IMG**. No other static resources besides images
are used.

The database connection information and location of the mailer program is passed
to the scripts via environment variables that are set in the Apache httpd.conf
or vhost configuration file.  These should be set in a `<Directory>` directive
for the *cgi-bin* directory, so that all the scripts in all the subdirectories
can see the values. The variables to set are:

- `ALEPHRX_DATABASE_HOST`
- `ALEPHRX_DATABASE_NAME`
- `ALEPHRX_DATABASE_USER`
- `ALEPHRX_DATABASE_PASS`
- `ALEPHRX_MAILER`

Software Versions
-----------------

These are the versions on the current production server (itd.umd.edu):

- perl: 5.6.1
- CGI: 2.752
- CGI::Carp: 1.20
- DBI: 1.18
- DBD::mysql: 2.0416
- IO::Handle: 1.21

Several of the scripts have `use lib '/lims/lib/perl'`, but that location does
not exist on the server.

DBD::mysql 2.0416 is from the Msql-Mysql-modules distribution. See
http://search.cpan.org/~jwied/Msql-Mysql-modules-1.2216/mysql/lib/DBD/mysql.pm
on CPAN.

The application appears to run successfully on a CentOS 5.1 VM (intended as a
close analogue for RHEL 5.1), with the following software versions:

- perl: 5.8.8
- CGI: 3.15
- CGI::Carp: 1.29
- DBI: 1.631
- DBD::mysql: 3.0007
- IO::Handle: 1.25

The only syntactic change needed to the source code (which happened prior to
placement into version control) was to change several instances of `EQ` and `NE`
to `eq` and `ne`.

Public Access Scripts
---------------------

**ALEPHform.cgi**

- Displays the form to submit a new issue.
- With a `submitted` parameter, validates submitted data and inserts it into
  the database, then displays a form to confirm email settings. This form
  submits to *ALEPHemail.cgi*.

**ALEPHemail.cgi**

- Displays a form to confirm email settings.
- Always sends to usmaialeph, defaults to sending to the reporter. The form
  provides 2 additional email text box inputs and a single choice dropdown
  to select up to 1 listserv/reflector address. This list of listservs is
  hardcoded into the form.
- When submitted, validates email addresses and sends email(s).

**ALEPHdate.cgi**

- *UNDER DEVELOPMENT/NON-PRODUCTION*
- The intent of this form is to provide "templates" for common requests that
  prompt the user for specific information, rather than forcing them to
  remember and enter all of the necessary information into the textarea.

Restricted Access Scripts
-------------------------

These scripts should be protected by HTTP authentication.

### User Access ###

These scripts are all in the **ALEPH16** directory.

**ALEPHsearch.cgi**

- Displays a form to search the issue reports and replies. Available columns
  to search are:
    - summary => report.summary
    - text => report.text
    - name => people.name
    - reply => reply.text or reply.name (searches both)
- Searches are of the form `column LIKE '%$term%'`.
- Displays an error page if the search term is empty.
- POSTs to itself, queries the database, and displays results. Each result
  links to the *ALEPHsum_full.cgi* page for that issue.

**ALEPHsum.cgi**

- User summary view of issues.
- Page is called "RxWeb Reports" or "RxWeb".
- Displays a table summary of issues.
- Has a form to quickly go to an issue by number. Sends a POST request to
  *ALEPHsum_full.cgi* with the report id in the POST body as `record`.
- POSTs to itself to update filtering and sorting options.
- Paginated at 30 records per page.
- Links to full info pages (*ALEPHsum_full.cgi*) for each issue displayed.

**ALEPHstats.cgi**

- Page is called "RxWeb Statistics".
- Displays the number of reports grouped by date, campus, group, user, and
  status.
- Reports grouped by date only search reports made in 2006 or later.
- Not often used by staff in their day-to-day work. It is more of a set of
  quick-and-dirty statistics rather than an in-depth statistical reporting
  tool. Much of this is due to users inaccurately catergorizing issues.

**ALEPHsum_full.cgi?{report.id}**

- User full view of the ticket.
- Displays issue and all responses to it.
- Links to *ALEPHreply.cgi* to create a new reply to this issue.

**ALEPHreply.cgi?{report.id}**

- User reply form.
- Displays a form to submit a reply to the issue.
- POSTs to *ALEPHxreply.cgi* to handle updating the database.

**ALEPHxreply.cgi**

- Inserts a new reply into the database.
- The `reply.parent_id` value is passed in as the `record_id` POST
  parameter.

### Staff Access ###

These scripts are all in the **ALEPH16/ALEPH** directory.

**ALEPHsearch.cgi**

- Search form that is almost identical to the user search form.
- See *ALEPHsearch.cgi* in the _User Access_ section.

**ALEPHform2.cgi**

- Staff summary view of issues. This is the starting point for staff users,
  who generally bookmark this page. There do not appear to be any direct
  links to this page from the user side of AlephRX.
- Has all the features of the *ALEPHsum.cgi* page.
- Has additional filter buttons for staff.
- The "UPDATE" button for each record links to the form for staff to update
  the report and add a response (*ALEPHurecord.cgi*).

**ALEPHurecord.cgi**

- Staff form to modify fields in the report and to add a response.
- Links to *ALEPHureply.cgi* to allow staff to edit submitted replies.
- POSTs to *ALEPHform2.cgi* to update the record in the database.
- Includes a form to set email notification options for this update.

**ALEPHureply.cgi**

- Staff form to modify the text of a reply.
- There is no email notification and no error checking. Page also has an
  "Under development" notice, but it has been in production use for a while.

#### Possibly Unused ####

**ALEPHrecs.cgi**

- Has no inbound links from any other scripts.
- POSTs to *FORM2.cgi*, which currently 404s because the script on the
  server is named in lowercase, *form2.cgi*.

**ALEPHfulltext.cgi**

- *UNDER DEVELOPMENT/NON-PRODUCTION*
- Uses `MATCH ... AGAINST ...` to do a natural language search.
- Uses the full text indexes in the `report` table (text and summary
  columns) and the `reply` table (text and name) to do matching across
  multiple tables.
- The search term must be non-empty.

**ALEPHdrecord.cgi?{report.id}**

- Appears to be a confirmation form to delete a record.
- Only has inbound links from *ALEPHirecord.cgi* and *ALEPHxrecord.cgi*.
  Does not appear to be linked to from anywhere in the usual application
  flow.
- POSTs to *ALEPHxrecord.cgi* with the `report.id` as a hidden field with
  the name `record_id`.

**ALEPHxrecord.cgi**

- Deletes a record if there is a `yes` POST parameter. Deletion is canceled
  if there is a `no` POST parameter.
- Deletes the rows in the report and people tables where the id matches the
  POSTed `record_id`. Also deletes any rows in the reply table whose
  `parent_id` matches the `record_id`.
- After deletion displays a summary table much like the *ALEPHform2.cgi*
  script.
- Only has inbound links from *ALEPHdrecord.cgi*. Does not appear to be
  linked to from anywhere in the usual application flow.

**ALEPHirecord.cgi**

- Has no inbound links from any other the other scripts.

**ALEPHupdate.cgi**

- Has no inbound links from any other the other scripts.

Furthermore, the copies of *ALEPHdrecord.cgi*, *ALEPHirecord.cgi*, and
*ALEPHxrecord.cgi* in the *ALEPH* and *ALEPH16/ALEPH* directories are identical.

Broken/Unknown/Other
--------------------

**ALEPH/*.cgi**: not linked to; are these under development or have they been
abandonned?

**ALEPH16/ALEPH18*.cgi**: also not linked to; are these under development or
have they been abandonned?

**ALEPH16/kbase_form.cgi**: currently broken due to a syntax error

**ALEPH16/FORM.cgi**: currently broken due to the Lims::IM module not being available
(related to the /lims/lib/perl directory not existing). Lims::IM looks like it
is a custom module (it is not on CPAN).
