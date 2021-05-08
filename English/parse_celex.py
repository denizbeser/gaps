import os
import random
import math

random.seed(1)
rootDir = os.path.abspath('')
data_path = './data/'
present = {}
past = {}

# Get verb wordforms
with open('./celex_relevant/emw/emw.cd') as emw:
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

# Get phonetic forms
phonemes = {}
with open('./celex_relevant/epw/epw.cd') as epw:
	lines = epw.readlines()
	for line in lines:
		tokens = line.strip('\n').split('\\')
		wordform,lemmaID,phonology = tokens[1],tokens[3],tokens[8].replace('[','').replace(']','')
		if lemmaID in present and lemmaID in past and wordform not in phonemes:
			phonemes[wordform] = phonology

# Get frequency 
frequencies = {} 
import math
with open('./celex_relevant/efw/efw.cd') as efw: 
  lines = efw.readlines() 
  for line in lines: 
    tokens = line.strip('\n').split('\\') 
    lemmaID,wordform,freq = tokens[0],tokens[1],tokens[5] 
    if lemmaID in present and lemmaID in past: 
      frequencies[lemmaID] = int(round(float(freq)))
# print(sum(frequencies.values()))
# print((frequencies))
# print(max(frequencies.values()))

data = []
for lemmaID in present.keys():
	if lemmaID in past:
		presform = present[lemmaID]
		pastform = past[lemmaID][0]
		inflection = past[lemmaID][1] if past[lemmaID][1] != '' else 'IRR'
		presphon = phonemes[presform]
		pastphon = phonemes[pastform]
		data.append((presform,presphon,pastform,inflection,pastphon,lemmaID))

random.shuffle(data)
data = data[:5000]
# print(data)
irregular_data = [d for d in data if d[3] == 'IRR']
random.shuffle(irregular_data)
regular_data = [d for d in data if d[3] != 'IRR']
random.shuffle(regular_data)
print(len(irregular_data))
print(len(regular_data))


# # Generate mixed Kirov Dataset
random.shuffle(data)
train = data[:round(len(data)*0.8)]
val = data[round(len(data)*0.8):round(len(data)*0.9)]
test = data[round(len(data)*0.9):len(data)]

with open('data/english-src-train.txt', 'w') as out:
	for item in train:
		out.write(' '.join(c for c in item[1]) + '\n')
with open('data/english-tgt-train.txt', 'w') as out:
	for item in train:
		 out.write(' '.join(c for c in item[4]) + '\n')

freq_train = [item for item in train for i in range(math.ceil((frequencies[item[-1]]+1)/10))]
print(len(freq_train))
random.shuffle(freq_train)
with open('data_token_freq/english-src-train.txt', 'w') as out:
  for item in freq_train[:4000]: 
    out.write(' '.join(c for c in item[1]) + '\n')
with open('data_token_freq/english-tgt-train.txt', 'w') as out:
  for item in freq_train[:4000]: 
    out.write(' '.join(c for c in item[4]) + '\n')		  
print('Token freq data type count:', len(set(i[1] for i in freq_train[:4000])))

for path in ['data','data_token_freq']:
  with open(f'{path}/english-all.txt', 'w') as out:
  	for d in data:
	  	out.write(' '.join(d) + '\n')

  with open(f'{path}/english-src-val.txt', 'w') as out:
    for item in val:
      out.write(' '.join(c for c in item[1]) + '\n')
  with open(f'{path}/english-tgt-val.txt', 'w') as out:
    for item in val:
      out.write(' '.join(c for c in item[4]) + '\n')

  with open(f'{path}/english-src-test.txt', 'w') as out:
    for item in test:
      out.write(' '.join(c for c in item[1]) + '\n')
  with open(f'{path}/english-tgt-test.txt', 'w') as out:
    for item in test:
      out.write(' '.join(c for c in item[4]) + '\n')

  with open(f'{path}/english-irr-src-test.txt', 'w') as out:
    for item in test:
      if item in irregular_data:
        out.write(' '.join(c for c in item[1]) + '\n')
  with open(f'{path}/english-irr-tgt-test.txt', 'w') as out:
    for item in test:
      if item in irregular_data:
        out.write(' '.join(c for c in item[4]) + '\n')

  with open(f'{path}/english-irr-test.txt', 'w') as out:
    for item in test:
      if item in irregular_data:
        out.write(' '.join(item) + '\n')

print('Done!')
# raise RuntimeError


# #######################################
# # Generate Schuler Experiment Datasets

# exp_lists = ['3r6e-x1','5r4e-x1',
# 	'3r6e-x2-LangA','5r4e-x2-LangA','3r6e-x2-LangB','5r4e-x2-LangB']

# past_count_list = [16,8,5,4,4,3,3,3,3]
# exp2index = {'3r6e-x2-LangA':[1,0,1,0,1,0,0,0,0],'5r4e-x2-LangA':[1,0,1,0,1,0,1,0,1],
# 	'3r6e-x2-LangB':[0,1,0,1,0,1,0,0,0],'5r4e-x2-LangB':[0,1,0,1,0,1,0,1,1]}
# multiplier = 100
# n_train_types = 1000
# n_val_types = 100
# n_test_types = 100

# # Generate data files for each experiment
# for exp in exp_lists:
# 	# Setup directory for experiment
# 	exp_dir = rootDir+data_path+exp+'/'
# 	# if os.path.exists(exp_dir): os.system('rm -r '+exp_dir)
# 	os.makedirs(exp_dir)
# 	src_train_path = exp_dir+'src-train.txt'
# 	tgt_train_path = exp_dir+'tgt-train.txt'
# 	src_val_path = exp_dir+'src-val.txt'
# 	tgt_val_path = exp_dir+'tgt-val.txt'
# 	src_test_path = exp_dir+'src-test.txt'
# 	tgt_test_path = exp_dir+'tgt-test.txt'
# 	# Generate training files
# 	with open (src_train_path, 'w') as srctrainf:
# 		with open (tgt_train_path, 'w') as tgttrainf:
# 			# Set number of regulars and exceptions for training 
# 			# for i in range(9):
# 			# 	# Pick type: X1: is i < N regular? X2: is i an index where data should be regular?
# 			# 	isRegular = exp2index[exp][i] if 'x2' in exp else (i < int(exp[0]))
# 			# 	item = regular_data[i] if isRegular else irregular_data[i]
# 			# 		for j in range(past_count_list[i]):
# 			# 		# repeat each item multiplier times
			
# 			for item in random.sample(data, n_train_types):
# 				srctrainf.write(' '.join(list(item[1]+'\n')))
# 				tgttrainf.write(' '.join(list(item[4]+'\n')))

# 	# Generate validation files
# 	with open (src_val_path, 'w') as srcvalf:
# 		with open (tgt_val_path, 'w') as tgtvalf:
# 			for i in range(9):
# 				# Pick type: X1: is i < N regular? X2: is i an index where data should be regular?
# 				isRegular = exp2index[exp][i] if 'x2' in exp else (i < int(exp[0]))
# 				item = regular_data[i] if isRegular else irregular_data[i]					
# 				for j in range(past_count_list[i]):
# 					srcvalf.write(' '.join(list(item[1]+'\n')))
# 					tgtvalf.write(' '.join(list(item[4]+'\n')))

# 	# Generate test files
# 	with open (src_test_path, 'w') as srctestf:
# 		with open (tgt_test_path, 'w') as tgttestf:
# 			for item in random.sample(regular_data, n_test_types):
# 				srctestf.write(' '.join(list(item[1]+'\n')))
# 				tgttestf.write(' '.join(list(item[4]+'\n')))
		
# # Preprocess data
# nmtdir = '../OpenNMT-py/'
# for experiment in os.listdir(rootDir+data_path):
# 	if '.DS' in experiment: continue
# 	expdir = rootDir+data_path+experiment
# 	os.system('python '+nmtdir+'preprocess.py -train_src '+expdir+'/src-train.txt -train_tgt '+expdir+'/tgt-train.txt -valid_src '+expdir+'/src-val.txt -valid_tgt '+expdir+'/tgt-val.txt -save_data '+expdir+'/processed')

# # Generate mixed Kirov Dataset
# random.shuffle(data)
# train = data[:round(len(data)*0.8)]
# val = data[round(len(data)*0.8):round(len(data)*0.9)]
# test = data[round(len(data)*0.9):len(data)]

# with open('kirov_data/src-train.txt', 'w') as out:
# 	for item in train:
# 		out.write(' '.join(c for c in item[1]) + '\n')
# with open('kirov_data/tgt-train.txt', 'w') as out:
# 	for item in train:
# 		out.write(' '.join(c for c in item[4]) + '\n')
# with open('kirov_data/src-val.txt', 'w') as out:
# 	for item in val:
# 		out.write(' '.join(c for c in item[1]) + '\n')
# with open('kirov_data/tgt-val.txt', 'w') as out:
# 	for item in val:
# 		out.write(' '.join(c for c in item[4]) + '\n')
# with open('kirov_data/src-test.txt', 'w') as out:
# 	for item in test:
# 		out.write(' '.join(c for c in item[1]) + '\n')
# with open('kirov_data/tgt-test.txt', 'w') as out:
# 	for item in test:
# 		out.write(' '.join(c for c in item[4]) + '\n')

# # Generate Schuler Dataset


