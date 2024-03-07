document.getElementById('startBtn').onclick = startRecording;
document.getElementById('stopBtn').onclick = stopRecording;

let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.start();
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
        });
}

function stopRecording() {
    mediaRecorder.stop();
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    mediaRecorder.onstop = async () => {
        const fileName = prompt("Please enter the name for your audio file:", "MyRecording");
        if (fileName) {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append("audio_file", audioBlob, fileName + ".wav"); // Append file with custom name
            try {
                const response = await fetch("/submit_session", {
                    method: "POST",
                    body: formData,
                    credentials: 'include' // Include credentials for session-based authentication
                });
                console.log(response);
                if (response.redirected) {
                    window.location.href = response.url;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        } else {
            // Handle the case where the user cancels the prompt or enters no name
            console.log("No name entered for the audio file. Upload cancelled.");
        }
        audioChunks = [];
    };
}
