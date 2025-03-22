// Function to analyze symptoms
function analyzeSymptoms() {
    const symptomInput = document.getElementById("symptomInput").value.trim();
    const response = document.getElementById("symptomResponse");

    if (symptomInput) {
        // Simulated AI response (you can replace this with an actual AI API)
        let analysis = "Symptoms analyzed. No serious conditions detected.";
        if (symptomInput.toLowerCase().includes("fever") || symptomInput.toLowerCase().includes("cough")) {
            analysis = "Possible flu or cold. Consult a doctor.";
        } else if (symptomInput.toLowerCase().includes("chest pain")) {
            analysis = "Chest pain detected. Seek medical help immediately.";
        }

        alert(analysis);
    } else {
        alert("Please enter your symptoms.");
    }
}

// Placeholder function for booking appointments
function bookAppointment() {
    alert("Redirecting to appointment booking...");
}

// Placeholder function for video consultation
function startVideoConsultation() {
    alert("Starting video consultation...");
}


let localStream;
let remoteStream;
let peerConnection;
const config = {
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
};

// Function to start video call
async function startCall() {
    document.getElementById("status").innerText = "Starting video call...";
    
    // Get user video/audio
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    document.getElementById("localVideo").srcObject = localStream;

    // Placeholder: Simulate a remote video (actual implementation needs WebRTC signaling)
    remoteStream = new MediaStream();
    document.getElementById("remoteVideo").srcObject = remoteStream;

    peerConnection = new RTCPeerConnection(config);
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

    peerConnection.ontrack = event => {
        event.streams[0].getTracks().forEach(track => remoteStream.addTrack(track));
    };

    document.getElementById("status").innerText = "Call in progress...";
}

// Function to end video call
function endCall() {
    document.getElementById("status").innerText = "Call ended.";
    if (peerConnection) peerConnection.close();
    if (localStream) localStream.getTracks().forEach(track => track.stop());
}

function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    
    if (userInput === "") {
        alert("Please enter a message.");
        return;
    }

    document.getElementById("chat-box").innerHTML += `<p><b>You:</b> ${userInput}</p>`;

    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("chat-box").innerHTML += `<p><b>AI:</b> ${data.response}</p>`;
    });

    document.getElementById("user-input").value = "";
}
