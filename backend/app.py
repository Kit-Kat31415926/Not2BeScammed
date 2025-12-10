from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import random

# Import modules for ML model
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# Load model and related packages for spam detection
model = load_model('model/nn_model.keras')
vectorizer = joblib.load('model/vectorizer.pkl')

stops = set(stopwords.words('english'))
ps = PorterStemmer()

# Load dataset for simulation
df = pd.read_csv("test_emails.csv")
test_df = df[["text", "label"]].dropna()
test_df.columns = ["text", "label"]
# Split into ham and spam
ham_test_df = df[df["label"] == "Ham"]
spam_test_df = df[df["label"] == "Spam"]

ALLOWABLE_ERROR = 0.05


###################
#                 #
#  API Endpoints  #
#                 #
###################

@app.post('/analyze')
def analyze():
    email_content = request.get_json()
    prob = model_response(email_content)
    return jsonify({"success": True, "data": prob})

@app.post('/simulate')
def simulate():
    # Get arguments
    data = request.get_json()
    numSpam = int(data.get("spam"))
    numHam = int(data.get("ham"))

    # Get specified sample of each
    spam_emails = spam_test_df.sample(numSpam)
    ham_emails = spam_test_df.sample(numHam)

    # Feed to model random order
    total = spam_emails.shape[0] + ham_emails.shape[0]
    correct = 0

    while spam_emails.shape[0] > 0 and ham_emails.shape[0] > 0:
        # Choose random from each dataset to send
        if random.randint(0, 1) == 0:
            # Get spam to send
            text = spam_emails["text"].iloc[0]
            spam_emails = spam_emails.iloc[1:]

            if 1 - model_response(text) <= ALLOWABLE_ERROR:
                correct += 1
        else:
            # Get ham to send
            text = ham_emails["text"].iloc[0]
            ham_emails = ham_emails.iloc[1:]

            if model_response(text) <= ALLOWABLE_ERROR:
                correct += 1

    # Send remaining to model
    while spam_emails.shape[0] > 0:
        # Get spam to send
        text = spam_emails["text"].iloc[0]
        spam_emails = spam_emails.iloc[1:]
        if 1 - model_response(text) <= ALLOWABLE_ERROR:
            correct += 1

    while ham_emails.shape[0] > 0:
        # Get ham to send
        text = ham_emails["text"].iloc[0]
        ham_emails = ham_emails.iloc[1:]

        if model_response(text) <= ALLOWABLE_ERROR:
            correct += 1
        

    return jsonify({"success": True, "accuracy": f"Fisher got {correct} correct of {total}! Their accuracy rate is {round(correct / total, 2)}%"})


####################
#                  #
#  Helper methods  #
#                  #
####################

def model_response(email):
    # Clean text first
    def clean_text(text):
        text = str(text).lower()
        tokens = word_tokenize(text)
        tokens = [w for w in tokens if w.isalpha() and w not in stops]
        tokens = [ps.stem(w) for w in tokens]
        return " ".join(tokens)
    
    cleaned = clean_text(email)

    # Vectorize cleaned text
    v = vectorizer.transform([cleaned]).toarray()

    res = float(model.predict(v)[0][0])
    return res


if __name__ == '__main__':
    app.run(debug=True)
