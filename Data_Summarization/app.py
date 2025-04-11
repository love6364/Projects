import streamlit as st
import requests

def summarize_text(text, max_length):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}
    
    min_length = max_length   # // 2
    response = requests.post(API_URL, headers=headers, json={
        "inputs": text,
        "parameters": {"min_length": min_length, "max_length": max_length}
    })
    
    result = response.json()
    return result[0]['summary_text'] if isinstance(result, list) else "Error in summarization"

# Streamlit UI
st.set_page_config(page_title="Data Summarization", layout="centered")
st.title("📄 Text Summarization")

text_input = st.text_area("Enter your text:", height=200)
max_length = st.slider("Select summary length:", 20, 300, 100)

if st.button("Summarize"):
    if text_input:
        summary = summarize_text(text_input, max_length)
        st.subheader("Summary:")
        st.success(summary)
    else:
        st.warning("Please enter some text to summarize.")
