
import json


from nltk.tag import StanfordPOSTagger
jar = 'stanford-model/stanford-postagger-3.7.0.jar'
model = 'stanford-models/models/french.tagger'

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')
haikus = json.load(open('data/haikus.json'))

for haiku in haikus:
    for line in haiku:
        res = pos_tagger.tag(line.split())
        print(res)
        input()