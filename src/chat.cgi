#! /usr/local/bin/perl
#
#ゆいちゃっとPro1.0(chat.cgi)+ゅぃぼっと
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
	print "</HEAD>$body<A HREF=\"$link\">[リロード]</A>\n";
}else{#ノンフレームの発言欄ここから
&hide;
print <<"_HTML_";
</HEAD>$body<FORM METHOD="$method" ACTION="chat.cgi">
<FONT SIZE=+2 COLOR="hotpink"><B>$title</B></FONT>おなまえ:<B>$name</B>
$hiddenログ行数:$logw
$kao<BR>発言:<INPUT TYPE=text NAME="chat" SIZE="80">
<TABLE border=0><TR>
<TH><INPUT TYPE=submit VALUE="発言/リロード"></TH>
<TH><INPUT TYPE=reset VALUE="リセット"></TH></FORM>
<FORM METHOD="$method" ACTION="chat.cgi">
$hidden
<INPUT TYPE=hidden NAME="chat" VALUE="退室">
<TH><INPUT TYPE=submit VALUE="退室する"></TH></FORM>
<TH>(<A HREF="./index.html">変更</A>)</TH></TR></TABLE>
_HTML_
}#ノンフレームの発言欄ここまで

#参加者表示
$num = @sanka3+1;
print "<FONT SIZE=2>参加者($num)：";
print "@sanka3ゅぃ</FONT SIZE=2><HR>\n";
#ログ表示
&readlog if(!@lines);
(@lines < $window) || (@lines = @lines[0 .. $window - 1]);
print "@lines\n";
   print "<H5 ALIGN=right><A HREF=\"http://www.cup.com/yui/\">ゆいぼっと(Free)</A></H5></BODY></HTML>\n";#この行だけは消さないでっ！！

}#html END

sub get{
	$chat = $FORM{'chat'};
	$emoji = $FORM{'emoji'};$emoji =~ s/\t/&lt;/eg;
		$emoji = '(<FONT COLOR="red">=</FONT>＾＾<FONT COLOR="red">=</FONT>)' if($emoji eq '(=＾＾=)');
	$emoji ='' if($emoji =~/なし/);
	$reload = 30 if($reload!=0 && $reload<30);
	$reload = $reload+5 if($reload);#サーバ負荷を少しでも減らすため....
}#get END

sub write {
&tag if ($chat=~s/\t/</g);
	&readlog;
#commandXXXと発言すると、XXXを含む行を削除します。
#以下のcommandという単語は別のものに変えて下さい。
$chat = 'commandimg' if ($chat eq 'cut');
$chat = "command".$host if ($chat eq 'clear');
	if( $chat=~s/^command//){
		foreach $line (@lines) {
			$line = '' if( $line=~/$chat/i);
		}
		$chat = '♪〜';
	}
#学習
if ($chat =~ /(.*)===(.*)/) {#半角のイコール3個であることに注意。
       $key = $1;
$key='' if $key eq 'ゆい';
       $res = $2;
       if($key ne 'ゅぃ'){
       &kioku;$chat="...（ゅぃを教育）<hr><font color=\"hotpink\">ゅぃ</font>&gt;$key　には○○○（ぴぃ〜）と言えばよいのね。...めもめも";}
       }#学習
	if ($chat eq '退室') {
		$value = "<FONT COLOR=\"blue\"><B>管理人</B></FONT> &gt; <B><FONT COLOR=\"$color\" SIZE=+2>$name</FONT><FONT COLOR=\"red\">さん、またきておくれやすぅ。</FONT></B><FONT COLOR=\"#888888\" SIZE=-1>($date $host)</FONT><HR>\n";
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
$chat='' if($botf eq '2');#学習後はそれ以上反応させない。
if ($chat eq 'おみくじ') {&bot3;$chat='';}
if( $num == 2){ $chat.='＞ゅぃ' if($chat);	}#二人きりのときだけ、特別。
if($chat =~/(ゅぃ|ゆい)/){
$rnd=rand(1);
if( $rnd>0.11 ){
&bot;#辞書応答
}else{
&bot2;#つっこみ？
}
}
#bot
$value=shift( @lines);#writelogルーチンが、@linesに、$valueを加えて書き込むため...
&writelog;
$dmy=shift( @lines) if($botflag);#ボットの応答を遅らせる...（この行は削除可）

#botのための処理ここまで

}#write END

sub tag{	#このタグ閉じは、正しく閉じてある場合も余分に閉じます。（苦笑）
$chat =~ s/<pre//ig;$chat =~ s/<meta//ig;$chat =~ s/<body//ig;#禁止タグ設定
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
	$chat.='">タグえらー？</A>' if( ($chat=~/<A.*HREF/i) && !($chat=~/<A.*".*".*>.*<\/A>/i) );
	$chat =~ s/<a href=/<A target="_blank" href=/ig;
	$chat =~s/<.*(img|href).*on.*=/TagError?/ig;
}#tag END

__END__
