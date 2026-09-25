var constraints = { audio: true };
var recorder, audioStream;

// Access the microphone and start recording
function startRecording() {
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        audioStream = stream;
        recorder = new MediaRecorder(stream);
        let chunks = [];
        recorder.ondataavailable = e => chunks.push(e.data);
        recorder.onstop = e => {
            var blob = new Blob(chunks, { 'type' : 'audio/wav; codecs=opus' });
            sendAudio(blob);
            chunks = [];
        };
        recorder.start();
        updateUI(true);
    }).catch(function(err) {
        console.log(err.name + ": " + err.message);
    });
}

// Stop recording
function stopRecording() {
    recorder.stop();
    audioStream.getTracks().forEach(track => track.stop());
    updateUI(false);
}

// Update UI during recording
function updateUI(isRecording) {
    document.getElementById("startRecord").disabled = isRecording;
    document.getElementById("stopRecord").disabled = !isRecording;
    document.getElementById("recordingStatus").textContent = isRecording ? "Recording..." : "Not Recording";
}

// Send the audio file to the server
function sendAudio(blob) {
    var formData = new FormData();
    formData.append("file", blob, "audio.wav");

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => {
        return response.text();
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
}

document.getElementById("startRecord").addEventListener("click", startRecording);
document.getElementById("stopRecord").addEventListener("click", stopRecording);
