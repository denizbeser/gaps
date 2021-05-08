import numpy as np

# How:
# get nouns and gender from gsl.cd (German Syntax, Lemmas)
# Then get plurals for these lemmas gw(wordform and phonologic)


# First get noun lemmas ang their genders
# 1.   IdNum
# 2.   Head
# 3.   Mann
# 4. ClassNum (Noun = 1)
# 5. GendNum (1 = M, 2 = F, 3 = N)
lemma2Syntax = {}
with open('./celex2/german/gsl/gsl.cd') as gsl:
	lines = gsl.readlines()
	# Nouns and gender
	for line in lines:
		tokens = line.strip('\n').split('\\')
		lemmaID, head, pos, gender = tokens[0],tokens[1],tokens[3],tokens[4]
		if pos == '1':
			if gender in ['1','2','3']:
				lemma2Syntax[lemmaID] = (head, gender)

# Second, get plural forms get noun lemmas ang their genders
   # 1.   IdNum
   # 2.   Word
   # 3.   Mann
   # 4.   IdNumLemma
   # 5.   FlectType
lemma2Forms = {lemma:{} for lemma,dic in lemma2Syntax.items()}
with open('./celex2/german/gmw/gmw.cd') as gmw:
	lines = gmw.readlines()
	# Nouns and gender
	for line in lines:
		tokens = line.strip('\n').split('\\')

		idNum,wordform,lemmaID,inflection = tokens[0],tokens[1],tokens[3],tokens[4]
		# if a noun we care about
		if lemmaID in lemma2Syntax:
			# if plural or singular
			if 'nS' in inflection:
				lemma2Forms[lemmaID]['S'] = idNum
			elif 'nP' in inflection: 
				lemma2Forms[lemmaID]['P'] = idNum
	# filter out ones with only one signular or plural
	lemma2Forms = {i: dic for i, dic in lemma2Forms.items() if len(dic) > 1}


# Third, get phonological representaion for both singular and plural forms
# # Use IdNum to get it
#     1.      IdNum
#     2.      Word
#     3.      Mann
#     4.      IdNumLemma
#     5.      PhonStrsDISC
#     6.      PhonSylBCLX
#     7.      PhonCVBr
# Convert lemma to data structure: lemma: {S:(wordform, gender, phon, idNum); P:(...)}
lemma2Data = {lemma:{} for lemma,dic in lemma2Forms.items()}
with open('./celex2/german/gpw/gpw.cd') as gpw:
	lines = gpw.readlines()
	for line in lines:
		tokens = line.strip('\n').split('\\')
		idNum,wordform,lemmaID,phonology = tokens[0],tokens[1],tokens[3],tokens[5].replace('[','').replace(']','')
		# if a noun we care about
		if lemmaID in lemma2Forms:
			# Insert data
			gender = lemma2Syntax[lemmaID][1]
			if idNum == lemma2Forms[lemmaID]['S']:
				lemma2Data[lemmaID]['S'] = (wordform, gender, phonology, idNum)
			elif idNum == lemma2Forms[lemmaID]['P']:
				lemma2Data[lemmaID]['P'] = (wordform, gender, phonology, idNum)

# Get frequency
with open('./celex2/german/gfl/gfl.cd') as gfl:
	lines = gfl.readlines()
	for line in lines:
		tokens = line.strip('\n').split('\\')
		lemmaID,wordform,freq = tokens[0],tokens[1],tokens[2]
		# if a noun we care about
		if lemmaID in lemma2Data:
			# Insert data
			lemma2Data[lemmaID]['f'] = freq
			# print(freq)

np.save('german_data.npy', lemma2Data) 
# print(lemma2Data)