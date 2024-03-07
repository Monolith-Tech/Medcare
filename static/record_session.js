// document.getElementById('startBtn').onclick = startRecording;
// document.getElementById('stopBtn').onclick = stopRecording;

// let mediaRecorder;
// let audioChunks = [];

// function startRecording() {
//     navigator.mediaDevices.getUserMedia({ audio: true })
//         .then(stream => {
//             mediaRecorder = new MediaRecorder(stream);
//             mediaRecorder.ondataavailable = event => {
//                 audioChunks.push(event.data);
//             };
//             mediaRecorder.start();
//             document.getElementById('startBtn').disabled = true;
//             document.getElementById('stopBtn').disabled = false;
//         });
// }

// function stopRecording() {
//     mediaRecorder.stop();
//     document.getElementById('startBtn').disabled = false;
//     document.getElementById('stopBtn').disabled = true;
//     mediaRecorder.onstop = async () => {
//         const fileName = prompt("Please enter the name for your audio file:", "MyRecording");
//         if (fileName) {
//             const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
//             const formData = new FormData();
//             formData.append("audio_file", audioBlob, fileName + ".wav"); // Append file with custom name
//             try {
//                 const response = await fetch("/submit_session", {
//                     method: "POST",
//                     body: formData,
//                     credentials: 'include' // Include credentials for session-based authentication
//                 });
//                 console.log(response);
//                 if (response.redirected) {
//                     window.location.href = response.url;
//                 }
//             } catch (error) {
//                 console.error('Error:', error);
//             }
//         } else {
//             // Handle the case where the user cancels the prompt or enters no name
//             console.log("No name entered for the audio file. Upload cancelled.");
//         }
//         audioChunks = [];
//     };
// }


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
            document.getElementById('statusMessage').style.display = 'block'; // Show recording message
        });
}

function stopRecording() {
    mediaRecorder.stop();
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('statusMessage').innerText = 'Generating SOAP...'; // Update message to indicate processing
    document.getElementById('statusMessage').style.display = 'block'; // Make sure the message is visible
    mediaRecorder.onstop = async () => {
        const fileName = prompt("Please enter the name for your audio file:", "MyRecording");
        if (fileName) {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append("audio_file", audioBlob, fileName + ".wav");
            try {
                const response = await fetch("/submit_session", {
                    method: "POST",
                    body: formData,
                    credentials: 'include'
                });
                console.log(response);
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    // Optionally, update or hide the status message once processing is complete or if you navigate the user elsewhere
                    document.getElementById('statusMessage').style.display = 'none'; // Hide the message after processing is complete
                }
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('statusMessage').style.display = 'none'; // Hide the message in case of error
            }
        } else {
            console.log("No name entered for the audio file. Upload cancelled.");
            document.getElementById('statusMessage').style.display = 'none'; // Hide the message if upload is cancelled
        }
        audioChunks = [];
    };
}
