#! /usr/local/bin/perl

#�E�F�u�`���b�g�p�{�b�g�X�N���v�gVer.3.1
#���쌠�͂䂢������Ƃ̂䂢�ɂ���܂��B
#
$bot_file = './yui.dat';#��{����
$non_file = './ago.dat';#�����o�^�Ȃ��̏ꍇ
$boke_file = './boke.dat';#������
$kuji_file = './kuji.dat';#���݂���
$bot ='�ァ';
1;#require�Ŏ�荞�ރt�@�C���ɂ͕K���K�v�Ȃӂ�����1

sub bot{
local (@ans);
open(DB,"$bot_file") || return;
while(<DB>){
($key,$res)=split(/:#/);
next if $key eq '';
$flag=0;$key=~s/\|/./g;
eval {	$flag=1 if $chat=~/.*$key.*/;	};
if($@ ne ''){
$flag=1 if (index($chat,$key) >= 0 );
}
push(@ans,$res) if $flag;
}#while
close(DB);
$pat=@ans;#�\�ȉ񓚃p�^�[������
if(@ans){
$res=$ans[rand($#ans+1)];
chop $res;
$res=~s/NAME/$name/g;
$value = "<B><FONT color=\"hotpink\">$bot</FONT></B> &gt; <B>$res $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)$pat</FONT><HR>\n";

&bot_w;
}elsif($chat=~/.*���ァ.*/){#�����ɂȂ��ꍇ

if(rand(1)>0.5){	#�����ă��[�h

$chat=~ s/(.*)��.*/$1/g;
$value = "<B><FONT color=\"hotpink\">$bot</FONT></B> &gt; <B>$chat���Ă����Ă��A�Ȃ�ē������炢���̂��킩��Ȃ��ł����B&gt; $name����B�i�Q�l�F<a href=\"http://www.cup.com/yui/edu.html\">������</a>�j $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)</FONT><HR>\n";

}else{	#���Ƃڂ����[�h(�����Ƃ͖��֌W�ȓ��e�����X)
open(DB,"$non_file") || return;
   @lines2 = <DB>;
   close(DB);
$msg= $lines2[rand($#lines2+1)];
chop $msg;
$value = "<B><FONT color=\"hotpink\">$bot</FONT></B> &gt; <B>$msg $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)</FONT><HR>\n";
}
&bot_w;
}#if-ans end

}#bot END

sub bot_w{
	unshift( @lines,$value);
	$botflag=1;
}#bot_w END

sub kioku{
  $key=~s/\.\.//g;  $key=~s/:#//g;
if(length($key) <4){
$key='�i�L�[���[�h���Z���̂œo�^�ł��܂���ł����B�j';
}elsif( $res ne '' ){
open(DB,">>$bot_file") || return;
print DB "$key:#$res\n";
close(DB);
}

$botf='2';
}#kioku END

sub bot2{	#�����݃{�b�g
open(DB,"$boke_file") || return;
   @lines2 = <DB>;
   close(DB);
$msg= $lines2[rand($#lines2+1)];
chop $msg;
$chat=~ s/(.*)��(.*)/$1/g;
$value = "<B><FONT color=\"hotpink\">$bot</FONT></B> &gt; <B>$chat....$msg.�B��$name���� $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)</FONT><HR>\n";

&bot_w;

}#bot2 END

sub bot3{	#���݂����{�b�g
open(DB,"$kuji_file")  || return;
   @lines2 = <DB>;
   close(DB);
$msg= $lines2[rand($#lines2+1)];
chop $msg;
$value = "<B><FONT color=\"hotpink\">$bot(�ޏ�)</FONT></B> &gt; <B>$msg��$name���� $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)</FONT><HR>\n";
&bot_w;
}#bot3 END
