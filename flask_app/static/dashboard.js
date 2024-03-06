document.getElementById('audio-file').onchange = function (e) {
    const file = e.target.files[0];
    if (!file) {
        return;
    }

    const formData = new FormData();
    formData.append('audio_file', file);

    // Show the progress bar
    const progressBar = document.getElementById('upload-progress');
    progressBar.hidden = false;
    progressBar.value = 0;

    fetch('/upload_audio', {
        method: 'POST',
        body: formData,
    }).then(response => {
        progressBar.value = 100; // Assuming the upload is done
        return response.text();
    }).then(result => {
        document.getElementById('upload-status').textContent = result;
        progressBar.hidden = true; // Hide progress bar after upload is complete
    }).catch(error => {
        console.error('Error:', error);
        document.getElementById('upload-status').textContent = 'Upload failed';
        progressBar.hidden = true;
    });
};



// document.getElementById('audio-file').onchange = function () {
//     document.getElementById('conversation-form').submit();
// };
