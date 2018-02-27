#!/usr/bin/perl

use warnings;
use strict;

#prog

my ($input_file) = "connectivity_matrix.csv";
my ($output_file) = "connectivity_matrix.yml";

open (IN, $input_file) or die;
open (OUT, ">$output_file") or die;

print OUT "---\nnode:\n";

while (my $line = <IN>) {
	my @words = split(/;/, $line);
	print OUT "  - hostname: $words[0]\n    type: $words[1]\n    model: $words[2]\n    os: $words[3]\n    vcpu: $words[4]\n    vram $words[5]\n    vdisk: $words[6]\n    ip_address:\n      ipxe: $words[7]\n      mgmt: $words[8]\n      sw_mgmt: $words[9]\n    console:\n      server: $words[10]\n      port: $words[11]\n    mgmt:\n      switch: $words[12]\n      port: $words[13]\n    username: $words[14]\n    url: $words[15]\n    rack: $words[16]";
}

print OUT "...\n";

close IN;
close OUT;

exit;
