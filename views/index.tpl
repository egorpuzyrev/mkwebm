<html>
    <head>
        <meta charset="utf-8">
        <script>
            function check_form()
            {
                update_size()
                var image_file = document.getElementById("image_file").files[0]
                // ~var audio_file = document.getElementById("audio_file").files[0]

                var audios_size = 0
                var audio_files = document.getElementById("audio_file").files
                for(var i=0; i<audio_files.length; i++) {
                    audios_size += audio_files[i].size
                }


                if(!image_file || !audio_files[0])
                {
                    alert("Выберите оба файла")
                    return false
                }

                var image_size = image_file.size/1024
                // ~var audio_size = audio_file.size/1024

                audios_size = audios_size/1024
                //if(image_size+audio_size>102400)
                if(image_size+audios_size>102400)
                {
                    alert("Суммарный размер файлов превышает допустимый!")
                    return false
                }

                if(audio_files.length==1) {
                    document.getElementById('files_send_form').action = "/mkwebm"
                } else {
                    document.getElementById('files_send_form').action = "/mkwebms"
                }

                return true
            }

            function update_size()
            {
                var image_file = document.getElementById("image_file").files[0]
                if(image_file)
                {
                    var image_size = image_file.size/1024
                }
                else
                {
                    var image_size = 0
                }

                document.getElementById("image_size_label").textContent = image_size.toFixed(1)


                // ~var audio_file = document.getElementById("audio_file").files[0]
                // ~if(audio_file)
                // ~{
                    // ~var audio_size = audio_file.size/1024
                // ~}
                // ~else
                // ~{
                    // ~var audio_size = 0
                // ~}

                var audio_files = document.getElementById("audio_file").files
                var audios_size = 0
                for(var i=0; i<audio_files.length; i++) {
                    audios_size += audio_files[i].size
                }
                audios_size = audios_size/1024

                // ~document.getElementById("audio_size_label").textContent = audio_size.toFixed(1)
                document.getElementById("audio_size_label").textContent = audios_size.toFixed(1)

                // ~var total_size = image_size + audio_size
                var total_size = image_size + audios_size
                document.getElementById("total_size_kb").value = total_size

                document.getElementById("total_size_label").textContent = total_size.toFixed(1)

                if(total_size>102400)
                {
                    document.getElementById("total_size_label").style.color = 'red'
                } else
                {
                    document.getElementById("total_size_label").style.color = 'black'
                }
            }

        </script>
    </head>

    <body>
        <p><b> Суммарный объём <s>двух</s> всех файлов не более 102400 Кб (100 Мб)</b></p>
        <p>Готовые файлы хранятся <s>сутки</s> <s>двое суток</s> пока не закончится место.</p>
        <p>Если был выбран один аудиофайл, то по окончании конвертации редирект на готовую вебмку происходит автоматически, нужно только подождать.</p>
        <p>Гифки <s>временно не</s> поддерживаются, но конвертятся очень медленно, так что проще сделать это на своей пекею</p>
        <p>UPD: Теперь можно выбирать сразу несколько аудиофайлов (1 картинка будет лепиться на все вебмки).</p>
        <form method="POST" enctype="multipart/form-data" name="upload" onsubmit="check_form()" id="files_send_form">
            <table>
                <tr>
                    <td> <p> Image file: <input type="file" accept="image/*" name="image_file" id="image_file" onchange="update_size()"></p> </td>
                    <td align="right"> <p> <span id="image_size_label">0</span> Kb </p> </td>
                </tr>
                <tr>
                    <td> <p> Audio file: <input type="file" accept="audio/*" name="audio_file" id="audio_file" onchange="update_size()" multiple /></p> </td>
                    <td align="right"> <p> <span id="audio_size_label">0</span> Kb </p> </td>
                </tr>
                <tr>
                    <td> <p> Video width (1-800): <input type="number" min=1 max=800 value=400 style="width: 50px" name="image_width" id="image_width"> px </p> </td>
                    <td align="right"> <p> Total size: <span id="total_size_label">0</span> Kb </p> </td>
                </tr>
            </table>
            <input type="hidden" name="total_size_kb" id="total_size_kb" value="">
            <input type="submit" value="Send">
        </form>
        <p> <a href="/webmslist"> List of converted webms </a> </p>
        <p style="color:grey;font-size:13"> {{mkwebm_views_counter}} webms converted</p>

        <p style="color:grey;font-size:13">
        Mailto: <a href="http://www.google.com/recaptcha/mailhide/d?k=01aPI0I1xx0AQ7rIxpelUAiQ==&amp;c=uY6EgEIYyg4kDoIk2nj1hHOzwrtWVgLoptKAAocYM_k=" onclick="window.open('http://www.google.com/recaptcha/mailhide/d?k\x3d01aPI0I1xx0AQ7rIxpelUAiQ\x3d\x3d\x26c\x3duY6EgEIYyg4kDoIk2nj1hHOzwrtWVgLoptKAAocYM_k\x3d', '', 'toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=0,width=500,height=300'); return false;" title="Reveal this e-mail address">e...</a>@mail.ru
        </p>

    </body>
</html>
