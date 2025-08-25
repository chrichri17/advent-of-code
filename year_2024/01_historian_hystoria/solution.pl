use strict;
use warnings;

use feature ':5.10';
use List::Util qw(sum);


open(my $fh, '<', 'data/in.txt') or die "Cannot open file in.txt: $!";

my (@lloc, @rloc);

while (my $line = readline($fh)) {
    my ($x, $y) = split(' ', $line);
    push @lloc, $x;
    push @rloc, $y;
}
close($fh);

@lloc = sort @lloc;
@rloc = sort @rloc;

# Part 1
say sum(map { abs $lloc[$_] - $rloc[$_] } 0 .. $#lloc);

# Part 2
my %counter;
$counter{$_}++ for @rloc;

say sum(map { exists $counter{$_} ? $counter{$_} * $_  : 0 } @lloc);
