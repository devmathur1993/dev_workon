<html>
    <script>
    function redirectToNewApp(userid,name,email,path,id){
        $.ajax({
        type: "POST",
        url: '/django_python_bridge/bridge_ajax.php',
        data: {userid:userid,
               username:name,
               email:email,
               func:'writeSession',
               path:path,
               xid:id}, 
        success:function(data) {
        //var host = window.location.hostname;
	var host = '127.0.0.1';        
	var protocol = window.location.protocol;
        var port = 8000;
        var path_link = protocol+"//"+host+":"+port+"/bridge/p="+data+"/";
        window.location.replace(path_link);
        }
    });
    }
    
</script>
    <body>
          <input type = 'hidden' onclick="opendjango()" value='open'>
     </body>
</html>
<?php



