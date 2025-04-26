import streamlit as st
import pandas as pd
from main import main

# Set Streamlit app background to white
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: #f8f7e8;
#         color: #000000;
#         textcolor: #000000;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Streamlit app title
st.title("From Data to Dialogue: Unlocking Language for All")

# Add two tiles for user choice
st.header("Choose Input Method")
option = st.radio("Select one:", ("Upload a File", "Paste Your Text"))

if option == "Upload a File":
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

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Words")
            st.dataframe(results["top_original"])
            
            st.subheader("Lemmatized Words")
            st.dataframe(results["top_lemmatized"])

            st.subheader("95% SWL")
            st.dataframe(results["top_swl"])

        with col2:
            st.subheader("95% SWL (No Stopwords)")
            st.dataframe(results["top_swl_no_stopwords"])

            st.subheader("95% SWL (No Proper Nouns)")
            st.dataframe(results["top_swl_no_proper_nouns"])

        # Clean up the temporary file
        import os
        os.remove(file_path)

elif option == "Paste Your Text":
    # Add a text area for user input
    st.subheader("Or Paste Your Text Below")
    user_text = st.text_area("Paste your text here:")

    if user_text:
        # Save the user input as a temporary text file
        file_path = "temp_user_input.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(user_text)

        # Process the file using main.py
        results = main(file_path)

        # Display the results
        st.header("Top 10 Words")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Words")
            st.dataframe(results["top_original"])

            st.subheader("Lemmatized Words")
            st.dataframe(results["top_lemmatized"])

            st.subheader("95% SWL")
            st.dataframe(results["top_swl"])

        with col2:
            st.subheader("95% SWL (No Stopwords)")
            st.dataframe(results["top_swl_no_stopwords"])

            st.subheader("95% SWL (No Proper Nouns)")
            st.dataframe(results["top_swl_no_proper_nouns"])

        # Clean up the temporary file
        import os
        os.remove(file_path)