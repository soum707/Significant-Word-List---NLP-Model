import streamlit as st
import pandas as pd
from main import main

# Streamlit app title
st.title("Text Analysis App")

# File uploader
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process the file using main.py
    results = main(file_path)

    # Display the results
    st.header("Top 10 Words")

    st.subheader("Original Words")
    st.dataframe(results["top_original"])

    st.subheader("Lemmatized Words")
    st.dataframe(results["top_lemmatized"])

    st.subheader("95% SWL")
    st.dataframe(results["top_swl"])

    st.subheader("95% SWL (No Stopwords)")
    st.dataframe(results["top_swl_no_stopwords"])

    st.subheader("95% SWL (No Proper Nouns)")
    st.dataframe(results["top_swl_no_proper_nouns"])

    # Clean up the temporary file
    import os
    os.remove(file_path)