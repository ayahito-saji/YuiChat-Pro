#! /usr/local/bin/perl
#
#�ァ�ڂ��Ƃ�[�Ă���Ă�  Ver.1.0
#�䂢�ڂ��Ɨp�����̃����e�i���X���s���܂��B
#���쌠�͂䂢������Ƃ̂䂢�ɂ���܂��B
#
#�{�X�N���v�g�́A�䂢�ڂ��Ƃ̊Ǘ��l����A�܂��́A�e������A����
#�݂̂�URL��閧���J���Ă��������B
#���ӂ̎Q���҂��S�Ă̎����o�^���폜����\��������܂��B
#���p�ɂ������ẮA�\���ɂ����ӂ��������B
require './jcodeLE.pl';
$bot_file = './yui.dat';
&decode;

&search if ($mode);
&html;
exit;
sub html {
#�������s����̂ݔԍ��w��ɂ���B
$bangou='<INPUT TYPE=radio NAME="mode" VALUE="del3">�s�ԍ��w��폜' if ($mode eq 'search');

print "Content-type: text/html\n\n";
print <<"_HTML_";
<HTML><HEAD>
<TITLE>BotUtility1.0</TITLE>
</HEAD>
<BODY bgcolor="#333333" text="#ffffff" link="#00ff00" vlink="#00ff00" alink="#ff0000">
<font color=red>�x���F���߂Ă��̃X�N���v�g�𗘗p����ꍇ�́A�����̃o�b�N�A�b�v�����肢���܂��B</font><BR>
�䂢�ڂ��Ǝ����̃����e�i���X��p�ł��B<BR>
�����ɑ΂��鉞�������A�L�[���[�h�ɂ��폜�A�����ɂ��폜���s�����Ƃ��ł��܂��B
<HR>
<FORM METHOD="post" ACTION="./bottool.cgi">
���[�h�F<INPUT TYPE=radio NAME="mode" VALUE="search" checked>����
<INPUT TYPE=radio NAME="mode" VALUE="del1">�L�[���[�h�폜
<INPUT TYPE=radio NAME="mode" VALUE="del2">�����폜
$bangou
<BR>������F<INPUT TYPE=text NAME="chat" SIZE="70">
<INPUT TYPE=submit VALUE="OK"></FORM><HR>
_HTML_
if(($chat ne "") && $mode eq 'search'){
	print "�������e�F<b>$chat</b><br>\n";
	print "$total�ʂ�̉������\\�ł��B<hr>\n";
	@ans = reverse @ans;
	print @ans;
}

if($del){
	print "<b>$chat</b>���܂ށA$del�̓o�^���폜���܂����B�����g�[�^��:$total<br><br>\n";
	print "�폜�ꗗ�F<br>\n";
	print @dels;
}elsif($mode =~/del/){
	print "<b>$chat</b>�̍폜�Ɏ��s���܂����B�����g�[�^��:$total<br><br>\n";
}
print <<'_HTML_';
<HR>
<A HREF="http://www.cup.com/yui/chat/free/Bot/bottool.html">�������</A>�g�����̐���������܂��B
<H5 ALIGN=right>�ァ�ڂ��Ƃ�[�Ă���Ă�  Ver.1.0</H5>
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
if($mode eq 'del1'){#�L�[���[�h�폜
	$keyword = $key;
}elsif($mode eq 'del2'){#�����폜
	$keyword = $res;
}elsif($mode eq 'del3'){#�ԍ��폜
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
	push(@ans,"$messege\n") ; #�c�����X�g
}else{
	push(@dels,"$messege ($i)<BR>") ; #�폜���X�g
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
