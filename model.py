import pandas as pd
import nltk
import re
import pickle
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords

# Download necessary NLP data
nltk.download("stopwords")
nlp = spacy.load("en_core_web_sm")

# Sample medical dataset (Extend this for better accuracy)
data = {
    "text": [
        "What are the symptoms of COVID?",
        "Tell me about flu symptoms.",
        "How to book an appointment?",
        "I need a doctor consultation.",
        "Can I get a prescription online?",
        "What are the side effects of antibiotics?",
        "How do I manage diabetes?",
        "What is a healthy diet for hypertension?",
        "How can I check my blood pressure at home?",
        "I have a fever and cough, what should I do?",
        "Best exercises for back pain?",
        "Can stress cause heart problems?"
    ],
    "label": [
        "COVID symptoms",
        "Flu symptoms",
        "Booking appointment",
        "Doctor consultation",
        "Online prescription",
        "Antibiotic side effects",
        "Diabetes management",
        "Hypertension diet",
        "Blood pressure check",
        "Fever and cough advice",
        "Back pain exercises",
        "Heart disease and stress"
    ]
}

df = pd.DataFrame(data)

# 🔹 **Text Preprocessing Function**
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"\W", " ", text)  # Remove special characters
    text = " ".join([word for word in text.split() if word not in stopwords.words("english")])  # Remove stopwords
    return text

df["clean_text"] = df["text"].apply(preprocess_text)

# 🔹 **TF-IDF Vectorization**
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["clean_text"])
y = df["label"]

# 🔹 **Train a RandomForest Model**
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 🔹 **Save the Model & Vectorizer**
with open("chatbot_model.pkl", "wb") as file:
    pickle.dump((vectorizer, model), file)

print("✅ Enhanced AI model trained and saved as 'chatbot_model.pkl'")
