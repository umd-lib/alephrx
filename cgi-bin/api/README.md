AlephRx HTTP API
================

This is the documentation for a simple HTTP API to the AlephRx system. The
examples that follow assume that the [cgi-bin directory](../) is mapped to
`/cgi-bin` on the server.

## Create a Report

POST XML or form data to [reports](reports). Please note that unlike the regular
form submission to AlephRx, this method does not send out notification emails.

### Request

XML:

    POST /cgi-bin/api/reports
    Content-Type: application/xml

    <report>
        <name>J. User</name>
        <functional_area>other</functional_area>
        <campus>UMCP</campus>
        <phone>301-555-0123</phone>
        <email>juser@example.com</email>
        <status>new</status>
        <summary>Problem Summary</summary>
        <text>Full text describing the issue...</text>
        <!-- submitter name is optional -->
        <submitter_name>A.N. Other</submitter_name>
    </report>

Form data:

    POST /cgi-bin/api/reports
    Content-Type: application/x-www-form-urlencoded

    name=J.%20User&functional_area=other&campus=UMCP&phone=301-555-0123&email=juser@example.com&status=new&summary=Problem%20Summary&text=Full%20text%20describing%20the%20issue...&submitter_name=A.N.%20Other

#### Request Body (XML)

The request must have a `Content-Type` of `application/xml` (preferred) or
`text/xml`. The request body XML format is a simple one. All of the child
elements of `report` are required except for `submitter_name`, and they all must
have simple string values as their content. In addition, the following
formatting restrictions apply:

- **phone** Must be in the format `NNN-NNN-NNNN`
- **email** Must look like an email address. See the source code in
  [AlephRx::Database::validate_data()](../../lib/AlephRx/Database.pm) for the
  exact rules used.

#### Request Body (Form Data)

The request must have a `Content-Type` of `application/x-www-form-urlencoded`.
Each of the form parameters are required, except for `submitter_name`. The form
parameters have the same names as the XML elements used in the XML version of
this request, and the values are subject to the same restrictions.

### Responses

The `Content-Type` header for all responses is `text/plain`.

**201 Created** Report was created. The `Location` response header contains the
URL of the newly created report, as does the response body.

**400 Bad Request** Unable to parse the submitted data as XML (if the request
`Content-Type` was an XML type), or there were missing or invalid fields in the
submitted data. If there are missing fields, they are listed in the second
paragraph of the response body.

**405 Method Not Allowed** A request method other than POST was used on this
endpoint.

**415 Unsupported Media Type** The request `Content-Type` header was set to
something other than `application/xml`, `text/xml`, or
`application/x-www-form-urlencoded`.

**500 Internal Server Error** There was a problem creating the record in the
database.
