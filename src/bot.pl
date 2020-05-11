#! /usr/local/bin/perl

#ウェブチャット用ボットスクリプトVer.3.1
#著作権はゆいちゃっとのゆいにあります。
#
$bot_file = './yui.dat';#基本辞書
$non_file = './ago.dat';#辞書登録なしの場合
$boke_file = './boke.dat';#つっこみ
$kuji_file = './kuji.dat';#おみくじ
$bot ='ゅぃ';
1;#requireで取り込むファイルには必ず必要なふしぎな1

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
$pat=@ans;#可能な回答パターン総数
if(@ans){
$res=$ans[rand($#ans+1)];
chop $res;
$res=~s/NAME/$name/g;
$value = "<B><FONT color=\"hotpink\">$bot</FONT></B> &gt; <B>$res $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)$pat</FONT><HR>\n";

&bot_w;
}elsif($chat=~/.*＞ゅぃ.*/){#辞書にない場合

if(rand(1)>0.5){	#教えてモード

$chat=~ s/(.*)＞.*/$1/g;
$value = "<B><FONT color=\"hotpink\">$bot</FONT></B> &gt; <B>$chatっていわれても、なんて答えたらいいのかわからないですぅ。&gt; $nameさん。（参考：<a href=\"http://www.cup.com/yui/edu.html\">教え方</a>） $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)</FONT><HR>\n";

}else{	#おとぼけモード(発言とは無関係な内容をレス)
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
$key='（キーワードが短いので登録できませんでした。）';
}elsif( $res ne '' ){
open(DB,">>$bot_file") || return;
print DB "$key:#$res\n";
close(DB);
}

$botf='2';
}#kioku END

sub bot2{	#つっこみボット
open(DB,"$boke_file") || return;
   @lines2 = <DB>;
   close(DB);
$msg= $lines2[rand($#lines2+1)];
chop $msg;
$chat=~ s/(.*)＞(.*)/$1/g;
$value = "<B><FONT color=\"hotpink\">$bot</FONT></B> &gt; <B>$chat....$msg.。＞$nameさん $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)</FONT><HR>\n";

&bot_w;

}#bot2 END

sub bot3{	#おみくじボット
open(DB,"$kuji_file")  || return;
   @lines2 = <DB>;
   close(DB);
$msg= $lines2[rand($#lines2+1)];
chop $msg;
$value = "<B><FONT color=\"hotpink\">$bot(巫女)</FONT></B> &gt; <B>$msg＞$nameさん $emoji</B><FONT color=\"#888888\" size=-1>($date yui.bot.com)</FONT><HR>\n";
&bot_w;
}#bot3 END
