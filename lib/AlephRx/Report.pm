package AlephRx::Report;

use Moose;

has db => (is => 'ro', isa => 'AlephRx::Database', handles => [qw{dbh}]);

has id => (is => 'ro');
has name => (is => 'rw');
has email => (is => 'rw');
has phone => (is => 'rw');
has campus => (is => 'rw');
has functional_area => (is => 'rw');
has status => (is => 'rw');
has summary => (is => 'rw');
has text => (is => 'rw');
has supress => (is => 'rw');
has submitter_name => (is => 'rw');
has created_date => (is => 'rw');
has created => (is => 'rw');
has updated => (is => 'rw');

1;
