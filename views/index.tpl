<html>
    <head>
        <meta charset="utf-8">
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

                if(image_size+audio_size>30720)
                {
                    alert("Суммарный размер файлов превышает допустимый!")
                    return false
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


                var audio_file = document.getElementById("audio_file").files[0]
                if(audio_file)
                {
                    var audio_size = audio_file.size/1024
                }
                else
                {
                    var audio_size = 0
                }

                document.getElementById("audio_size_label").textContent = audio_size.toFixed(1)

                var total_size = image_size + audio_size

                document.getElementById("total_size_label").textContent = total_size.toFixed(1)

                if(total_size>30720)
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
        <p><b> Суммарный объём двух файлов не более 30720 Кб </b></p>
        <p>Готовые файлы хранятся <s>сутки</s> двое суток.</p>
        <p>По окончании конвертации редирект на готовый файл происходит автоматически, нужно только подождать.</p>
        <p>Гифки <s>временно не</s> поддерживаются, но конвертятся очень медленно, так что проще сделать это на своей пекею</p>
        <form method="POST" enctype="multipart/form-data" action="/mkwebm" name="upload" onsubmit="check_form()">
            <table>
                <tr>
                    <td> <p> Image file: <input type="file" accept="image/*" name="image_file" id="image_file" onchange="update_size()"></p> </td>
                    <td align="right"> <p> <span id="image_size_label">0</span> Kb </p> </td>
                </tr>
                <tr>
                    <td> <p> Audio file: <input type="file" accept="audio/*" name="audio_file" id="audio_file" onchange="update_size()"></p> </td>
                    <td align="right"> <p> <span id="audio_size_label">0</span> Kb </p> </td>
                </tr>
                <tr>
                    <td> <p> Video width (1-800): <input type="number" min=1 max=800 value=400 style="width: 50px" name="image_width" id="image_width"> px </p> </td>
                    <td align="right"> <p> Total size: <span id="total_size_label">0</span> Kb </p> </td>
                </tr>
            </table>

            <input type="submit" value="Send">
        </form>
        <p> <a href="/webmslist"> List of converted webms </a> </p>
        <p style="color:grey;font-size:13"> {{mkwebm_views_counter}} webms converted</p>

        <p style="color:grey;font-size:13">
        Mailto: <a href="http://www.google.com/recaptcha/mailhide/d?k=01aPI0I1xx0AQ7rIxpelUAiQ==&amp;c=uY6EgEIYyg4kDoIk2nj1hHOzwrtWVgLoptKAAocYM_k=" onclick="window.open('http://www.google.com/recaptcha/mailhide/d?k\x3d01aPI0I1xx0AQ7rIxpelUAiQ\x3d\x3d\x26c\x3duY6EgEIYyg4kDoIk2nj1hHOzwrtWVgLoptKAAocYM_k\x3d', '', 'toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=0,width=500,height=300'); return false;" title="Reveal this e-mail address">e...</a>@mail.ru
        </p>

    </body>
</html>
