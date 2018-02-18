import json

data = json.load(open('haikus.json'))
haikus = list()
bad = 0
for haiku in data:
    lines = list(filter(None, haiku.split("\n")))
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line != '']
    if len(lines) %3 != 0:
        bad += 1
        print('bad haiku:\n{}'.format('\n'.join(lines)))
    else:
        haiku = list()
        while len(lines) > 0:
            haiku.append(lines.pop(0))
            if len(haiku) == 3:
                haikus.append(haiku)
                haiku = list()

unique = set()
save = list()
for haiku in haikus:
    msg = '\n'.join(haiku)
    if msg not in unique:
        unique.add(msg)
        save.append(haiku)

print('Total haikus: {}'.format(len(haikus)))
print('Total unique haikus: {}'.format(len(save)))
print('Total discarded: {}'.format(bad))
json.dump(save, fp=open('haikus-clean.json', 'w'))
