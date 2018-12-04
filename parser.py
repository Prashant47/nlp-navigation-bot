import json

class Parser:
    def __init__(self):
        self.prcSentences = []
        self.edges = {'recipient','instance_of' }

    def sentences(self, para):
        prePrcSnts = para.split(".")
        for sentence in prePrcSnts:
            self.prcSentences.append(sent for sent in self.kparser(sentence))
        return self.prcSentences

    def kparser(self, parser_input):
        #data = json.loads(open('kparserOutput.json').read())    #Data to come from kparser
        
        sentences = []
        queue = []
        for data in parser_input:
            if data["data"]["isEvent"]:
                queue.append(data)
            while(queue):
                curr = dict(queue.pop())
                for child in curr["children"]:
                    if child["data"]["isEvent"]:
                        queue.append(child)
                    elif child["data"]["isEntity"] and child['data']['Edge'] in self.edges:
                        currSentence = curr["data"]["word"].split('-')[0] + self.traverse(child)
                        sentences.append(currSentence)
        return sentences

    def traverse(self, child):
        queue = [child]
        sentence = ""
        while queue:
            curr = queue.pop()
            sentence += " " + curr["data"]["word"].split('-')[0]
            for child in curr["children"]:
                if child["data"]["isEntity"] and child['data']['Edge'] in self.edges:
                    queue.append(child)
        return sentence
