import random

present = {}
past = {}

# Get verb wordforms
with open('./emw/emw.cd') as emw:
	lines = emw.readlines()
	# Get present tense
	for line in lines:
		tokens = line.strip('\n').split('\\')
		wordform,lemmaID,tense,inflection = tokens[1],tokens[3],tokens[4],tokens[5]
		if tense == 'e1S':
			if len(wordform.split())==1:
				if lemmaID not in present:
					present[lemmaID] = wordform
	# Get past tense
	for line in lines:
		tokens = line.strip('\n').split('\\')
		wordform,lemmaID,tense,inflection = tokens[1],tokens[3],tokens[4],tokens[5]
		if tense == 'a1S':
			if lemmaID in present:
				past[lemmaID] = (wordform,inflection)

# Get phonemes
phonemes = {}
with open('./epw/epw.cd') as epw:
	lines = epw.readlines()
	for line in lines:
		tokens = line.strip('\n').split('\\')
		wordform,lemmaID,phonology = tokens[1],tokens[3],tokens[8].replace('[','').replace(']','')
		if lemmaID in present and lemmaID in past and wordform not in phonemes:
			phonemes[wordform] = phonology

lemma2data = {}
for lemmaID in present.keys():
	if lemmaID in past:
		presform = present[lemmaID]
		pastform = past[lemmaID][0]
		inflection = past[lemmaID][1] if past[lemmaID][1] != '' else 'IRR'
		presphon = phonemes[presform]
		pastphon = phonemes[pastform]
		lemma2data[lemmaID] = (presform,presphon,pastform,inflection,pastphon)

c_irr = sum([1 for k,v in lemma2data.items() if v[3] == 'IRR'])
print(c_irr / len(lemma2data))


# Generate dataset


