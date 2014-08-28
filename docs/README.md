Aleph Rx Application
====================

Overview of Screens
-------------------

The end user's point of entry to the system is the request submission screen,
titled "RxWeb Form". On this screen, the user fills out a new request and
submits it to the system. Once the request is submitted, the system takes the
user to an email notification confirmation screen.

On the email notification confirmation screen, the user can select additional
email addresses to send notifications to. The notification email is *always*
sent to the usmaialeph@umd.edu community, and by default the reporting user's
email address (that they provided on the request submission screen) is
selected.  The system provides two additional input boxes for additional emails,
as well as a dropdown to select from a predefined list of communities. If they
wish to make use of the text inputs for additional emails, the user must check
the checkbox next to the text input field in addition to filling in an email
address.

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

The end user details view just shows the initial request and any replies and
responses to it. It also contains a link to the end user response screen for
this issue.

The end user repsonse screen, title "RxWeb Reply", shows the same table of
information as the end user details view. In addition, it provides a form for
the user to submit a reply, and to choose where to send email notifications. The
email notifications portion of the form behaves in the same way as on the staff
details screen.

Technical Details
-----------------

The above text is intended as a high-level overview of the application
functionality. For more technical information, please see the following:

- [CGI Scripts](scripts.md)
- [Database Schema](database.md)

Diagrams
--------

The .dot diagrams in the documentation are written using
[GraphViz](http://www.graphviz.org). Images can be generated from them using the
`dot` command line program:

    $ dot -Tpng -osubmit.png submit.dot

See the [documentaion Makefile](Makefile) for more info.
