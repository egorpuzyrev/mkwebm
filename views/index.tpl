<html>
    <head>
        <script>
            function check_form()
            {
                var image_file = document.getElementById("image_file").files[0]
                var audio_file = document.getElementById("audio_file").files[0]
                if(!image_file || !audio_file)
                {
                    alert("Выберите оба файла")
                    return false
                }

                var image_size = image_file.size/1024
                var audio_size = audio_file.size/1024

                if(image_size+audio_size>20480)
                {
                    alert("Суммарный размер файлов превышает допустимый!")
                    return false
                }

                return true
            }

            function update_image_size()
            {
                var image_file = document.getElementById("image_file").files[0]
                var image_size = image_file.size/1024
                document.getElementById("image_size_label").textContent = image_size
            }

            function update_audio_size()
            {
                var audio_file = document.getElementById("audio_file").files[0]
                var audio_size = audio_file.size/1024
                document.getElementById("audio_size_label").textContent = audio_size
            }

            function update_size()
            {
                var image_file = document.getElementById("image_file").files[0]
                if(image_file)
                {
                    var image_size = (image_file.size/1024).toFixed(1)
                }
                else
                {
                    var image_size = 0
                }

                document.getElementById("image_size_label").textContent = image_size


                var audio_file = document.getElementById("audio_file").files[0]
                if(audio_file)
                {
                    var audio_size = (audio_file.size/1024).toFixed(1)
                }
                else
                {
                    var audio_size = 0
                }

                document.getElementById("audio_size_label").textContent = audio_size


                document.getElementById("total_size_label").textContent = (image_size + audio_size).toFixed(1)
            }

        </script>
    </head>

    <body>
        <p><b> Суммарный объём двух файлов - 20480 Кб </b></p>
        <form method="POST" enctype="multipart/form-data" action="/mkwebm" name="upload" onsubmit="check_form()">
            <p> Image file: <input type="file" name="image_file" id="image_file" onchange="update_size()"> <span id="image_size_label">0</span> Kb </p>
            <p> Audio file: <input type="file" name="audio_file" id="audio_file" onchange="update_size()"> <span id="audio_size_label">0</span> Kb </p>
            <p> Total size: <span id="total_size_label">0</span> Kb  </p>
            <input type="submit" value="Send">
        </form>
    </body>
</html>
