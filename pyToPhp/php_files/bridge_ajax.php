<?php

use \Firebase\JWT\JWT;
require __DIR__ . '/vendor/autoload.php';
//$mysqli = new mysqli("localhost","root","root","bridgedb");
mysql_connect('localhost','root','Sukh@9971');
mysql_select_db("bridgedb");


writeSession($_POST['path'],$_POST['xid']);

switch($_POST["func"]){ 

        case 'writeSession': 
            $r = writeSession($_POST['path'],$_POST['xid']);
            echo $r;
            break;      
}

function writeSession($path_to,$x_id){
    $jwtvar;
    $session_key = $_POST['userid'];
    
        $name = $_POST['username'];
        $email = $_POST['email'];

        $session_key = mysql_real_escape_string($session_key);
        $name = mysql_real_escape_string($name);
        $email = mysql_real_escape_string($email); 

        $sql = "SELECT PK_session_key FROM maintain_session WHERE PK_session_key = '$session_key'";
        $result = mysql_query($sql);
        $num = mysql_num_rows($result);
	
        if($num ==1){
            $sql = "UPDATE maintain_session
                    SET PK_session_key = '$session_key',
                        username = '$name',
                        useremail = '$email',
                        session_time = NOW(),
                        link_used = '1'
                    WHERE PK_session_key = '$session_key'";
        }else{
            $sql = "INSERT INTO maintain_session(PK_session_key, username, useremail, session_time,link_used)
                    VALUES('$session_key', '$name', '$email', NOW(),'1')";
        }
        
        mysql_query($sql);
        $jwtvar = make_JWT($session_key,$x_id,$path_to);
        return $jwtvar;
}

function make_JWT($uid,$x_id,$path_to){
    $currentTime = date('H:i:s');
    $key = "alskDJFHgqpwoeiRUTYVBCNmzx";
    $payload = array(
        "iss" => "localhost:80",
        "iat" => strtotime($currentTime),
        "exp" => $currentTime + strtotime("+1 minutes",strtotime($currentTime)) ,
        "path"=> $path_to,
        "uid" => $uid,
        "param"=> $x_id 
    );

    $jwt = JWT::encode($payload,$key);

    return $jwt;
 
   
}
