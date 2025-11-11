"""
Create model to detect spam
"""

import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

files = ["emails.csv", "malicious_phish.csv", "phishing_site_urls.csv", "spam.csv"]

def find_cols(df):
    text_col = [c for c in df.columns if any(k in c.lower() for k in ["text", "url", "message"])][0]
    label_col = [c for c in df.columns if any(k in c.lower() for k in ["spam", "type", "label", "category"])][0]
    return text_col, label_col

dfs = []
for f in files:
    df = pd.read_csv(f)
    text_col, label_col = find_cols(df)
    if text_col and label_col:
        temp = df[[text_col, label_col]].dropna()
        temp.columns = ["text", "label"]
        dfs.append(temp)

df = pd.concat(dfs, ignore_index=True)

def clean_label(x):
    x = str(x).strip().lower()
    if x in ["1", "spam", "phishing", "defacement", "malware", "bad"]:
        return 1
    if x in ["0", "ham", "benign", "good"]:
        return 0
    return np.nan

df['label'] = df['label'].apply(clean_label)
df = df.dropna(subset=['label'])
df['label'] = df['label'].astype(int)

stops = set(stopwords.words('english'))
ps = PorterStemmer()

def clean_text(text):
    text = str(text).lower()
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w.isalpha() and w not in stops]
    tokens = [ps.stem(w) for w in tokens]
    return " ".join(tokens)

df['clean'] = df['text'].apply(clean_text)
df = df[df['clean'].str.len() > 0]

vec = CountVectorizer(max_features=1000)
X = vec.fit_transform(df['clean']).toarray()
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)

print("\nDecision Tree:")
print(f"Accuracy: {accuracy_score(y_test, dt_pred):.3f}")
print(classification_report(y_test, dt_pred))

rf = RandomForestClassifier(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

print("\nRandom Forest:")
print(f"Accuracy: {accuracy_score(y_test, rf_pred):.3f}")
print(classification_report(y_test, rf_pred))

joblib.dump(rf, 'model.pkl')
joblib.dump(vec, 'vectorizer.pkl')

def check(text):
    cleaned = clean_text(text)
    v = vec.transform([cleaned])
    return "SPAM" if rf.predict(v)[0] == 1 else "LEGIT"
