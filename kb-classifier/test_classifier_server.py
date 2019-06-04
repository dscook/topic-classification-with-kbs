import requests
import numpy as np

from kb_common import wiki_topics_to_actual_topics, wiki_topics_to_index, print_topic_probs


def convert_topic_probs_wikipedia_to_actual(topic_to_prob):            
    topic_indexes = set([index for index in wiki_topics_to_actual_topics.values()])
    
    topic_index_to_prob = np.zeros(shape=len(topic_indexes))
    wiki_topic_index_to_prob = np.zeros(shape=len(wiki_topics_to_index.keys()))
    
    for topic in topic_to_prob.keys():
        topic_index_to_prob[wiki_topics_to_actual_topics[topic]] += topic_to_prob[topic]
        wiki_topic_index_to_prob[wiki_topics_to_index[topic]] = topic_to_prob[topic]
            
    return topic_index_to_prob, wiki_topic_index_to_prob

# data to be sent to api 
data = {'text': """
Leicester City football club is set to float its shares on the stock market, a move expected to value the English premier league side at about 40 million pounds ($64.2 million), The Sunday Telegraph reported.
The newspaper said Leicester, which is currently in the middle of the premier league table and has reached the Coca Cola Cup final, is poised to write to existing shareholders about the plan.
Victory in the Coca-Cola final next month, its first cup final in 28 years, would qualify the Midlands club to play in European competition next year.
"""
} 

# Classify the text
r = requests.post(url = 'http://127.0.0.1:5000/classify', json = data) 
probabilities = r.json()
print(probabilities)
converted_probabilities, _ = convert_topic_probs_wikipedia_to_actual(probabilities)
print_topic_probs(converted_probabilities)

# Get the normalised probabilities
r = requests.get(url = 'http://127.0.0.1:5000/probabilities/1') 
normalised_prob = r.json()
print(normalised_prob)