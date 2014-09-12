package AlephRx::Database;

use Moose;
use DBI;
use AlephRx::Report;

has dbh => (is => 'ro', isa => 'DBI::db');

sub BUILDARGS {
    my ($self, @dbi_args) = @_;
    return {
        dbh => DBI->connect(@dbi_args, { RaiseError => 1 }),
    };
}

=head2 report_exists($text, $phone, $name)

Check to see if a report with the given text, phone number, reporter name, and
today's date already exists in the database. This is used to prevent the
submission of duplicates. Returns the count of matching rows.

Note that this currently has a bug, whereby no duplicates will ever be found. To
fix, must do an explicit cast of the C<NOW()> function to the C<DATE> type.

=cut
sub report_exists {
    my ($self, $text, $phone, $name) = @_;

    my $statement = "SELECT COUNT(*) FROM report, people WHERE people.id = report.id AND report.text = ? AND report.date = NOW() AND people.phone = ? AND people.name = ?";

    my $sth = $self->dbh->prepare($statement);
    $sth->execute($text, $phone, $name);

    return scalar $sth->fetchrow_array;
}

=head2 submit_report($data)

Creates a new report in the database, and returns a new AlephRx::Report object
representing that report. Expects the following keys in the C<$data> hashref:

    name
    functional_area
    campus
    phone
    email
    status
    summary
    text
    submitter_name

=cut
sub submit_report {
    my ($self, $data) = @_;

    my $sth_people = $self->dbh->prepare("INSERT INTO people (name, grp, campus, phone, email) VALUES (?, ?, ?, ?, ?)");
    $sth_people->execute(@{ $data }{qw{name functional_area campus phone email}});

    my $id = $self->dbh->last_insert_id(undef, undef, 'people', 'id');

    my $statement = "INSERT INTO report (id, date, status, summary, text, cataloger, timestamp, updated, version) VALUES (LAST_INSERT_ID(), NOW(), ?, ?, ?, ?, NOW(), NOW(), '18.01')";

    my $sth_report = $self->dbh->prepare($statement);
    $sth_report->execute(@{ $data }{qw{status summary text submitter_name}});

    return $self->get_report($id);
}

=head2 get_report($id)

Get a report by its ID. Returns undef if a report with that ID cannot be found.

=cut
sub get_report {
    my ($self, $id) = @_;

    my $statement = <<END_SQL;
SELECT 
    people.id AS id,
    people.name AS name,
    people.email AS email,
    people.phone AS phone,
    people.campus AS campus,
    people.grp AS functional_area,
    report.status AS status,
    report.summary AS summary,
    report.text AS text,
    report.supress AS supress,
    report.cataloger AS submitter_name,
    DATE_FORMAT(report.date,'%m/%d/%y') AS created_date,
    report.timestamp AS created,
    report.updated AS updated
FROM people, report
WHERE people.id = ? AND people.id = report.id
END_SQL
    my $sth = $self->dbh->prepare($statement);
    $sth->execute($id);

    my $data = $sth->fetchrow_hashref;
    return unless $data;

    $data->{db} = $self;

    return AlephRx::Report->new($data);
}

1;
