import requests
import urllib 

class ResolveCoreference:

    def __init__(self):
        self.resolved_sentece = []
        self.input_sentence = None

    def process(self, corenlp_output):
       
        self.input_sentence = corenlp_output
        for coref in self.input_sentence['corefs']:
            mentions = self.input_sentence['corefs'][coref]
            antecedent = mentions[0]  #  first mention in the coreference chain
            for j in range(1, len(mentions)):
                mention = mentions[j]
                if mention['type'] == 'PRONOMINAL':
                    # get the attributes of the target mention in the corresponding sentence
                    target_sentence = mention['sentNum']
                    target_token = mention['startIndex'] - 1
                    # transfer the antecedent's word form to the appropriate token in the sentence
                    self.input_sentence['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']


    def get_resolved(self):
        possessives = {'hers', 'his', 'their', 'theirs'}
        for sentence in self.input_sentence['sentences']:
            for token in sentence['tokens']:
                output_word = token['word']
                # check lemmas as well as tags for possessive pronouns in case of tagging errors
                if token['lemma'] in possessives or token['pos'] == 'PRP$':
                    output_word += "'s"  # add the possessive morpheme
                output_word += token['after']
                self.resolved_sentece.append(output_word)
        resolvedStr = ''.join(self.resolved_sentece) 
        return resolvedStr

def ResolveCoreferenceDriver(data):
    text = "Tom and Jane are good friends. They are cool. He knows a lot of things and so does she. His car is red, but " \
        "hers is blue. It is older than hers. The big cat ate its dinner."

    url = 'http://localhost:9000?properties='
    params = '\"annotators": \"dcoref\", \"outputFormat\": \"json\"'
    #print(params)
    queryString = urllib.parse.quote(params)
    #data = 'John is teacher. He loves coding'
    #data = "You pick up the fork and plate. Then move them to another table."
    #data = 'You move the green ball on red block. Now pick it up again and put it on yellow base'
    #data = 'push the box to left of table and put fork on it.'
    #print(url+queryString)
    response = requests.post(url+queryString,data)
    resolveObj = ResolveCoreference()
    resolveObj.process(response.json())
    return resolveObj.get_resolved()
if __name__ == "__main__":
    print(ResolveCoreferenceDriver(input()))
