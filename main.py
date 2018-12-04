import sys
import parser as kp
import requests
import json
import urllib
import os
import dialogflow
import kparserInterface
import resolvecoref


def main():
    directory = '/home/prashant/fall18/nlp/project/nlp/examples/'
    url = "http://bioai8core.fulton.asu.edu/kparser/ParserServlet?"
   
    while True:
        try:
            sentence = input("User> ")
            sentence = resolvecoref.ResolveCoreferenceDriver(sentence)
            print("coref: ",sentence)
            kparser_output = kparserInterface.kparserDriver(sentence)
            print("kparser: ",kparser_output)
            sentence = sentence.replace('and','.')
            sentence = sentence.replace(',','.')
            sentence = sentence.split('.')
            print("split sentence: ",sentence)
            detect_intent_texts('robot-1a726' ,'abded',sentence ,'en',kparser_output)

        except EOFError:
            break
    
def detect_intent_texts(project_id, session_id, texts, language_code,kparser_output):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    #print('Session path: {}\n'.format(session))
    result = []
    for index, text in enumerate(texts):
        if text:
            text = text.strip()
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

            query_input = dialogflow.types.QueryInput(text=text_input)

            response = session_client.detect_intent(
                session=session, query_input=query_input)

            #print('=' * 20)
            #print('Query text: {}'.format(response.query_result.query_text))
            #print('Detected intent: {} (confidence: {})\n'.format(
            #    response.query_result.intent.display_name,
            #    response.query_result.intent_detection_confidence))
            #print(text,response.query_result.fulfillment_text)
            if response.query_result.fulfillment_text == 'Undefined':
                kparser_output_list = kparser_output.split(',')
                if index < len(kparser_output_list):
                    result.append(kparser_output_list[index] )
                else:
                    result.append(kparser_output)
            else:
                result.append(response.query_result.fulfillment_text )
        
    print('Bot> ' + ','.join(result)+ '\n')

if __name__ == "__main__":
    main()
