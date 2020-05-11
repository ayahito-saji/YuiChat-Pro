package jcode;
;######################################################################
;#
;# jcode.pl: Perl library for Japanese character code conversion
;#
;# Copyright (c) 1995-1999 Kazumasa Utashiro <utashiro@iij.ad.jp>
;# Internet Initiative Japan Inc.
;# 3-13 Kanda Nishiki-cho, Chiyoda-ku, Tokyo 101-0054, Japan
;#
;# Copyright (c) 1992,1993,1994 Kazumasa Utashiro
;# Software Research Associates, Inc.
;#
;# Original version was developed under the name of srekcah@sra.co.jp
;# February 1992 and it was called kconv.pl at the beginning.  This
;# address was a pen name for group of individuals and it is no longer
;# valid.
;#
;# Use and redistribution for ANY PURPOSE, without significant
;# modification, is granted as long as all copyright notices are
;# retained.  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND
;# ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.
;#
;# The latest version is available here:
;#
;#	ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/
;#
;#; $rcsid = q$Id: jcode.pl,v 2.10 1999/01/10 13:43:14 utashiro Exp $;
;#
;######################################################################
;######################################################################
;#注意！！
;#このjcodeLE.plは、チャットスクリプト　ゆいちゃっと専用に利用するために、
;#余分な機能を削除した、機能限定版(Limited Edition)です。
;#不要なサブルーチンの削除と、それにともなう一部のルーチンの修正だけしています。
;#オリジナルのjcode.plは、多機能かつ汎用性に優れているものです。
;#ちなみに、この限定jcodeLE.plは、
;#&jcode'convert(*value,'sjis');#通常のsjisへの変換
;#のみ可能です。euc変換機能はありません。
;#他のCGIスクリプトで上記の機能しか使わないのなら、jcodeLE.plでも大丈夫でしょう。
;#注意：jcode.plを改変して配付する場合は、オリジナルと区別するために、別名にしましょう。
;#1997年4月5日初版
;#1999年4月5日2.10を元に作成
;# 改変責任者　Suzuki Yui <E-mail:yui@cup.com>
;#####################################################################
&init unless defined $version;
sub init {
    $version =  '2.10:LimitedEdition';
    $convf{'jis'} = *jis2sjis;
    $convf{'euc'} = *euc2sjis;
    $convf{'sjis'} = *sjis2sjis;
}
sub getcode {
    local(*_) = @_;
    local($code);
    if (!/[\e\200-\377]/) {	# not Japanese
	$code = undef;
    }				# 'jis'
    elsif (/\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I/o) {
	$code = 'jis';
    }
    elsif (/[\000-\006\177\377]/o) {	# 'binary'
	$code = 'binary';
    }
    else {			# should be 'euc' or 'sjis'
	local($sjis, $euc);
	$sjis += length($1) while /(([\201-\237\340-\374][\100-\176\200-\374])+)/go;
	$euc  += length($1) while /(([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])+)/go;
	&max($sjis, $euc);
	$code = ('euc', undef, 'sjis')[($sjis<=>$euc) + $[ + 1];
    }
    $code;
}
sub max { $_[ $[ + ($_[$[] < $_[$[+1]) ]; }
sub convert {
    local(*_, $icode) = @_;
    return (undef, undef) unless $icode = &getcode(*_);
    return (undef, $icode) if $icode eq 'binary';
    local(*f) = $convf{$icode};
    &f(*_);
     (*f);
}
sub jis2sjis {
    local(*_, $n) = @_;
    s/(\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I)([^\e]*)/&_jis2sjis($1,$2)/geo;
    $n;
}
sub _jis2sjis {
    local($esc, $_) = @_;
    if ($esc =~ /\e\$\(D/o) {
	s/../\x81\xac/g;
	$n = length;
    }
    elsif ($esc !~ /\e\([BJ]/o) {
	$n += tr/\041-\176/\241-\376/;
	s/([\241-\376][\241-\376])/&e2s($1)/geo if $esc =~ /\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D/o;
    }
    $_;
}
sub euc2sjis {
    local(*_, $n) = @_;
    $n = s/([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])/&e2s($1)/geo;
}
sub e2s {
    local($c1, $c2, $code);
    ($c1, $c2) = unpack('CC', $code = shift);
    if ($c1 == 0x8e) {		# SS2
	return substr($code, 1, 1);
    } elsif ($c1 == 0x8f) {	# SS3
	return "\x81\xac";
    } elsif ($c1 % 2) {
	$c1 = ($c1>>1) + ($c1 < 0xdf ? 0x31 : 0x71);
	$c2 -= 0x60 + ($c2 < 0xe0);
    } else {
	$c1 = ($c1>>1) + ($c1 < 0xdf ? 0x30 : 0x70);
	$c2 -= 2;
    }
	pack('CC', $c1, $c2);
}
sub sjis2sjis {
    local(*_) = @_;
}
1;
