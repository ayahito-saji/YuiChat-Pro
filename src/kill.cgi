#! /usr/local/bin/perl

#アクセス制限ユーティティVer1.0
#97/3/19日作成...
#著作権はゆいちゃっとが所有しております。
#利用に当たっては、簡単なメール(yui@cup.com)とリンクをお願いしたいんですけどぉ...（笑）

#ユーティリティCGIの名前(kill.cgi)とパスワード名を以下で設定する。
#ホスト名登録ファイルkillfileの名前も
#必ず自分のオリジナルな名前に変更すること！！。
#
$host_file = './kill.dat';
$cgi='kill.cgi';#このCGIの名前
$passwd='vampire';
#$passwd2='vampire2';#いくつかのパスワードをつかうなら、#を外す..かなり下のとこも同様に外して有効にする。
#$passwd3='vampire3';
$clear='clearfile';#ホスト名のかわりに入力すると登録ファイルを初期化します。

&decode;
if($host){ &killhost;}
&html;
exit;

sub decode{
 @pairs = split(/&/,$ENV{'QUERY_STRING'});
   foreach $pair (@pairs)
   {
       ($name, $value) = split(/=/, $pair);
       $value =~ tr/+/ /;
       #$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
       $value =~ s/\n//g;
       $FORM{$name} = $value;
   }
   $pass = $FORM{'pass'};
   $host = $FORM{'host'};
}#decode end

sub html{
print "Content-type: text/html\n\n";
print <<"_HTML_";
<html><head><title>アクセス制限ゆーてぃりてぃ～</title></head>
<BODY BGCOLOR=#888888>
<form method="GET" action="$cgi">
<font size=4><b>アクセス制限ゆーてぃりてぃ～</b></font><br><br>
<font color=red>$messege</font><br>
<form method="get" action="$cgi">
パスワード:<input type=text name="pass" size="15"value="$pass"><br>
ホスト名:<input type=text name="host" size="30">
<input type=submit value="実行"><hr>
現在アクセス制限がかけられているのは以下の通りです。
_HTML_

open(DB,"$host_file") || die "Cannot Open Log File $host_file: $!";
	@lines = <DB>;
close(DB);
$num=@lines;
print "登録数：$num<br>";
   foreach $line (@lines) {
		print "$line<br>"
	}

print <<"_HTML_";
<hr>
<h5 align=right><a href="http://www.cup.com/yui/">YuiCHAT Security Systems.</a></h5></body></html>
_HTML_
}#html end

sub killhost{
	$messege='';
	$flag=0;
	$flag=1 if($passwd eq $pass);
#$flag=1 if($passwd2 eq $pass);#複数のパスワードをつかうなら、#を消す。
#$flag=1 if($passwd3 eq $pass);

if($flag){
	if($host ne $clear){
		open(DB,">>$host_file") || die "Cannot Open Log File $host_file: $!";
			print DB "$host\n";
		close(DB);
		$messege="$hostを追加しました。";
	}else{
		open(DB,">$host_file") || die "Cannot Open Log File $host_file: $!";
			close(DB);
		$messege="アクセス制限ファイルを初期化しました。";
	}
}else{
	$messege="$passは正しいパスワードではありませんでした。";
}

}#killhost end

__END__
