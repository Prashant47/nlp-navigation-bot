import sys
import parser as kp
import requests
import json
import urllib
import os

def kparserDriver(sentence):
    url = "http://bioai8core.fulton.asu.edu/kparser/ParserServlet?"
    params = { 'text' : sentence, 'useCoreference' :'false' }
    queryString = urllib.parse.urlencode(params)
    response = requests.get(url+queryString)
    possibleSentences = ''
    if response.json():
        parser = kp.Parser()
        #possibleSentences = parser.getSentences(para)                              #para processing
        possibleSentences = parser.kparser(response.json())     #sentence processing
        possibleSentences =  ', '.join(possibleSentences)
    return possibleSentences  

