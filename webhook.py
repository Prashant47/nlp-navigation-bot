
import json

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
log = app.logger

@app.route('/', methods=['GET'])
def test():
    return make_response(jsonify({'fulfillmentText': 'server is up and running.'}))


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    req = request.get_json(silent=True, force=True)
    print(req)
    try:
        intent = req.get('queryResult').get('intent').get('displayName')
    except AttributeError:
        return 'json error'

    if intent == 'moveto':
        parameters = req.get('queryResult').get('parameters')
        direction = parameters.get('DisplacementAction')
        quantity = parameters.get('number-integer')
        if not quantity or not direction:
            res = 'undefined move command found. Original Move command MOVE DIRECTION QUANTITY'
        else:
            res = 'MOVE ' + direction + ' ' + str(quantity) 
    elif intent == 'pick':
        parameters = req.get('queryResult').get('parameters')
        obj = parameters.get('object')
        if not obj:
            res = 'undefined object in pick command.'
        else:
            res = 'PICK ' + obj
    elif intent == 'jump':
        parameters = req.get('queryResult').get('parameters')
        direction = parameters.get('DisplacementAction')
        quantity = parameters.get('number-integer')
        if not quantity or not direction:
            res = 'undefined jump command found. Original jump command JUMP DIRECTION QUANTITY'
        else:
            res = 'JUMP ' + direction + ' ' + str(quantity) 
    elif intent == 'put':
        parameters = req.get('queryResult').get('parameters')
        obj = parameters.get('object')
        if not obj:
            res = 'undefined object in pick command.'
        else:
            res = 'PUT ' + obj
    elif intent == 'isvisible':
        res = 'what should I do ' +req.get('queryResult').get('queryText')
    else:
        res = 'Undefined'

    return make_response(jsonify({'fulfillmentText': res}))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
