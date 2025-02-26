<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube to MP3 Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        input, button {
            margin: 10px;
            padding: 10px;
            font-size: 16px;
        }
    </style>
</head>
<body>

    <h1>YouTube to MP3 Converter</h1>
    <input type="text" id="youtubeUrl" placeholder="Enter YouTube Video URL">
    <button onclick="convertVideo()">Convert to MP3</button>

    <p id="message"></p>

    <script>
        function convertVideo() {
            let url = document.getElementById("youtubeUrl").value;
            let formData = new FormData();
            formData.append("url", url);

            fetch("/convert", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById("message").innerHTML = 
                        `<a href="${data.download_url}" download>Download MP3</a>`;
                } else {
                    document.getElementById("message").innerText = "Error: " + data.error;
                }
            })
            .catch(error => {
                document.getElementById("message").innerText = "Error: " + error;
            });
        }
    </script>

</body>
</html>
