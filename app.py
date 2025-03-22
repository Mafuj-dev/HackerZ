from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import pickle
import openai  # Optional for GPT-based chatbot

# Initialize Flask App
app = Flask(__name__)
socketio = SocketIO(app)

# Load Trained NLP Chatbot Model
with open("chatbot_model.pkl", "rb") as file:
    vectorizer, model = pickle.load(file)

# Load Symptom Checker AI Model
with open("symptom_checker.pkl", "rb") as file:
    symptom_vectorizer, symptom_model = pickle.load(file)

# OpenAI API Key (Optional)
openai.api_key = "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"  # Replace with your actual key

# -----------------------------------
# ROUTES
# -----------------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    # Use GPT API for better responses (Optional)
    if openai.api_key:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a medical assistant."},
                      {"role": "user", "content": user_input}]
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})

    # Use traditional NLP Model
    input_vector = vectorizer.transform([user_input])
    response = model.predict(input_vector)[0]
    return jsonify({"response": response})

@app.route("/check_symptoms", methods=["POST"])
def check_symptoms():
    user_symptoms = request.json["symptoms"]
    transformed_symptoms = symptom_vectorizer.transform([user_symptoms])
    disease_prediction = symptom_model.predict(transformed_symptoms)[0]
    return jsonify({"prediction": disease_prediction})

# -----------------------------------
# WebRTC Video Call Signaling
# -----------------------------------

@socketio.on("offer")
def handle_offer(data):
    socketio.emit("offer", data, broadcast=True)

@socketio.on("answer")
def handle_answer(data):
    socketio.emit("answer", data, broadcast=True)

@socketio.on("candidate")
def handle_candidate(data):
    socketio.emit("candidate", data, broadcast=True)

# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == "__main__":
    socketio.run(app, debug=True)
