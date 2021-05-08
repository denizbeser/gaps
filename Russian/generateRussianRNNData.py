import numpy as np
import random
import operator
import math

random.seed(1)

defectives = []
with open('defective-verbs.txt', 'r') as inp:
	lines = inp.readlines()
	for i in range(1, len(lines)):
		line = lines[i]
		if i%4==1:
			verb = line.strip().split(',')[0]
			defectives.append(verb)
# print(len(defectives))

#dental verbs to sing
verb2sing = {}
with open('russian-verbs.csv', 'r') as inp:
	lines = inp.readlines()
	# print(len(lines))
	for i in range(1,len(lines)):
		tokens = lines[i].split('\t')
		bare = tokens[0]
		accented = tokens[1]
		english = tokens[2]
		fsg = tokens[12]
		
		# get only dental verbs
		if bare[-3:-1] in ['ит','из','ид','ис''иц']:
			j = 0
			while j < len(accented) and j < len(fsg) and accented[j] == fsg[j]: j += 1
			common = fsg[:j]
			inflection = fsg[j:]
			if inflection == '': continue
			# accented form, 1sg, common part, inflection
			verb2sing[bare] = (accented, fsg, common, inflection)

# 69 defective verbs
print(len(defectives))

# number of inflections ~34
inflections = set([d[3] for v,d in verb2sing.items()])
print(len(inflections))

# 2393 data points
verbs = [(k,v[1])for k,v in verb2sing.items() if k not in defectives]
print(len(verbs))

random.shuffle(verbs)

# Generate data for FG
with open('data/russian-src-train.txt','w') as src:
	with open('data/russian-tgt-train.txt','w') as tgt:
		for inf,fsg in verbs[0:2000]:
			src.write(' '.join(list(inf))+'\n')
			tgt.write(' '.join(list(fsg))+'\n')
with open('data/russian-src-val.txt','w') as src:
	with open('data/russian-tgt-val.txt','w') as tgt:
		for inf,fsg in verbs[2000:2300]:
			src.write(' '.join(list(inf))+'\n')
			tgt.write(' '.join(list(fsg))+'\n')
with open('data/russian-src-test.txt','w') as src:
	with open('data/russian-tgt-test.txt','w') as tgt:
		for inf,fsg in verbs[2300:-1]:
			src.write(' '.join(list(inf))+'\n')
			tgt.write(' '.join(list(fsg))+'\n')

with open('data/russian-defectives.txt','w') as f:
	for d in defectives:
		f.write(' '.join(list(d))+'\n')

#############################
# get to Zipfian distributions
# verb2singList = [(v,d) for v,d in verb2sing.items()]
# random.shuffle(verb2singList)
# zipf = []
# length = len(verb2singList)
# for rank in range(1,length+1):
# 	zipf.append(math.floor(length/rank))