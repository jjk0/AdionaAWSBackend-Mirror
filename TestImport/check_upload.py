import json

f = open('testFile.json')

data = json.load(f)

acceleration = data['acceleration']['z_val']

abs_minutes = len(acceleration) / (60*32)
seconds = abs_minutes * 60
print('minutes', seconds)