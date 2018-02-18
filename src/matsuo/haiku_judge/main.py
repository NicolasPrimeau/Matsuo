
import json
import random
import queue
from multiprocessing import Process, Queue
from langdetect import detect
from nltk.tag import StanfordPOSTagger


JAR = 'stanford-models/stanford-postagger-3.8.0.jar'
MODELS = {
    'fr': 'stanford-models/models/french.tagger',
    'en': 'stanford-models/models/english-bidirectional-distsim.tagger'
}


class HaikuJudge:

    def __init__(self, haiku_model=None):
        self.pos_taggers = dict()
        self.haiku_model = haiku_model

    def tag_line(self, text):
        language = detect(text)
        if language not in MODELS:
            language = random.choice(list(MODELS.keys()))
        if language not in self.pos_taggers:
            self.pos_taggers[language] = StanfordPOSTagger(MODELS[language], JAR, encoding='utf-8')

        return self.pos_taggers[language].tag(text.split())

    def judge_haiku(self, haiku):
        scores = list()
        for idx in range(len(haiku)):
            tagged = self.tag_line(haiku[idx])
            if tagged is None:
                return 0
            annotations = list(map(lambda x: x[1], tagged))
            scores.append(self.haiku_model.probability(idx, annotations))
        return sum(scores) / len(scores)


class HaikuModel:

    def __init__(self):
        self.train_models = [[], [], []]
        self.statistical_models = None
        self.cnt = 0

    def add_model(self, i, model):
        self.cnt += 1
        self.train_models[i].append(model)

    def learn(self):
        self.statistical_models = [None, None, None]
        for idx in range(len(self.train_models)):
            self.statistical_models[idx] = self._learn(idx)

    def _learn(self, idx):
        occurences = dict()
        for model in self.train_models[idx]:
            model = tuple(model)
            if model not in occurences:
                occurences[model] = 0
            occurences[model] += 1
        sum_of_all = sum(map(lambda key: occurences[key], occurences.keys()))
        for key in occurences.keys():
            occurences[key] = occurences[key] / sum_of_all
        return occurences

    def probability(self, idx, model):
        model = tuple(model)
        if model in self.statistical_models[idx]:
            return self.statistical_models[idx][model]
        else:
            return 0

    def save(self):
        models = {'cnt': 0, 'data': [[], [], []]}
        max_val = 0
        for idx in range(len(self.statistical_models)):
            max_val = max((max_val, len(self.statistical_models[idx])))
            for key in self.statistical_models[idx].keys():
                models['data'][idx].append((key, self.statistical_models[idx][key]))
        models['cnt'] = max_val
        json.dump(models, fp=open('models/haiku-model.json', 'w'))

    def load(self):
        loaded = json.load(fp=open('models/haiku-model.json'))
        self.cnt = loaded['cnt']
        models = loaded['data']
        self.statistical_models = [dict(), dict(), dict()]
        for idx in range(len(models)):
            for t in models[idx]:
                self.statistical_models[idx][tuple(t[0])] = t[1]


def pos_tagger(in_q, out_q):
    print('Producer process started')
    judge = HaikuJudge()
    try:
        while True:
            haiku = in_q.get()
            for idx in range(len(haiku)):
                annotated = judge.tag_line(haiku[idx])
                if annotated is not None:
                    out_q.put((idx, [x[1] for x in annotated]))
    except queue.Empty:
        pass


def add_to_model(in_q):
    print('Consumer process started')
    cnt = 0
    model = HaikuModel()
    try:
        while True:
            item = in_q.get(block=True, timeout=60)
            idx, tagged = item
            model.add_model(idx, tagged)
            cnt += 1
            print('To process: {}'.format(in_q.qsize()))
            print('Haikus processed: {}'.format(cnt))
            if cnt % 250 == 0:
                model.learn()
                model.save()
    except queue.Empty:
        pass

    model.learn()
    model.save()


if __name__ == '__main__':
    data = json.load(open('data/haikus.json'))
    input_q = Queue()
    for item in data:
        input_q.put(item)
    output_q = Queue()
    processes = list()
    for i in range(4):
        processes.append(Process(target=pos_tagger, args=(input_q, output_q)))
    processes.append(Process(target=add_to_model, args=(output_q, )))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    input_q.close()
    output_q.close()
