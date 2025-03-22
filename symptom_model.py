import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# 🔹 Sample dataset for symptom-based diagnosis (expand for better accuracy)
data = {
    "symptoms": [
        "fever cough headache",
        "chest pain shortness of breath",
        "nausea vomiting stomach pain",
        "joint pain swelling redness",
        "fatigue frequent urination thirst",
    ],
    "disease": [
        "Flu or Cold",
        "Heart Attack - Seek Emergency Care",
        "Food Poisoning",
        "Arthritis",
        "Diabetes"
    ]
}

df = pd.DataFrame(data)

# 🔹 **Text Vectorization (TF-IDF)**
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["symptoms"])
y = df["disease"]

# 🔹 **Train a RandomForest Model**
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 🔹 **Save Model & Vectorizer**
with open("symptom_checker.pkl", "wb") as file:
    pickle.dump((vectorizer, model), file)

print("✅ Symptom Checker AI Model Trained & Saved as 'symptom_checker.pkl'")
