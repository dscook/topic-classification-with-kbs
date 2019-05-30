import requests

from kb_common import convert_topic_probs_wikipedia_to_actual, print_topic_probs


# data to be sent to api 
data = {'text': """
Philip Morris Tuesday Kansas attorney general decision list states lawsuits tobacco firms Medicaid money tobacco-related illnesses Philip Morris Kansas Attorney General Carla Stovall courts public policy tobacco Philip Morris companies lawsuit zealousness bandwagon attorney general fact state viaable legal basis upon cigarette manufacturers Gregory Little lawyer Philip Morris law correct state Kansas process waste millions taxpayer dollars time costs
"""
} 

r = requests.post(url = 'http://127.0.0.1:5000/classify', json = data) 
probabilities = r.json()
converted_probabilities = convert_topic_probs_wikipedia_to_actual(probabilities)
print_topic_probs(converted_probabilities)