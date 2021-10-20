#!/usr/bin/env python3

import nltk, string
try:
    s = set(nltk.corpus.words.words())
except LookupError:
    print("Installing NLTK's word corpus")
    nltk.download("words")
    s = set(nltk.corpus.words.words())

def is_english(msg, tol=0.5, max_words=10):
    """
    Compares the frequency of the first max_words words in NLTK's corpus
    of words. If the frequency is less than the tol, then reject, otherwise
    accept.
    Input:
        msg: The message that needs to be checked if in the English language
        tol: reject if frequency is less than tol, accept if else
        max_words: look only at this number of first words
    Output:
        Boolean: True if accepted in language,
                 False if not
    Runtime:
        O(n) plus O(msg.translate), n < max_words
        O(1) plus O(msg.translate), n >= max_words
    """
    global s
    msg = msg.translate(str.maketrans("","",string.punctuation))
    count = 0
    pmsg = msg.split()
    for word in pmsg:
        if word.lower() in s:
            count += 1

    print(count, len(pmsg))
    if count / len(pmsg) >= tol:
        return True
    return False

if __name__ == "__main__":
    test = "My name is Anmol Kapoor."
    print(f"Testing the following message: `{test}`")
    print("Is this message English?", is_english(test))
