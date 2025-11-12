from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

# Import modules for ML model
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

app = Flask(__name__)
CORS(app)

# Load model and related packages
model = joblib.load('model/model.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')

stops = set(stopwords.words('english'))
ps = PorterStemmer()


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.post('/analyze')
def analyze():
    email_content = request.get_json()

    # Clean text first
    def clean_text(text):
        text = str(text).lower()
        tokens = word_tokenize(text)
        tokens = [w for w in tokens if w.isalpha() and w not in stops]
        tokens = [ps.stem(w) for w in tokens]
        return " ".join(tokens)
    
    cleaned = clean_text(email_content)

    # Vectorize cleaned text
    v = vectorizer.transform([cleaned])
    print(model.predict(v)[0])

    # Returned % possibility that it is spam
    return jsonify({"success": True, "data": float(model.predict(v)[0])})


if __name__ == '__main__':
    app.run(debug=True)