#! /usr/local/bin/perl

#�A�N�Z�X�������[�e�B�e�BVer1.0
#97/3/19���쐬...
#���쌠�͂䂢������Ƃ����L���Ă���܂��B
#���p�ɓ������ẮA�ȒP�ȃ��[��(yui@cup.com)�ƃ����N�����肢��������ł����ǂ�...�i�΁j

#���[�e�B���e�BCGI�̖��O(kill.cgi)�ƃp�X���[�h�����ȉ��Őݒ肷��B
#�z�X�g���o�^�t�@�C��killfile�̖��O��
#�K�������̃I���W�i���Ȗ��O�ɕύX���邱�ƁI�I�B
#
$host_file = './kill.dat';
$cgi='kill.cgi';#����CGI�̖��O
$passwd='vampire';
#$passwd2='vampire2';#�������̃p�X���[�h�������Ȃ�A#���O��..���Ȃ艺�̂Ƃ������l�ɊO���ėL���ɂ���B
#$passwd3='vampire3';
$clear='clearfile';#�z�X�g���̂����ɓ��͂���Ɠo�^�t�@�C�������������܂��B

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
<html><head><title>�A�N�Z�X������[�Ă���Ă��`</title></head>
<BODY BGCOLOR=#888888>
<form method="GET" action="$cgi">
<font size=4><b>�A�N�Z�X������[�Ă���Ă��`</b></font><br><br>
<font color=red>$messege</font><br>
<form method="get" action="$cgi">
�p�X���[�h:<input type=text name="pass" size="15"value="$pass"><br>
�z�X�g��:<input type=text name="host" size="30">
<input type=submit value="���s"><hr>
���݃A�N�Z�X�������������Ă���͈̂ȉ��̒ʂ�ł��B
_HTML_

open(DB,"$host_file") || die "Cannot Open Log File $host_file: $!";
	@lines = <DB>;
close(DB);
$num=@lines;
print "�o�^���F$num<br>";
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
#$flag=1 if($passwd2 eq $pass);#�����̃p�X���[�h�������Ȃ�A#�������B
#$flag=1 if($passwd3 eq $pass);

if($flag){
	if($host ne $clear){
		open(DB,">>$host_file") || die "Cannot Open Log File $host_file: $!";
			print DB "$host\n";
		close(DB);
		$messege="$host��ǉ����܂����B";
	}else{
		open(DB,">$host_file") || die "Cannot Open Log File $host_file: $!";
			close(DB);
		$messege="�A�N�Z�X�����t�@�C�������������܂����B";
	}
}else{
	$messege="$pass�͐������p�X���[�h�ł͂���܂���ł����B";
}

}#killhost end

__END__
