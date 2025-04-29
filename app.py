import streamlit as st
import pandas as pd
from functions import main
import os
import io
import random

def display_results(results):
    st.header("Top 10 Words in each Variation")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Words")
        st.text("Number of words in list: " + str(results["size_original"]))
        st.dataframe(results["top_original"])
        csv_original = results["original_words"].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Original Words as CSV",
            data=csv_original,
            file_name="original_words.csv",
            mime="text/csv"
        )
        
        # st.subheader("Lemmatized Words")
        # st.text("Number of words in list: " + str(results["size_lemmatized"]))
        # st.dataframe(results["top_lemmatized"])
        # csv_lemmatized = results["lemmatized_words"].to_csv(index=False).encode("utf-8")
        # st.download_button(
        #     label="Download Lemmatized Words as CSV",
        #     data=csv_lemmatized,
        #     file_name="lemmatized_words.csv",
        #     mime="text/csv"
        # )

        st.subheader("95% Word List (No Stopwords)")
        st.text("Number of words in list: " + str(results["size_swl_no_stopwords"]))
        st.dataframe(results["top_swl_no_stopwords"])
        csv_swl_no_stop = results["swl_no_stopwords"].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download 95% Word List (No Stopwords) as CSV",
            data=csv_swl_no_stop,
            file_name="word_list.csv",
            mime="text/csv"
        )
        

    with col2:
        st.subheader("95% Word List")
        st.text("Number of words in list: " + str(results["size_swl"]))
        st.dataframe(results["top_swl"])
        csv_swl = results["swl"].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download 95% Word List as CSV",
            data=csv_swl,
            file_name="word_list_nostopwords.csv",
            mime="text/csv"
        )

        # st.subheader("95% SWL (No Proper Nouns)")
        # st.text("Number of words in list: " + str(results["size_swl_no_proper_nouns"]))
        # st.dataframe(results["top_swl_no_proper_nouns"])
        # csv_swl_no_pn = results["swl_no_proper_nouns"].to_csv(index=False).encode("utf-8")
        # st.download_button(
        #     label="Download 95% SWL (No Proper Nouns) as CSV",
        #     data=csv_swl_no_pn,
        #     file_name="word_list_nopropernouns.csv",
        #     mime="text/csv"
        # )

# Streamlit app title
st.title("From Data to Dialogue: Unlocking Language for All")

st.markdown("""
    This web app transforms any text into a targeted word list optimized for language learning. Research shows that knowing the 95% most frequent words in a text dramatically improves comprehension, and our tool automates that process for you. Whether you’re a teacher, student, or lifelong learner, you can:<br>
    - Upload your own file, paste text directly, or choose from our curated classics<br>
    - Generate multiple word-list variants: original word frequencies, 95% SWL, and 95% SWL without stopwords<br>
    - Download each list as a CSV for easy integration with teaching materials, flash-card apps, or further analysis<br><br>
    Harness the power of literature—or any text you like—to build a custom vocabulary list in seconds.
""", unsafe_allow_html=True)


# Add two tiles for user choice
st.subheader("Choose Input Method")
option = st.radio("Select one:", (
    "Upload a File",
    "Paste Your Text",
    "Our Choices for You",
    "Play Guess the Literature"
))

if option == "Upload a File":
    # File uploader
    uploaded_file = st.file_uploader("Upload a text (.txt) file", type=["txt"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the file using main.py
        results = main(file_path)

        display_results(results)
        st.session_state["results"] = results

        # Clean up the temporary file
        os.remove(file_path)

elif option == "Paste Your Text":
    # Add a text area for user input
    st.subheader("Paste Your Text Below")
    user_text = st.text_area("Paste your text here:")

    if user_text:
        # Save the user input as a temporary text file
        file_path = "temp_user_input.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(user_text)

        # Process the file using main.py
        results = main(file_path)

        display_results(results)
        st.session_state["results"] = results

        # Clean up the temporary file
        os.remove(file_path)

elif option == "Our Choices for You":
    st.subheader("Select a Preloaded Text File")
    preloaded_files = ["Alice In Wonderland", "Lord of the Rings - Chapter One", "Titanic (Movie Script)", "The Catcher In The Rye", "The Great Gatsby", "1984", "Harry Potter And the Sorcerer’s Stone", "Snakes on a Plane (Movie Script)"]
    selected_file = st.selectbox("Select a file:", preloaded_files)
    if selected_file:
        file_path = "data/" + selected_file + ".txt"
        results = main(file_path)
        
        display_results(results)
        st.session_state["results"] = results

elif option == "Play Guess the Literature":
    st.subheader("Guess the Literature")

    # Define sample paragraphs
    samples = {
        "Pride and Prejudice": (
            "Elizabeth, as they drove along, watched for the first appearance of Pemberley Woods with some perturbation; "
            "and when at length they turned in at the lodge, her spirits were in a high flutter. The park was very large, "
            "and contained great variety of ground. They entered it in one of its lowest points, and drove for some time "
            "through a beautiful wood stretching over a wide extent. Elizabeth’s mind was too full for conversation, "
            "but she saw and admired every remarkable spot and point of view."
        ),
        "The Great Gatsby": (
            "In his blue gardens men and girls came and went like moths among the whisperings and the champagne and the stars. "
            "At high tide in the afternoon I watched his guests diving from the tower of his raft, or taking the sun on the hot sand "
            "of his beach while his two motor-boats slit the waters of the Sound, drawing aquaplanes over cataracts of foam."
        ),
        "1984": (
            "Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors "
            "of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him."
        )
    }
# Generate a 95% word list for each full text in the repo
wordlists = {}
for title in samples:
    file_path = os.path.join("data", f"{title}.txt")
    res = main(file_path)
    wordlists[title] = set(res["swl"]["word"].str.lower())
# Select a random excerpt
title, paragraph = random.choice(list(samples.items()))
# Blackout words based on that title's wordlist
def blackout(text, wordlist):
    return " ".join(
        "_____" if word.strip(".,;!?").lower() in wordlist else word
        for word in text.split()
    )
masked = blackout(paragraph, wordlists[title])
st.markdown(masked)
# Multiple-choice guessing
choices = random.sample(list(samples.keys()), k=len(samples))
guess = st.radio("Which work is this from?", ["Select one"] + choices)
if guess != "Select one":
    if guess == title:
        st.success(f"Correct! It’s from *{title}*.")
    else:
        st.error("Sorry, that’s not it. Try again!")