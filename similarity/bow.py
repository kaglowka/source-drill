from wordfreq import word_frequency
from nltk.stem import WordNetLemmatizer
import skfuzzy as fuzz
import numpy as np
import pandas as pd


def get_length_penalty(sent_len):
    # 0.5 value for len=2
    # quickly raising to 1 at ~10 words
    return fuzz.sigmf(sent_len, 2, 0.5)

def get_word_itf(string_tokens):
    min_val = 10e-7
    return [1./max(min_val, word_frequency(token, 'en')) for token in string_tokens]

def transform_tokens(string_tokens, lemmatizer):
    return [lemmatizer.lemmatize(token.lower()) for token in string_tokens]

def bow_score(link, name):
    """
    Score using term frequency
    """
    lemmatizer = WordNetLemmatizer()
    scores = []
    s = link.citing_context_part
    s_tokens = [token.text for token in s.tokens]
    context_token_set = set(transform_tokens(s_tokens, lemmatizer=lemmatizer))
    sentences = link.cited_text_parts
    for sentence in sentences:
        sent_tokens = [token.text for token in sentence.tokens]
        sent_token_set = set(transform_tokens(sent_tokens, lemmatizer))
        if len(sent_token_set) == 0:
            scores.append(0)
            continue
        matching_tokens = sent_token_set.intersection(context_token_set)
        all_tokens = sent_token_set.union(context_token_set)
        raw_score = np.sum(get_word_itf(matching_tokens)) / np.sum(get_word_itf(all_tokens))
        # Eliminate artifacts by penalizing extremely short matches
        raw_score *= get_length_penalty(len(sent_token_set))
        if np.isclose(raw_score, 0):
            score = 0.
        else:
            score = 1./-np.log(raw_score)
        scores.append(score)
    return pd.DataFrame({
        name: scores
    }, index=[sent.to_plain_string() for sent in sentences])

