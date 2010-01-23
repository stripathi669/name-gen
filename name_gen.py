
import itertools
import random
import os

#filename = 'greek2'
#filename = 'greek3'
#filename = 'hebrew2'
filename = 'hebrew3'
#filename = 'lusiadas2'
#filename = 'lusiadas3'

#minimum and maximum number of syllables
if filename[-1] == '2':  #short syllables, more per word
	min_syl = 3
	max_syl = 5
else:  #long syllables, less per word
	min_syl = 2
	max_syl = 5


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
	
	#if chosen > counts[-1][1]: return None
	#out = itertools.takewhile(lambda (syl, count): count >= chosen, counts)
	#return counts[len(out)-1][0]

def load_language(language_file):
	with open(language_file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]
		
		syllables = lines[0].split(',')
		
		starts_ids = [int(n) for n in lines[1].split(',')]
		starts_counts = [int(n) for n in lines[2].split(',')]
		starts = zip(starts_ids, starts_counts)  #zip into a list of tuples
		
		ends_ids = [int(n) for n in lines[3].split(',')]
		ends_counts = [int(n) for n in lines[4].split(',')]
		ends = zip(ends_ids, ends_counts)
		
		#starting with the 6th and 7th lines, each pair of lines holds ids and counts for a prefix.
		combinations = []
		for (ids_str, counts_str) in zip(lines[5:None:2], lines[6:None:2]):
			if len(ids_str) == 0 or len(counts_str) == 0:  #empty lines
				combinations.append([])
			else:
				line_ids = [int(n) for n in ids_str.split(',')]
				line_counts = [int(n) for n in counts_str.split(',')]
				combinations.append(zip(line_ids, line_counts))
		
		return (syllables, starts, ends, combinations)

def tic():  #profiling functions
	global tictoc
	tictoc = os.times()[0]
	
def toc(msg = 'Elapsed time'):
	print msg + ': ' + str(os.times()[0] - tictoc) + 's'


tic()
#load from language file
language_file = 'Languages/' + filename + '.txt'
(syllables, starts, ends, combinations) = load_language(language_file)
toc('Load language')


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
