import streamlit as st
import pandas as pd
from functions import main
import os
import io

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
    # Persist a quiz question until correctly answered
    if "quiz_title" not in st.session_state:
        # Sample excerpts for the quiz
        samples = {
            "Pride and Prejudice": (
                "Mr. Bennet was so odd a mixture of quick parts, sarcastic humour, reserve, and caprice, "
                "that the experience of three-and-twenty years had been insufficient to make his wife understand his character. "
                "Her mind was less difficult to develope. She was a woman of mean understanding, little information, and uncertain temper. "
                "When she was discontented, she fancied herself nervous. The business of her life was to get her daughters married: "
                "its solace was visiting and news."
            ),
            "The Great Gatsby": (
                "And as I sat there brooding on the old, unknown world, I thought of Gatsby’s "
                "wonder when he first picked out the green light at the end of Daisy’s dock. "
                "He had come a long way to this blue lawn, and his dream must have seemed so close "
                "that he could hardly fail to grasp it. He did not know that it was already behind him, "
                "somewhere back in that vast obscurity beyond the city, where the dark fields of the republic rolled on under the night"
            ),
            "1984": (
                "There was of course no way of knowing whether you were being watched at any given moment. "
                "How often, or on what system, the Thought Police plugged in on any individual wire was guesswork. "
                "It was even conceivable that they watched everybody all the time. But at any rate they could plug in your "
                "wire whenever they wanted to. You had to live — did live, from habit that became instinct — in the assumption "
                "that every sound you made was overheard, and, except in darkness, every movement scrutinized."
            )
        }
        # Generate a 95% word list for each full text in the repo
        wordlists = {}
        for t in samples:
            fp = os.path.join("data", f"{t}.txt")
            r = main(fp)
            wordlists[t] = set(r["swl"]["word"].str.lower())
        # Pick and store the next quiz question in sequence
        if "quiz_index" not in st.session_state:
            st.session_state.quiz_index = 0
        else:
            st.session_state.quiz_index = (st.session_state.quiz_index + 1) % len(samples)
        chosen_title = list(samples.keys())[st.session_state.quiz_index]
        chosen_paragraph = samples[chosen_title]
        st.session_state.quiz_title = chosen_title
        st.session_state.quiz_paragraph = chosen_paragraph
        st.session_state.quiz_wordlist = wordlists[chosen_title]

    # Retrieve persistent quiz state
    title = st.session_state.quiz_title
    paragraph = st.session_state.quiz_paragraph
    wordlist = st.session_state.quiz_wordlist

    # Blackout words from the excerpt
    def blackout(text, wl):
        return " ".join(
            "_____" if w.strip(".,;!?").lower() in wl else w
            for w in text.split()
        )
    st.markdown(blackout(paragraph, wordlist))

    # Multiple-choice options
    choices = ["Select one",
        "Pride and Prejudice",
        "The Great Gatsby",
        "1984"]
    
    guess = st.radio("Which work is this from?", choices)

    if guess != "Select one":
        if guess == title:
            st.success(f"Correct! It’s from *{title}*.")
            st.markdown(f"**Excerpt:** {paragraph}")
            # Offer a Next button to advance
            if st.button("Next"):
                # Advance quiz index
                st.session_state.quiz_index = (st.session_state.quiz_index + 1) % len(samples)
                # Update session state for the next question
                next_title = list(samples.keys())[st.session_state.quiz_index]
                st.session_state.quiz_title = next_title
                st.session_state.quiz_paragraph = samples[next_title]
                st.session_state.quiz_wordlist = wordlists[next_title]
                # Rerun the app to show the new quiz
                st.experimental_rerun()
        else:
            st.error("Sorry, that’s not it. Try again!")