#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
## Code adapted (significantly, >60% new) from:
##     Chastney, J., Cook, D., Ma, J., Melamed, T., 2019. Lab 1: Group Project.
##     CM50265: Machine Learning 2. University of Bath. Unpublished.
##
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import nltk
import re

# Punctuation to remove
punctuation = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/',
               '\\', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|',
               '}', '~', '``', '\'\'', '’', '...', '--', 'gt', 'lt', 'amp', '”', '“']

# For expanding of contractions
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

# Setup stopwords
english_stopwords = stopwords.words('english')
english_stopwords.append('would')
english_stopwords.append('could')
english_stopwords.append('you')
english_stopwords.append('us')
lemmatizer = WordNetLemmatizer()


def wordnet_tag_from_penn_treebank(pos):
    """
    Given a Penn Treebank POS tag, converts it to a WordNet tag.
    
    :param pos: Penn Treebank POS tag.
    :returns: WordNet POS tag.
    """
    if pos.startswith('J'):
        return wordnet.ADJ
    elif pos.startswith('V'):
        return wordnet.VERB
    elif pos.startswith('N'):
        return wordnet.NOUN
    elif pos.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def remove_stop_words_and_lemmatize(text,
                                    lowercase = True,
                                    lemmatize = True,
                                    keep_nouns_only=False,
                                    simple_keep_nouns=False,
                                    eos_indicators=False):
    """
    Given a string, tokenises the string based on punctuation and whitespace, lowercases
    all tokens if lowercase is True and lemmatizes if lemmatize is True.
    Stopwords and punctuation are also removed as well as phrases split with a slash expanded.
    
    :param text: the text string to process.
    :param lowercase: set to True to lowercase the string.
    :param lemmatize: set to True to lemmatize the string.
    :param keep_nouns_only: set to True to keep nouns and adjectives only.
    :param simple_keep_nouns: by default proper noun phrases will be made inseparable by joining the words with
                              an underscore, coreference resolution will also be applied to expand surname mentions
                              back to fullnames (if the fullname appears elsewhere in the text).
                              Set this flag to True if you do not want this behaviour.
    :param eos_indicators: set to True to add <EOS> tokens into the text to indicate sentence boundaries.
    :returns: a string with the separate tokens joined back up with a space between them.
    """
    tokens = []
    pos_tags = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    
    if keep_nouns_only:
        
        if simple_keep_nouns:
            # Only keep adjectives and nouns                
            tokens = [(word, tag) for sent in pos_tags 
                      for (word, tag) in sent if tag in set(['NN', 'NNS', 'NNP', 'NNPS', 'JJ'])]
        else:
            # Potential people: key surname, value full name
            potential_people = {}
            
            # Only keep adjectives and nouns
            # Ensure noun phrases are grouped together
            nouns = set(['NN', 'NNS', 'JJ'])
            proper_nouns = set(['NNP', 'NNPS'])
            
            tokens = []
            token_so_far = ''
            
            for sent in pos_tags:
                            
                matching_proper_noun_phrase = False
                token_so_far = ''
                
                for word, tag in sent:
                    if matching_proper_noun_phrase:
                        if tag in proper_nouns:
                            token_so_far += '_{}'.format(word)
                        else:
                            # Matched the full proper noun, if a single noun then check to see if this potential
                            # surname is in the potential people list and use the full name instead of the token
                            noun_phrase_tokens = token_so_far.split('_')
                            
                            if len(noun_phrase_tokens) == 1:
                                if token_so_far in potential_people:
                                    tokens.append((potential_people[token_so_far], 'NP'))
                                else:
                                    tokens.append((token_so_far, 'NP'))
                            else:
                                tokens.append((token_so_far, 'NP'))
                            
                            # Add the proper noun phrase to the potential people set if length == 2
                            if len(noun_phrase_tokens) == 2:
                                # Use the fact news articles refer to people by surname once they have stated
                                # their full name
                                potential_people[noun_phrase_tokens[-1]] = token_so_far
                            
                            # Reset the matching process
                            token_so_far = ''
                            matching_proper_noun_phrase = False
                            
                            if tag in nouns:
                                tokens.append((word, tag))
                    else:
                        if tag in proper_nouns:
                            token_so_far = word
                            matching_proper_noun_phrase = True
                        elif tag in nouns:
                            tokens.append((word, tag))
                
                if token_so_far:
                    tokens.append((token_so_far, 'NP'))
                    
                # Add an end of sentence tag if instructed to do so
                if eos_indicators:
                    tokens.append(('<EOS>', 'NP'))
    else:
        
        if not eos_indicators:
            tokens = [(word, tag) for sent in pos_tags for (word, tag) in sent]
        else:
            for sent in pos_tags:
                for word, tag in sent:
                    
                    eos_detected = False
                    
                    # Catch case where new sentence was not started with a space
                    # Check the length of a word is greater than a limit before
                    # splitting to try and avoid splitting acronyms
                    if len(word) > 9:
                        eos_split = word.split('.')
                        # Should only be two words if a split at the end of a sentence occurred
                        if len(eos_split) == 2:
                            tokens.append((eos_split[0], 'NN'))
                            tokens.append(('<EOS>', 'NP'))
                            tokens.append((eos_split[1], 'NN'))
                            eos_detected = True
                    
                    if not eos_detected:
                        tokens.append((word, tag))
                
                # Add end of sentence tag
                tokens.append(('<EOS>', 'NP'))
                            

    updated_tokens = []
    
    prev_word = None
    
    for word, tag in tokens:
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
        # Also capture the case where a space did not occur between sentences 
        # e.g. "end of sentence.start of new sentence ..."
        words = word.split('/')
        # Check the length of a word is greater than a limit before splitting to try and avoid splitting acronyms
        if len(word) > 9 and len(words) == 1:
            eos_split = word.split('.')
            # Should only be two words if a split at the end of a sentence went wrong
            if len(eos_split) == 2:
                words = eos_split
        
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
        if word.lower() not in english_stopwords and word.lower() != '\'s' and not is_number(word) and not is_time(word):
            # Additional check to ensure U.S. is not lemmatised to U
            if lemmatize and word != 'US':
                word = lemmatizer.lemmatize(word, pos=wordnet_tag_from_penn_treebank(tag))
            updated_tokens.append(word)
        prev_word = word.lower()
                     
    return ' '.join(updated_tokens)


number_matcher = re.compile(r'^([:,/\.\-\+\\]*\d+[:,/\.\-\+\\]*)+$')
def is_number(token):
    """
    Given a token, returns True if the token is soley a sequence of numbers and punctuation.
    
    :param token: the token to test.
    :returns: True if the token is soley a sequence of numbers and punctuation.
    """
    return number_matcher.match(token) != None


days = set(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
months = set(['january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december'])
months_shortened = set(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
date_matcher = re.compile(r'^\d{1,2}(st|nd|rd|\-jan|\-feb|\-mar|\-apr|\-may|\-jun|\-jul|\-aug|\-sep|\-oct|\-nov|\-dec)$')
def is_time(token):
    """
    Given a token, returns True if the token is a time or date.
    
    :param token: the token to test.
    :returns: True if the token is a time or date.
    """
    lowercase_token = token.lower()
    
    if lowercase_token in days or lowercase_token in months or lowercase_token in months_shortened:
        return True
    
    if date_matcher.match(lowercase_token) != None:
        return True
    
    return False
    
    