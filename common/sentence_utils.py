#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
## Code adapted from:
##     Chastney, J., Cook, D., Ma, J., Melamed, T., 2019. Lab 1: Group Project.
##     CM50265: Machine Learning 2. University of Bath. Unpublished.
##
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

punctuation = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/',
               '\\', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|',
               '}', '~', '``', '\'\'', '’', '...', '--', 'gt', 'lt', 'amp', '”', '“']

contractions = {
    'ca': { "n't": 'not' },
    'can': { "'t": 'not' },
    'it': { "'s": 'is' },
    'is': { "n't": 'not' },
    'he': { "'s": 'is' },
    'she': { "'s": 'is' },
    'that': { "'s": 'is' },
    'i': { "'ll": 'will', "'d": 'would', "'m": 'am', "'ve": 'have' },
    'they': { "'ll": 'will', "'ve": 'have' },
    'what': { "'s": 'is' },
    'we': { "'re": 'are', "'ve": 'have', "'ll": 'will', "'d": 'had' },
    'you': { "'ll": 'will', "'re": 'are' },
    'let': { "'s": 'us' },
    'do': { "n't": 'not' },
    'have': { "n't": 'not' },
    'should': { "n't": 'not' },
    'does': { "n't": 'not' },
    'are': { "n't": 'not' },
    'was': { "n't": 'not' },
    'has': { "n't": 'not' },
    'wo': { "n't": 'not' }
}

english_stopwords = stopwords.words('english')
english_stopwords.append('u')    # Add additional stopword that is common for 'you' in tweets
english_stopwords.append('would')
english_stopwords.append('could')
english_stopwords.append('you')
english_stopwords.append('us')
lemmatizer = WordNetLemmatizer()

def remove_stop_words_and_lemmatize(text, lowercase = True, lemmatize = True, keep_nouns_only=False):
    """
    Given a string, tokenises the string based on punctuation and whitespace, lowercases
    all tokens if lowercase is True and lemmatizes if lemmatize is True.
    Stopwords and punctuation are also removed as well as phrases split with a slash expanded.
        
    :returns: a string with the separate tokens joined back up with a space between them.
    """
    tokens = []
    
    if keep_nouns_only:
        pos_tags = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
        # Only keep adjectives and nouns
        tokens = [word for sent in pos_tags for word, tag in sent if tag in set(['NN', 'NNS', 'NNP', 'NNPS', 'JJ'])]
    else:
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

    updated_tokens = []
    
    prev_word = None
    
    for word in tokens:
        # Remove case
        if lowercase:
            word = word.lower()
        
        # To remove punctuation
        if word in punctuation:
            prev_word = word.lower()
            continue
            
        # Expand contractions
        word_to_test = word.lower()
        if word_to_test == 'wo' or word_to_test == 'ca':
            prev_word = word_to_test
            continue
        if prev_word in contractions and word_to_test in contractions[prev_word]:
            if prev_word == 'wo':
                updated_tokens.append('will')
            elif prev_word == 'ca':
                updated_tokens.append('can')
            word = contractions[prev_word][word.lower()]

        # NLTK does not appear to remove leading single quotes so manually do this
        # unless indicating pluralisation
        if word.startswith('\'') and not word.startswith('\'s'):
            word = word[1:]
        
        # Quite often similar words are separated with a slash, e.g. iphone/android
        # Split these terms into separate words
        words = word.split('/')
        if len(words) > 1:
            perform_split = True
            
            # Only split if all found strings are non empty and do not contain a number
            for found_word in words:
                if not found_word:
                    perform_split = False
                    break
                if any(char.isdigit() for char in found_word):
                    perform_split = False
                    break
            
            if perform_split:
                for found_word in words:
                    if found_word.lower() not in english_stopwords and found_word.lower() != '\'s':
                        updated_tokens.append(lemmatizer.lemmatize(found_word))
                prev_word = None
                continue

        # Add the updated token
        if word.lower() not in english_stopwords and word.lower() != '\'s':
            # Additional check to ensure U.S. is not lemmatised to U
            if lemmatize and word != 'US':
                word = lemmatizer.lemmatize(word)
            updated_tokens.append(word)
        prev_word = word.lower()
                     
    return ' '.join(updated_tokens)


def lowercase_all_capital_words(text):
    """
    Lowercase words in all caps only with length >1 character.  All uppercase words in tweets are common.
    
    :param text: string to convert.
    :returns: converted string.
    """
    # Set of words that should remain uppercase
    words_to_ignore = set(['UK', 'GB', 'EU', 'USA', 'POTUS', 'BBC', 'UN',
                           'ISIS', 'UKMO', 'GEFS', 'EXO', 'CNN', 'CBS', 'CBC'])
    
    tokens = text.split()
    updated_tokens = [token.lower() if (token.isupper() and len(token) > 1 and token not in words_to_ignore) 
                                    else token for token in tokens]
    
    return ' '.join(updated_tokens)
