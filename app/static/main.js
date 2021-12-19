window.AudioContext = window.AudioContext || window.webkitAudioContext;

var audioContext = new AudioContext();
var audioInput = null,
realAudioInput = null,
inputPoint = null,
audioRecorder = null;

function gotBuffers(buffers) {
    audioRecorder.exportMonoWAV(doneEncoding);
}

function doneEncoding(soundBlob) {
    fetch('/audio', {method: "POST", body: soundBlob}).then(response => response.text().then(text => {
        if (text == "ERR"){
            WERerror();
        }
        else{
            getWER(text);
        };
    }));
}

function WERerror(){
    document.getElementById('wer-output').innerHTML = '<div class="extra-space">No voice was detected! Please try again.</div>';
}

function getWER(hypothesis) {
    // Get reference sentence from page
    var e = document.getElementById("sentences");
    var my_sentence = e.options[e.selectedIndex].text;
    // Post reference and hypothesis to Flask API
    let postData = {
        reference: my_sentence,
        hypothesis: hypothesis
    };
    fetch('/wer', {method: "POST", body: JSON.stringify(postData)}).then(response => response.text().then(text => {
        // Parse JSON response
        werOutput = JSON.parse(text).html
        document.getElementById('wer-output').innerHTML = werOutput;
        levenshteinMatrix = JSON.parse(text).levenshtein
        document.getElementById('levenshtein-matrix').innerHTML = levenshteinMatrix;
    }));
}

function stopRecording() {
    // Stop recording
    audioRecorder.stop();
    // Toggle buttons
    document.getElementById('stop').disabled = true;
    document.getElementById('start').removeAttribute('disabled');
    // Store recorded audio
    audioRecorder.getBuffers(gotBuffers);
}

function startRecording() {
    if (!audioRecorder)
        return;
    // Toggle buttons
    document.getElementById('start').disabled = true;
    document.getElementById('stop').removeAttribute('disabled');
    // Clear WER info
    document.getElementById('wer-output').innerHTML = '';
    // Start recording
    audioRecorder.clear();
    audioRecorder.record();
}

function gotStream(stream) {
    document.getElementById('start').removeAttribute('disabled');

    inputPoint = audioContext.createGain();

    // Create an audio node from the stream.
    realAudioInput = audioContext.createMediaStreamSource(stream);
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    inputPoint.connect(analyserNode);

    audioRecorder = new Recorder(inputPoint);

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect(zeroGain);
    zeroGain.connect(audioContext.destination);
}

function initAudio() {
    if (!navigator.getUserMedia)
        navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    if (!navigator.cancelAnimationFrame)
        navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
    if (!navigator.requestAnimationFrame)
        navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

    navigator.getUserMedia(
        {
            "audio": {
                "mandatory": {
                    "googEchoCancellation": "false",
                    "googAutoGainControl": "false",
                    "googNoiseSuppression": "false",
                    "googHighpassFilter": "false"
                },
                "optional": []
            },
        }, gotStream, function (e) {
            alert('Error getting audio');
            console.log(e);
        });
}

window.addEventListener('load', initAudio);

