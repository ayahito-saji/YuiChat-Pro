#! /usr/local/bin/perl
#
#ゅぃぼっとゆーてぃりてぃ  Ver.1.0
#ゆいぼっと用辞書のメンテナンスを行います。
#著作権はゆいちゃっとのゆいにあります。
#
#本スクリプトは、ゆいぼっとの管理人さん、または、親しい常連さん
#のみにURLを秘密公開してください。
#悪意の参加者が全ての辞書登録を削除する可能性があります。
#利用にあたっては、十分にご注意ください。
require './jcodeLE.pl';
$bot_file = './yui.dat';
&decode;

&search if ($mode);
&html;
exit;
sub html {
#検索実行直後のみ番号指定可にする。
$bangou='<INPUT TYPE=radio NAME="mode" VALUE="del3">行番号指定削除' if ($mode eq 'search');

print "Content-type: text/html\n\n";
print <<"_HTML_";
<HTML><HEAD>
<TITLE>BotUtility1.0</TITLE>
</HEAD>
<BODY bgcolor="#333333" text="#ffffff" link="#00ff00" vlink="#00ff00" alink="#ff0000">
<font color=red>警告：初めてこのスクリプトを利用する場合は、辞書のバックアップをお願いします。</font><BR>
ゆいぼっと辞書のメンテナンス専用です。<BR>
発言に対する応答検索、キーワードによる削除、応答による削除を行うことができます。
<HR>
<FORM METHOD="post" ACTION="./bottool.cgi">
モード：<INPUT TYPE=radio NAME="mode" VALUE="search" checked>検索
<INPUT TYPE=radio NAME="mode" VALUE="del1">キーワード削除
<INPUT TYPE=radio NAME="mode" VALUE="del2">応答削除
$bangou
<BR>文字列：<INPUT TYPE=text NAME="chat" SIZE="70">
<INPUT TYPE=submit VALUE="OK"></FORM><HR>
_HTML_
if(($chat ne "") && $mode eq 'search'){
	print "発言内容：<b>$chat</b><br>\n";
	print "$total通りの応答が可能\です。<hr>\n";
	@ans = reverse @ans;
	print @ans;
}

if($del){
	print "<b>$chat</b>を含む、$del個の登録を削除しました。辞書トータル:$total<br><br>\n";
	print "削除一覧：<br>\n";
	print @dels;
}elsif($mode =~/del/){
	print "<b>$chat</b>の削除に失敗しました。辞書トータル:$total<br><br>\n";
}
print <<'_HTML_';
<HR>
<A HREF="http://www.cup.com/yui/chat/free/Bot/bottool.html">こちらに</A>使い方の説明があります。
<H5 ALIGN=right>ゅぃぼっとゆーてぃりてぃ  Ver.1.0</H5>
</BODY></HTML>
_HTML_
}#html END

sub decode {

if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }
   @pairs = split(/&/,$buffer);
   foreach $pair (@pairs)
   {
       ($name, $value) = split(/=/, $pair);
       $value =~ tr/+/ /;
       $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
       $value =~ s/\n//g;       $value =~ s/\r//g;
       &jcode'convert(*value,'sjis');
       $FORM{$name} = $value;
   }
   $chat = $FORM{'chat'};   $mode = $FORM{'mode'};
}#decode END

sub search{
undef (@ans);
open(DB,"$bot_file") || exit;
$i=0;
while(<DB>){
chop;
$messege=$_;
($key,$res)=split(/:#/);
next if $key eq '';
$i++;
if($mode eq 'del1'){#キーワード削除
	$keyword = $key;
}elsif($mode eq 'del2'){#応答削除
	$keyword = $res;
}elsif($mode eq 'del3'){#番号削除
	$keyword = $i;
}else{
	$test=0;
	eval {$test=1 if $chat=~/.*$key.*/;};
	if($@ ne ''){	$test=1 if (index($chat,$key) >= 0 );	}
	$res=$key.":#".$res.":#($i)<br>";
	push(@ans,$res) if $test;
	next;
}


if ($chat ne $keyword){
	push(@ans,"$messege\n") ; #残すリスト
}else{
	push(@dels,"$messege ($i)<BR>") ; #削除リスト
}
}#while
close(DB);
$total=@ans;$del=@dels;
&write if ( ($mode=~/del/) && $del);
}#search END

sub write{
	open(DB,">$bot_file") || exit;
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @ans;
		eval 'flock(DB,8);';
	close(DB);
}#write END
__END__
