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
    
    fetch('/save_audio', {method: "POST", body: soundBlob}).then(response => response.text().then(text => {
        if (text == "ERR"){
            displayError('Unable to save your recording! Please try again.');
        }
        else{
            displayText('Calculating WER. Please wait a moment...');
            // Get reference sentence from page
            var e = document.getElementById("sentences");
            var reference_sentence = e.options[e.selectedIndex].text;
            let postData = {
                reference: reference_sentence,
            };

            // Post reference sentence to Flask API and get HTML content back
            fetch('/get_wer', { method: "POST", body: JSON.stringify(postData) }).then(response => response.text().then(text => {

                // Parse JSON response
                response = JSON.parse(text)
                if ('error' in response){
                    displayError(response.error)
                }
                else{
                    displayWerInfo(response.html, response.levenshtein)
                }
            }));
        };
    }));
}

function displayWerInfo(werOutput, levenshteinMatrix){
    document.getElementById('wer-output').classList.remove("red-text");
    document.getElementById('wer-output').innerHTML = werOutput;
    document.getElementById('levenshtein-matrix').innerHTML = levenshteinMatrix;
}

function displayError(error){
    document.getElementById('wer-output').classList.add("red-text");
    document.getElementById('wer-output').innerHTML = `<div class="extra-space">${error}</div>`;
}

function displayText(message){
    document.getElementById('wer-output').classList.remove("red-text");
    document.getElementById('wer-output').innerHTML = `<div class="extra-space">${message}</div>`;
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
    // Need to resume audioContext in case this is the first user gesture since landing on the page
    // https://stackoverflow.com/questions/55026293/google-chrome-javascript-issue-in-getting-user-audio-the-audiocontext-was-not
    audioContext.resume();

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

