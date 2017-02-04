"""
This is a super-simple script meant to demo how easy it is to make an Alexa
skill using Python 2.7 and AWS Lambda. This doesn't get into details about how
to create cards, reprompt text, etc.

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import json

data = json.loads(open('whiskey_data.json').read())

def build_response(output, should_end_session=True):
    '''
    boilerplate for creating the json response the Alexa service expects
    '''
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'shouldEndSession': should_end_session
        }
    }

def build_review_text(dram_data):
    '''
    some simple logic for creating a data-driven review that Alexa will read.
    '''

    # simple descriptors of quality
    if dram_data['average_ratings'] > 89:
        quality_adj = 'highly regarded'
    elif dram_data['average_ratings'] > 69:
        quality_adj = 'respectable'
    elif dram_data['average_ratings'] > 49:
        quality_adj = 'decent'
    else:
        quality_adj = 'awful'

    price = int(dram_data['average_price'])
    # simple descriptors of price
    if price > 0:              # null prices set to -1
        if price < 50:
            price_adj = 'affordable'
        elif price < 100:
            price_adj = 'average-priced'
        else:
            price_adj = 'expensive'

    review_text = 'The {} is a {} dram, with an average rating of {}.'.format(
                                                   dram_data['dram'],
                                                   quality_adj,
                                                   dram_data['average_ratings'])

    if price > 0:
        # if price was missing, don't say this sentence.
        review_text += " It's also an {} bottle at ${} for a fifth.".format(
                                                     price_adj  ,
                                                     price)

    return review_text

def lambda_handler(event, context):
    """
    A router for the incoming request to the correct intent handler. Since we
    only have one intent, this is fairly simple.
    """
    intent_name = event['request']['intent']['name']
    dram_name = event['request']['intent']['slots']['dram']['value']

    if intent_name == "GetReview":
        dram_data = None
        for row in data:
            if row['dram'].lower() == dram_name.lower():
                dram_data = row

        # short circuit if it's not a recognized whiskey
        if dram_data is None:
            sorry_response = "Sorry, I don't have an information on {}.".format(
                                                                      dram_name)
            return build_response(sorry_response)

        review_text = build_review_text(dram_data)
        return build_response(review_text)

    else:
        # Found an unrecognized intent!
        raise ValueError("Invalid intent")
