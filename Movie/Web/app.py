
import streamlit as st
import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords

# Load stopwords
nltk.download('stopwords')

# Text cleaning function
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    tokens = text.split()
    tokens = [w for w in tokens if w not in stopwords.words('english')]
    return ' '.join(tokens)

# Load the trained model
with open("G:\\Final_Projects\\NLP\\Project2\\Movie\\Model\\genre_classifier.pkl", "rb") as file:
    model = pickle.load(file)

# Streamlit UI
st.title("🎬 Movie Genre Classifier")
st.write("Enter a short movie description to predict its genre.")

user_input = st.text_area("Movie Overview")

if st.button("Predict Genre"):
    if user_input.strip():
        cleaned_input = clean_text(user_input)
        prediction = model.predict([cleaned_input])[0]
        st.success(f"Predicted Genre: **{prediction}**")
    else:
        st.warning("Please enter a movie overview.")
