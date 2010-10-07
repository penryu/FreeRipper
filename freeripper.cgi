#!/usr/bin/perl -w

use strict;
use vars qw/ $VERSION /;

$VERSION = '1.0';

my ($url, $begin, $end, $source_link, $new_link, $source_image, $new_image);
####################  CHANGE THESE VARIABLES  ####################
# This script was inspired by a commercial product of questionable
# quality.
#
# It should be functionally equivalent.  Set the following variables as
# required and execute it.
#
# FreeRipper has been test successfully as a CGI script and also
# with mod_perl. 
#
#1 - the URL of page you wish to begin extract
#2 - HTML at the beginning of the section to extract.
#3 - HTML at the end of the section to extract
#4 - change to reflect the link source if links don't work (remove the #'s)
#5 - change to reflect the image source if links don't work (remove the #'s)

#1
$url = 'http://www.activestate.com/';

#2
$begin = '<!-- Start of Press Article -->';

#3
$end = '<!-- End of Press Article -->';

#4
$source_link = ' href="/';
$new_link = ' href="http://www.activestate.com/';

#5  (don't uncomment unless images aren't working)
$source_image = 'img src="';
$new_image = 'img src="http://www.activestate.com/';

#################### END USER VARIABLES ####################

my $header = "Content-type: text/html\n\n";
exists $ENV{'MOD_PERL'}
    ? Apache->request->send_cgi_header($header)
    : print $header;

require LWP::UserAgent;

my $content = '';

$begin  =~ s#\s#\\s\+#;
$end    =~ s#\s#\\s\+#;

$url ? rip_page() : ($content = "<P>Enter the URL</P>");

print "<HTML>$content</HTML>";

sub rip_page {
    my ($ua, $req, $res);
    $ua = new LWP::UserAgent;
    $ua->timeout(60);
    $ua->agent('Mozilla/4.73'); 
    $req = HTTP::Request->new(GET => $url);
    $res = $ua->request($req);
    $content = $res->content;
    if ( $res->is_success ) {
        strip_page();
    }
    else {
        my $http_error = $res->code();
        $content = "<PRE>Error Getting Page:$url  Code: $http_error</PRE>";
    }
}

sub strip_page {
    $content = ($content =~ m#$begin(.+)$end#si)
        ? $1
        : '<PRE>Invalid <B>$Begin</B> and <B>$End</B> vars.</PRE>';
    if ($source_link) {
        $content =~ s/$source_link/$new_link/gi;
        $content =~ s/$new_link$new_link/$new_link/gi;
    }
    if ($source_image) {
        $content =~ s/$source_image/$new_image/gi;
    }
}
__END__
=pod

=head1 CAVEAT

The following README is included, with one exception, in it's
original form and text.  The only change I've made is the removal
of the project which "inspired" it.  Please enjoy the product of
arrogance that can only come with youth.

=head1 NAME

FreeRipper - rip pages from external sites to include in user pages

=head1 INSTALLATION

Installation is simple and straight forward and discussed at the top of
the FreeRipper script.

=head1 DESCRIPTION

FreeRipper allows you to fetch and use HTML from other web sites
directly on your site.  You simply supply the URL and the starting and
ending points to start fetching in minutes

Advantages of FreeRipper over similar scripts (such as [REDACTED] at
[REDACTED]):

=over 4

=item experience

FreeRipper was written by someone who actually knows Perl.

=item portability

FreeRipper is compatible with mod_perl and 'use strict'

=item efficiency

FreeRipper doesn't go through the trouble of reading, parsing, and
processing POST data (that isn't there) and then never even _attempt_
to use it.

=item efficiency (cont'd)

FreeRipper doesn't have numerous pointless page-wide regex substitutions
that would be unnecessary had the author any idea of how to use regex's.

=item ethics =)

FreeRipper doesn't tell you that removal of the pathetic link back to
the script's home will break the script.  As a matter of fact, there
_is_ no extra output with FreeRipper!

=back

=head1 NOTES

This copylefted script may be duplicated and sold without or without
written permission from anyone. 

This software is available to do whatever you want with. Change names,
butcher the Perl, or turn it into a hacker script.  The only condition
is that I'm not responsible for anything that happens to any code or
system after the tarball is opened.

=cut
