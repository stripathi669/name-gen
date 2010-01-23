
import itertools
import random
import os

#filename = 'lusiadas'
#filename = 'greek'
filename = 'hebrew'

#fraction of acceptable syllables of 2 and 3 letters
syl_2_letters = 0.2
#syl_3_letters = 0.05
syl_3_letters = None

#minimum and maximum number of syllables
if syl_3_letters is None:  #short syllables, more per word
	min_syl = 3
	max_syl = 5
else:  #long syllables, less per word
	min_syl = 2
	max_syl = 5



def get_count(count_tuple):
	return count_tuple[1]

def get_best_syllables(num_letters, fraction, sample):
	alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
	
	#get all possible syllables using this number of letters, then count
	#them in the sample. output is list of tuples (syllable, count).
	counts = [(''.join(letters), sample.count(''.join(letters)))
		for letters in itertools.product(alphabet, repeat = num_letters)]
	
	#output to comma-separated-values file (view in Excel)
	#print counts, len(counts)
	#with open('counts.csv','w') as f:
	#	f.write(''.join([str(count_tuple[1]) + '\n' for count_tuple in counts]))
	
	#get only the syllables with the most counts, up to the fraction specified
	counts.sort(key = get_count)
	n = int(fraction * len(counts))
	counts = counts[-n:]
	
	#get syllables from the tuples by "unzipping"
	syllables = list(zip(*counts)[0])
	return syllables

def count_combinations(syllables):
	combinations = []
	for prefix in syllables:
		combinations.append(count_with_prefix(syllables, prefix))
	
	starts = count_with_prefix(syllables, ' ')
	ends = count_with_postfix(syllables, ' ')
	
	return (combinations, starts, ends)

def count_with_prefix(syllables, prefix):
	combinations = []
	total = 0
	for (index, syl) in enumerate(syllables):
		count = sample.count(prefix + syl)
		if count != 0:
			total += count
			combinations.append([index, total])
	return combinations

def count_with_postfix(syllables, postfix):
	combinations = []
	total = 0
	for (index, syl) in enumerate(syllables):
		count = sample.count(syl + postfix)
		if count != 0:
			total += count
			combinations.append([index, total])
	return combinations



def gen_word(syllables, combinations, starts, ends, min_syl, max_syl):
	#random number of syllables, the last one is always appended
	num_syl = random.randint(min_syl, max_syl - 1)
	
	#turn ends list of tuples into a dictionary
	ends_dict = dict(ends)
	
	#start word with the first syllable
	syl = select_syllable(syllables, starts, 0)
	word = [syllables[syl]]
	
	for i in range(1, num_syl):
		#don't end yet if we don't have the minimum number of syllables
		if i < min_syl: end = 0
		else: end = ends_dict.get(syl, 0)  #probability of ending for this syllable
		
		#select next syllable
		syl = select_syllable(syllables, combinations[syl], end)
		if syl is None: break  #early end for this word, end syllable was chosen
		
		word.append(syllables[syl])
		
	else:  #forcefully add an ending syllable if the loop ended without one
		syl = select_syllable(syllables, ends, 0)
		word.append(syllables[syl])
	
	return ''.join(word)

def select_syllable(syllables, counts, end_count):
	if len(counts) == 0: return None  #no elements to choose from
	
	#"counts" holds cumulative counts, so take the last element in the list
	#(and 2nd in that tuple) to get the sum of all counts
	chosen = random.randint(0, counts[-1][1] + end_count)
	
	for (syl, count) in counts:
		if count >= chosen:
			return syl
	return None

def save_language(language_file, syllables, starts, ends, combinations):
	with open(language_file, 'w') as f:
		(starts_ids, starts_counts) = zip(*starts)  #unzip list of tuples into 2 lists
		(ends_ids, ends_counts) = zip(*ends)
		
		lines = [
			','.join(syllables) + '\n',
			','.join([str(n) for n in starts_ids]) + '\n',
			','.join([str(n) for n in starts_counts]) + '\n',
			','.join([str(n) for n in ends_ids]) + '\n',
			','.join([str(n) for n in ends_counts]) + '\n',
		]
		
		for line in combinations:
			if len(line) == 0:  #special case, empty
				lines.append('\n');
				lines.append('\n');
			else:
				(line_ids, line_counts) = zip(*line)
				lines.append(','.join([str(n) for n in line_ids]) + '\n')
				lines.append(','.join([str(n) for n in line_counts]) + '\n')
		f.writelines(lines)

def tic():  #profiling functions
	global tictoc
	tictoc = os.times()[0]
	
def toc(msg = 'Elapsed time'):
	print msg + ': ' + str(os.times()[0] - tictoc) + 's'



tic()
#get sample text
with open('Samples/' + filename + '.txt', 'r') as f:
	sample = ''.join(f.readlines()).lower()

#remove all characters except letters from A to Z
a = ord('a')
z = ord('z')
sample = ''.join([
	c if (ord(c) >= a and ord(c) <= z) else ' '
		for c in sample])
toc('Load sample')


tic()
#get list of syllables of 2 letters
syllables = get_best_syllables(2, syl_2_letters, sample)

#optionally, do the same with 3 letters syllables (slower)
if syl_3_letters is not None:
	syllables.extend(get_best_syllables(3, syl_3_letters, sample))
toc('Scan syllables')

tic()
(combinations, starts, ends) = count_combinations(syllables)
toc('Scan combinations')


tic()
#save the results
if syl_3_letters is not None: language_file = 'Languages/' + filename + '3.txt'
else: language_file = 'Languages/' + filename + '2.txt'

save_language(language_file, syllables, starts, ends, combinations)
toc('Save output')


tic()
#generate a few words
words = []
for i in range(20):
	w = gen_word(syllables, combinations, starts, ends, min_syl, max_syl)
	print w
	words.append(w + '\n')
toc('Generate 20 words')

with open('out.txt', 'w') as f:
	f.writelines(words)


#pause (wait for some input)
try:
	raw_input()
except EOFError:
	pass
