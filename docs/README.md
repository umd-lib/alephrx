Aleph Rx Application
====================

For information on setting up a development environment, see the [VM
docs](../vm/README.md). For information on using the HTTP API to create reports,
see the [HTTP API docs](../cgi-bin/api/README.md).

Overview of Screens
-------------------

### End User ###

The end user's point of entry to the system is the request submission screen,
titled "RxWeb Form". On this screen, the user fills out a new request and
submits it to the system. Once the request is submitted and validated, the
system creates a new record in the database. Then the system takes the user to
an email notification confirmation screen.

On the email notification confirmation screen, the user can select additional
email addresses to send notifications to. The notification email is *always*
sent to the usmaialeph@umd.edu community, and by default the reporting user's
email address (that they provided on the request submission screen) is
selected.  The system provides two additional input boxes for additional emails,
as well as a dropdown to select from a predefined list of communities. If they
wish to make use of the text inputs for additional emails, the user must check
the checkbox next to the text input field in addition to filling in an email
address.

After the user submits the email confirmation form, the system checks the email
addresses. If any of these addresses are invalid, the system displays an error
message page to the user. The user may then navigate back to the email
confirmation form to correct their errors. If all of the submitted addresses are
valid, the system sends the email and then displays a confirmation page
containing the submitted report information.

The end user also has access to the user summary screen. This screen displays a
summary view of all of the reports in the system. By default, all reports are
shown, sorted by their ID number. The user may select one of several filters to
narrow the display of the reports. The user may also sort by columns other
than the ID number, in either ascending or descending order. Only 30 records are
displayed per page; if there are more than 30 records returned, the system
displays a set of buttons to navigate to the preivous, next, first, and last
pages, as appropriate.

From the user summary screen, the user may view the full details of any report.
The report details page shows the report information followed by a reverse
chronological listing of all the responses and replies to that report. From the
report details page, the user may go to the reply form to submit a reply to the
report.

On the reply form, the user enters their name and the text of their reply. They
can also select where to send email notifications to.

From the user summary screen, the end user also has access to a basic search
form. The basic search looks for a literal occurence of the search term anywhere
in the field to be searched.

### Library Staff User ###

A library staff user views a list of requests via the staff summary view screen,
titled "RxWeb Update". From this screen, they may filter the list of requests
present using a number of predefined filter buttons. They may also sort the
requests on different columns, either ascending or descending. Only 30 records
are displayed per page; if there are more than 30 records returned, the system
displays a set of buttons to navigate to the preivous, next, first, and last
pages, as appropriate.

From the summary view screen, the library staff user may go to either the staff
or end user details view of an individual request. On the staff details view,
titled "RxWeb Update - Record {id}", the staff user may change any of the fields
in the report as well as submitting a response. As part of submitting a
response, the user may choose where to send the notification email. By default,
the usmaialeph@umd.edu community is selected, as is the email address of the
person who reported the issue. There are two text inputs for additional email
addresses as well as a single-select dropdown to select an additional predefined
community email address (typically a listserv or reflector address).

In addition, each existing reply or response is displayed below the request
information. Each one links to the reply editing screen, titled "RxWeb Reply
Edit Test", where the staff user may edit the text of any reply. Unlike the
other form submissions in the application, there is no email notification
functionality associated with this screen.

Note that while the reply editing screen's title includes the word "Test" and a
notice that "This function is still in development", this feature has been in
production use for a while and, according to library staff users, appears to be
stable.

Page Flow Diagrams
------------------

- [Submitting a report](submit.png)
- [End user replying to a report](userreply.png)
- [Staff user updating a report](staffresponse.png)
- [Basic search](search.png)

### Reading the Diagrams ###

Rectangles are pages that are rendered by the CGI script. Ovals are general
server-side processes, usually ones that cause changes (updating the database,
sending email, etc.). Diamonds are decision points, sometimes a binary if-then,
but may have more than two conditions. The conditions are noted as bracketed
guard expressions on the edges leading out of the diamond (e.g. "[invalid]").

An incoming arrow to a page means "render this page". A labelled outgoing arrow
from a page is user-initiated navigation, either a link or a form submission.

The pages, processes, and decision points that happen within a single script are
grouped into a cluster labeled with the name of that script.

Open arrowheads between two pages indicate a subclass-like relationship. Any
action that the "parent class" page can take, the "subclass" page can take. This
is used primarily when the parent page sometimes gets displayed with an update
notice or other notification about the previous request, but its primary
functionality remains unchanged.

Technical Details
-----------------

The above text is intended as a high-level overview of the application
functionality. For more technical information, please see the following:

- [CGI Scripts](scripts.md)
- [All Script Interconnections](pageflow.png)
- [Database Schema](database.md)
- [Codebase Cleanup Ideas](codefixes.md)
- [HTTP API](../cgi-bin/api/README.md)
- [Development VM](../vm/README.md)

### Diagram Source Code ###

The .dot diagrams in the documentation are written using
[GraphViz](http://www.graphviz.org). The PNG images are generated from them
using the `dot` command line program:

    $ dot -Tpng -osubmit.png submit.dot

There is also a [documentaion Makefile](Makefile) that will regenerate all of
the diagram images at once.
