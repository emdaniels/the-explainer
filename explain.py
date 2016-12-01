#! /usr/bin/env python
"""
Filename: explain.py
Author: Emily Daniels
Date: November 2016
Purpose: Augments text with the definitions of words not found
in the Basic English word list.
"""

import nltk
from nltk.corpus import wordnet

pos_to_define = ['JJ', 'JJS', 'JJR', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB',
                 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def tag_text(text):
    token_wordy_text = nltk.word_tokenize(text)
    return nltk.pos_tag(token_wordy_text)


def define_word(word, pos):
    top_def = ''
    synsets = wordnet.synsets(word, pos)
    if len(synsets) > 0:
        defined = synsets[0].definition()
        top_def = '\n(' + defined + ')\n'
    return top_def


def define_by_pos(tagged_wordy_text):
    basic_text = []
    definition = ''
    for word, pos in tagged_wordy_text[:]:
        for pos_def in pos_to_define:
            if pos == pos_def:
                if any(word in s for s in basic_english):
                    continue
                else:
                    if pos == 'JJ' or pos == 'JJS' or pos == 'JJR':
                        definition = define_word(word, 'a')
                    elif pos == 'NN' or pos == 'NNS':
                        definition = define_word(word, 'n')
                    elif pos == 'RB' or pos == 'RBR' or pos == 'RBS':
                        definition = define_word(word, 'r')
                    elif pos == 'VB' or pos == 'VBD' or pos == 'VBG' \
                            or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ':
                        definition = define_word(word, 'v')
        basic_text.append((word + ' ' + definition).encode('utf-8'))
        definition = ''
    return basic_text


def chunk_text(text, length):
    all_sent = []
    temp = ""
    for word in text:
        new_sent = word
        temp += new_sent
        if len(temp) >= length:
            all_sent.append(temp)
            temp = ""
    return all_sent


if __name__ == "__main__":
    with open("basicEnglish.txt", "rU") as f:
        basic_english = f.read().split('\n')

    with open("HeartofDarkness.txt", "rU") as f:
        wordy_text = f.read().decode('latin-1').encode('utf-8').decode('utf-8')

    basic_text = define_by_pos(tag_text(wordy_text))
    chunked_text = chunk_text(basic_text, 80)

    with open("HeartofDarkness_Explained.txt", "wb") as f:
        for sent in chunked_text:
            f.write(sent + "\n")
