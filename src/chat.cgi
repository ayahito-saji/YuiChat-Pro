#! /usr/local/bin/perl
#
#�䂢�������Pro1.0(chat.cgi)+�ァ�ڂ���
#
require './jcodeLE.pl';
require './pref.cgi';
require './bot.pl';


$| = 1;
&init;
&decode;	&jikan;	srand($times);
&get; &sanka;	&write  if ($chat);
	&html;	&ended();	exit;

sub html {
$buffer =~s/&chat=.*&/&/;$buffer =~s/reload=[\d]*/reload=${reload}/;
$link = "./chat.cgi?${buffer}";
print "Content-type: text/html\n\n";
print "<HTML><HEAD><TITLE>$title</TITLE>\n";

if($mode eq 'checked' ){
	print "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"$reload;URL=$link\">\n" if($reload);
	print "</HEAD>$body<A HREF=\"$link\">[�����[�h]</A>\n";
}else{#�m���t���[���̔�������������
&hide;
print <<"_HTML_";
</HEAD>$body<FORM METHOD="$method" ACTION="chat.cgi">
<FONT SIZE=+2 COLOR="hotpink"><B>$title</B></FONT>���Ȃ܂�:<B>$name</B>
$hidden���O�s��:$logw
$kao<BR>����:<INPUT TYPE=text NAME="chat" SIZE="80">
<TABLE border=0><TR>
<TH><INPUT TYPE=submit VALUE="����/�����[�h"></TH>
<TH><INPUT TYPE=reset VALUE="���Z�b�g"></TH></FORM>
<FORM METHOD="$method" ACTION="chat.cgi">
$hidden
<INPUT TYPE=hidden NAME="chat" VALUE="�ގ�">
<TH><INPUT TYPE=submit VALUE="�ގ�����"></TH></FORM>
<TH>(<A HREF="./index.html">�ύX</A>)</TH></TR></TABLE>
_HTML_
}#�m���t���[���̔����������܂�

#�Q���ҕ\��
$num = @sanka3+1;
print "<FONT SIZE=2>�Q����($num)�F";
print "@sanka3�ァ</FONT SIZE=2><HR>\n";
#���O�\��
&readlog if(!@lines);
(@lines < $window) || (@lines = @lines[0 .. $window - 1]);
print "@lines\n";
   print "<H5 ALIGN=right><A HREF=\"http://www.cup.com/yui/\">�䂢�ڂ���(Free)</A></H5></BODY></HTML>\n";#���̍s�����͏����Ȃ��ł��I�I

}#html END

sub get{
	$chat = $FORM{'chat'};
	$emoji = $FORM{'emoji'};$emoji =~ s/\t/&lt;/eg;
		$emoji = '(<FONT COLOR="red">=</FONT>�O�O<FONT COLOR="red">=</FONT>)' if($emoji eq '(=�O�O=)');
	$emoji ='' if($emoji =~/�Ȃ�/);
	$reload = 30 if($reload!=0 && $reload<30);
	$reload = $reload+5 if($reload);#�T�[�o���ׂ������ł����炷����....
}#get END

sub write {
&tag if ($chat=~s/\t/</g);
	&readlog;
#commandXXX�Ɣ�������ƁAXXX���܂ލs���폜���܂��B
#�ȉ���command�Ƃ����P��͕ʂ̂��̂ɕς��ĉ������B
$chat = 'commandimg' if ($chat eq 'cut');
$chat = "command".$host if ($chat eq 'clear');
	if( $chat=~s/^command//){
		foreach $line (@lines) {
			$line = '' if( $line=~/$chat/i);
		}
		$chat = '��`';
	}
#�w�K
if ($chat =~ /(.*)===(.*)/) {#���p�̃C�R�[��3�ł��邱�Ƃɒ��ӁB
       $key = $1;
$key='' if $key eq '�䂢';
       $res = $2;
       if($key ne '�ァ'){
       &kioku;$chat="...�i�ァ������j<hr><font color=\"hotpink\">�ァ</font>&gt;$key�@�ɂ́������i�҂��`�j�ƌ����΂悢�̂ˁB...�߂��߂�";}
       }#�w�K
	if ($chat eq '�ގ�') {
		$value = "<FONT COLOR=\"blue\"><B>�Ǘ��l</B></FONT> &gt; <B><FONT COLOR=\"$color\" SIZE=+2>$name</FONT><FONT COLOR=\"red\">����A�܂����Ă�����₷���B</FONT></B><FONT COLOR=\"#888888\" SIZE=-1>($date $host)</FONT><HR>\n";
		&writelog;
		print "Location: $endpage\n\n";
		&ended;
	}elsif ($email) {
		$value = "<FONT COLOR=\"$color\"><B>$name</B></FONT> <A HREF=\"mailto:$email\" TARGET=\"_top\">|&gt;</A> <B>$chat $emoji</B><FONT COLOR=\"#888888\" SIZE=-1>($date $host)</FONT><HR>\n";
		}else {
			$value = "<FONT COLOR=\"$color\"><B>$name</B></FONT> &gt; <B>$chat $emoji</B><FONT COLOR=\"#888888\" SIZE=-1>($date $host)</FONT><HR>\n";
		}
	unshift( @lines,$value);
#bot
$chat='' if($botf eq '2');#�w�K��͂���ȏ㔽�������Ȃ��B
if ($chat eq '���݂���') {&bot3;$chat='';}
if( $num == 2){ $chat.='���ァ' if($chat);	}#��l����̂Ƃ������A���ʁB
if($chat =~/(�ァ|�䂢)/){
$rnd=rand(1);
if( $rnd>0.11 ){
&bot;#��������
}else{
&bot2;#�����݁H
}
}
#bot
$value=shift( @lines);#writelog���[�`�����A@lines�ɁA$value�������ď������ނ���...
&writelog;
$dmy=shift( @lines) if($botflag);#�{�b�g�̉�����x�点��...�i���̍s�͍폜�j

#bot�̂��߂̏��������܂�

}#write END

sub tag{	#���̃^�O���́A���������Ă���ꍇ���]���ɕ��܂��B�i��΁j
$chat =~ s/<pre//ig;$chat =~ s/<meta//ig;$chat =~ s/<body//ig;#�֎~�^�O�ݒ�
$chat =~ s/<applet//ig;$chat =~ s/<script//ig;$chat =~ s/<.*width//ig;
$chat =~ s/<noscript//ig;	$chat =~ s/<embed//ig;$chat =~ s/<.*height//ig;
$chat =~ s/<title//ig;	$chat =~ s/<!--//ig;$chat =~ s/<.*mailbox://ig;
$chat =~ s/<server//ig;$chat =~ s/<.*cols//ig;$chat =~ s/<.*rows//ig;
$chat =~ s/<plain//ig;$chat =~ s/<.*font-size//ig;$chat=~s/<img.*\?//ig;
	@tags = split( /</ ,  $chat ); $dmy = shift( @tags);
	foreach $tag ( @tags ){
		$tag =~s/([^>]*)>(.*)/$1/;
		$tag =~s/^\/(.*)//;
		$tag =~s/^([^\s]*).*/$1/;
	}
	$chat.='>' if($chat=~/<\/$/);
	@tags = reverse( @tags );
	foreach $tag ( @tags ){
		next if($tag =~/(img|^hr$|^br$)/i);
		$chat.="</$tag>" if($tag);
	}
	$chat.='">�^�O����[�H</A>' if( ($chat=~/<A.*HREF/i) && !($chat=~/<A.*".*".*>.*<\/A>/i) );
	$chat =~ s/<a href=/<A target="_blank" href=/ig;
	$chat =~s/<.*(img|href).*on.*=/TagError?/ig;
}#tag END

__END__
