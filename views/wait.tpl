<html>
    <head>

        <script type="text/javascript">

            var webm_file = "{{webm_file}}";

            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open('GET', webm_file, true);

            xmlhttp.onreadystatechange = function() {
              if (xmlhttp.readyState == 4) {
                if((xmlhttp.status == 200) || (xmlhttp.status == 0)) {
                   clearTimeout(t1);
                   document.location.href = "{{webm_file}}";
                   xmlhttp.send(null);
                }
              }
            };

            xmlhttp.send(null);

            var t1 = setTimeout(function(){ xmlhttp.open('GET', webm_file, true); xmlhttp.send(null);}, 30*1000)

        </script>

    </head>
    <body>
        Redirecting to {{webm_file}} Please wait
    </body>
</html>
