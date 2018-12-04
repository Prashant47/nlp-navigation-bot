import sys
import parser as kp
import requests
import json
import urllib
import os

def main():
    sentence = raw_input()
    url = "http://bioai8core.fulton.asu.edu/kparser/ParserServlet?"
    params = { 'text' : sentence, 'useCoreference' :'false' }
    queryString = urllib.urlencode(params)
    response = requests.get(url+queryString)
    possibleSentences = ''
    if response.json():
        parser = kp.Parser()
        #possibleSentences = parser.getSentences(para)                              #para processing
        possibleSentences = parser.kparser(response.json())     #sentence processing
        possibleSentences =  ', '.join(possibleSentences)
    print(possibleSentences)  
if __name__ == "__main__":
    main()
