<?php

        $mailid=$_POST['mailid'];
        $ip=$_SERVER['REMOTE_ADDR'];

        $log_file = fopen("/home/user/Desktop/result/result.txt", "a");
        fwrite($log_file, $mailid."|".date('Y/m/d H:i:s', time())."|".$ip."\r\n");
        fclose($log_file);

?>

<html>
<body>
<font size=6>This site is a training site for phishing attacks.<br><br>

Please contact the Information Security Department.
</font>

</body>
</html>


