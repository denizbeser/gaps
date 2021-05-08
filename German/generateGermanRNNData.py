import numpy as np
import random
import operator

random.seed(1)

Data = np.load('german_data.npy', allow_pickle=True).item() # Format lemma: {S:(wordform, gender, phon, idNum); P:(...)}
genders = {'1':'MAS', '2':'FEM','3':'NTR'} 			# 5. GendNum (1 = M, 2 = F, 3 = N)

# print(len(Data)) 20k words
# Get the most frequent n lemmas
n = 5000
sortedLemmas = sorted(Data, key = lambda x: int(Data[x]['f']), reverse = True)[:n]

nouns = []
n2f = {}
for lemma in sortedLemmas:
 data = Data[lemma] 
 gender = genders[data['P'][1]]
 plural = data['P'][2]
 singular = data['S'][2]
 n2f[singular] = int(data['f'])
 nouns.append((singular,gender,plural))
  
random.shuffle(nouns)

with open('celex/german-src-train.txt','w') as src:
	with open('celex/german-tgt-train.txt','w') as tgt:
		for s,g,p in nouns[0:4000]:
			src.write(g+' <s> '+' '.join(list(s))+'\n')
			tgt.write(' '.join(list(p))+'\n')

with open('celex_token_freq/german-src-train.txt','w') as src:
 with open('celex_token_freq/german-tgt-train.txt','w') as tgt:
  freq_train = [item for item in nouns[0:4000] for i in range(n2f[item[0]])]
  random.shuffle(freq_train)
  for s,g,p in freq_train[0:4000]:
   src.write(g+' <s> '+' '.join(list(s))+'\n')
   tgt.write(' '.join(list(p))+'\n')
print('Token freq data type count:', len(set(i[0] for i in freq_train[:4000])))

for path in ['celex','celex_token_freq']:
  with open(f'{path}/german-src-val.txt','w') as src:
    with open(f'{path}/german-tgt-val.txt','w') as tgt:
      for s,g,p in nouns[4000:4500]:
        src.write(g+' <s> '+' '.join(list(s))+'\n')
        tgt.write(' '.join(list(p))+'\n')
  with open(f'{path}/german-src-test.txt','w') as src:
    with open(f'{path}/german-tgt-test.txt','w') as tgt:
      for s,g,p in nouns[4500:5000]:
        src.write(g+' <s> '+' '.join(list(s))+'\n')
        tgt.write(' '.join(list(p))+'\n')

  with open(f'{path}/german-wug.txt','w') as wug:
    for s,g,p in nouns[4500:5000]:
      wug.write(' '.join(list(s))+'\n')

  with open(f'{path}/german-wug-gendered.txt','w') as wug:
    for s,g,p in nouns[4500:5000]:
      wug.write(genders['3']+' <s> '+' '.join(list(s))+'\n')



