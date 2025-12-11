import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

import os
import random
import tensorflow as tf

#add seeds for reproducing results
os.environ["PYTHONHASHSEED"] = "0"
random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)

#contains the Kaggle datasets used in project for building and testing ML model
data_files = ["emails.csv", "malicious_phish.csv", "phishing_site_urls.csv", "spam.csv"]

#the datasets all have different column names, using this function to standardize column name
def identify_cols(df):
    text = [c for c in df.columns if any(x in c.lower() for x in ["text", "url", "message"])]
    label = [c for c in df.columns if any(x in c.lower() for x in ["spam", "type", "label", "category"])]
    return text[0], label[0]

#using the identify_cols method and dropping any na values
merged_frames = []
for f in data_files:
    temp = pd.read_csv(f)
    t, l = identify_cols(temp)
    part = temp[[t, l]].dropna()
    part.columns = ["text", "label"]
    merged_frames.append(part)
spam_dataset = pd.concat(merged_frames, ignore_index=True) #combining datasets into one dataframe

#normalizing label values in the datasets into binary (1 = spam, 0 = legit)
def convert_label_to_binary(original_label):
    original_label = str(original_label).strip().lower()
    if original_label in ["1", "spam", "phishing", "defacement", "malware", "bad"]:
        return 1
    if original_label in ["0", "ham", "benign", "good"]:
        return 0
    return np.nan

#cleaning and standardizing labels
spam_dataset["label"] = spam_dataset["label"].apply(convert_label_to_binary)
spam_dataset = spam_dataset.dropna(subset=["label"])
spam_dataset["label"] = spam_dataset["label"].astype(int)
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

#Preprocesses the text by converting string to lowercase,
#tokenizing, removing stopwords, ensuring only non alphabetical tokens are used
#and stemming is applied

def clean_text(input_text):
    input_text = str(input_text).lower()
    tokens = word_tokenize(input_text)
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(tokens)

#cleaning the data and dropping any non useful data
spam_dataset["cleaned_text"] = spam_dataset["text"].apply(clean_text)
spam_dataset = spam_dataset[spam_dataset["cleaned_text"].str.len() > 0]

#vectorizing text into a matrix of numbers (using bag of words vectorizer)
vectorizer = CountVectorizer(max_features=3000)
X = vectorizer.fit_transform(spam_dataset["cleaned_text"]).toarray() #X is the features
y = spam_dataset["label"].values #y is the labels

#splitting data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

#defining the neural network model, a feed forward neural network
model = Sequential() #defining the model type based on the task of text classification
#using 512 neurons for the input and first hidden layer
#relu is activation function
#need the model to know the size of each input vector, so decided to go with input_dim
model.add(Dense(512, activation="relu", input_dim=X_train.shape[1]))
model.add(Dropout(0.3)) #using dropout to reduce overfitting
model.add(Dense(256, activation="relu"))
model.add(Dropout(0.3))  #using dropout to reduce overfitting
model.add(Dense(1, activation="sigmoid")) #outputs the probablity of spam

#compiling the model. using Adam as the optimizer to adjust learning rate per parameter
#the loss function is binary_crossentropy and used as our project is trying
#to classify into two groups, spam or not
#using metrics to view report of accuracy of model
model.compile(optimizer=Adam(0.001), loss="binary_crossentropy", metrics=["accuracy"])

#train the model
print("Training the model:")
#having the model learn from the the train features and labels
#using 5 epoch so the run through of the entire training dataset is 5 times
#using batches of 32 for how much data the model will learn from at one time
#using 10% of data for validation
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.1, shuffle=False)
probs = model.predict(X_test)
preds = (probs > 0.5).astype(int).flatten()

#printing the performance using sklearn.metrics
print("\nModel performance:")
print(f"Accuracy: {accuracy_score(y_test, preds):.3f}")
print(classification_report(y_test, preds))

#saving the trained neural networks model and vectorizer
model.save("nn_model.keras")
joblib.dump(vectorizer, "vectorizer.pkl")
