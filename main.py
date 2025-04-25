# Loading necessary libraries


import numpy as np
import pandas as pd
import nltk
import spacy
import stanza
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import warnings
warnings.filterwarnings(action="ignore")
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

stanza.download('en')
nlp1 = spacy.load("en_core_web_sm")
nlp2 = stanza.Pipeline(lang='en', processors='tokenize,pos')

# Functions

def load_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        src = file.read()
        src = src.replace("\n", " ")
    return src
def tokenize_text(text):
    tokens = [[j.lower() for j in word_tokenize(i)] for i in sent_tokenize(text)]

    words = []
    for sentence in tokens:
        words.extend(sentence)
    return words
def generate_frequncy_df(words):
    text_counts = pd.DataFrame({'word': words})
    text_counts = text_counts.groupby('word')['word'].count().reset_index(name='count')
    text_counts = text_counts.sort_values(by='count', ascending=False)
    text_counts = text_counts[text_counts['word'].str.isalpha()].reset_index(drop=True)
    return text_counts
def lemmatize(df):
    lemma_freq = {}
    for _, row in df.iterrows():
        word = row['word']
        count = row['count']
        doc = nlp1(word)
        token = doc[0]
        if token.like_num:
            continue
        lemma = token.lemma_
        lemma_freq[lemma] = lemma_freq.get(lemma, 0) + count

    grouped_df = pd.DataFrame(list(lemma_freq.items()), columns=['word', 'count'])
    grouped_df = grouped_df.sort_values(by='count', ascending=False).reset_index(drop=True)

    return grouped_df
def get_swl(df, coverage: float = 0.95):
    if not 0.0 <= coverage <= 1.0:
        raise ValueError("`coverage` must be between 0.0 and 1.0")
    
    df = df.copy()
    df['cumulative_coverage'] = df['count'].cumsum() / df['count'].sum()
    swl = df[df['cumulative_coverage'] <= coverage]
    return swl
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    mod_text = (
        text[~text['word'].isin(stop_words)]
        .reset_index(drop=True)
    )
    return mod_text
def remove_proper_nouns(df):
    drops = []
    for i, txt in df['word'].items():
        doc = nlp2(txt)
        if any(word.upos == 'PROPN' for sent in doc.sentences for word in sent.words):
            drops.append(i)
    return df.drop(drops).reset_index(drop=True)
def coverage(new_series, original_series):
    new_sum = new_series.sum()
    original_sum = original_series.sum()
    coverage = (new_sum / original_sum) * 100
    return print("Coverage: ", coverage, "%")

def get_lemmatized_swl(file_path):
    # Load the text file
    text = load_text_file(file_path)

    # Tokenize the text
    tokens = tokenize_text(text)

    # Generate frequency DataFrame
    freq_df = generate_frequncy_df(tokens)

    # Lemmatize the words
    lemmatized_df = lemmatize(freq_df)
    
    return lemmatized_df
def get_95_swl(lemmatized_df, 
               remove_sw: bool = False, 
               remove_pn: bool = False):
    
    # Get the 95% SWL
    swl = get_swl(lemmatized_df)
    
    # Remove stopwords
    if remove_sw:
        swl = remove_stopwords(swl)

    # Remove proper nouns
    if remove_pn:
        swl = remove_proper_nouns(swl)
    
    return swl
def compare_ngsl_lemmatized(lemmatized_df):
    ngsl = pd.read_csv(r"data/ngsl-v1.2.csv")
    ngsl.rename(columns={'Adjusted Frequency per Million (U)': 'count', 'Lemma': 'word'}, inplace=True)

    common_df = pd.merge(
    ngsl, lemmatized_df,
    on='word',
    how='inner',
    suffixes=('_ngsl', '_df')
    )

    coverage = float((common_df['count_df'].sum() / lemmatized_df['count'].sum())* 100)
    print(f"Coverage of NGSL in lemmatized SWL: {coverage:.2f}%")
    return coverage
def compare_nawl_lemmatized(lemmatized_df):
    nawl = pd.read_csv(r"data/NAWL-1.0.csv")
    nawl.rename(columns={'Word': 'word', 'U': 'count'}, inplace=True)

    common_df = pd.merge(
    nawl, lemmatized_df,
    on='word',
    how='inner',
    suffixes=('_nawl', '_df')
    )

    coverage = float((common_df['count_df'].sum() / lemmatized_df['count'].sum())* 100)
    print(f"Coverage of NAWL in lemmatized SWL: {coverage:.2f}%")
    return coverage

def main():
    file_path = input("Enter the path to the text file: ")
    lemmatized_df = get_lemmatized_swl(file_path)
    swl = get_95_swl(lemmatized_df)
    coverage(swl, lemmatized_df)
    compare_ngsl_lemmatized(lemmatized_df)

if __name__ == "__main__":
    main()
