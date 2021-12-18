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
    document.getElementById('wer-output').innerHTML = "No voice was detected! Please try again."
}

function getWER(hypothesis) {
    var e = document.getElementById("sentences");
    var my_sentence = e.options[e.selectedIndex].text;
    let postData = {
        reference: my_sentence,
        hypothesis: hypothesis
    };
    fetch('/wer', {method: "POST", body: JSON.stringify(postData)}).then(response => response.text().then(text => {
        document.getElementById('wer-output').innerHTML = text;
    }));
}

function stopRecording() {
    // stop recording
    
    audioRecorder.stop();
    document.getElementById('stop').disabled = true;
    document.getElementById('start').removeAttribute('disabled');
    audioRecorder.getBuffers(gotBuffers);
}

function startRecording() {

    // start recording
    if (!audioRecorder)
        return;
    document.getElementById('start').disabled = true;
    document.getElementById('stop').removeAttribute('disabled');
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
