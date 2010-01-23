"""
Copyright 2010 Joao Henriques <jotaf (no spam) at hotmail dot com>.

This file is part of name-gen.

name-gen is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

name-gen is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with name-gen.  If not, see
<http://www.gnu.org/licenses/>.
"""

import itertools
import random

class NameGen:
	"""
	name-gen: Free python name generator module that analyzes sample text and produces
	similar words.
	
	Usage:
		1. Initialize with path to language file (generated using 'namegen_training.py').
		2. Possibly change min_syl and max_syl to control number of syllables.
		3. Call gen_word() method, returns generated string.
	"""
	
	def __init__(self, language_file):
		self.min_syl = 2
		self.max_syl = 5
		with open(language_file, 'r') as f:
			lines = [line.strip() for line in f.readlines()]
			
			self.syllables = lines[0].split(',')
			
			starts_ids = [int(n) for n in lines[1].split(',')]
			starts_counts = [int(n) for n in lines[2].split(',')]
			self.starts = zip(starts_ids, starts_counts)  #zip into a list of tuples
			
			ends_ids = [int(n) for n in lines[3].split(',')]
			ends_counts = [int(n) for n in lines[4].split(',')]
			self.ends = zip(ends_ids, ends_counts)
			
			#starting with the 6th and 7th lines, each pair of lines holds ids and counts for a prefix.
			self.combinations = []
			for (ids_str, counts_str) in zip(lines[5:None:2], lines[6:None:2]):
				if len(ids_str) == 0 or len(counts_str) == 0:  #empty lines
					self.combinations.append([])
				else:
					line_ids = [int(n) for n in ids_str.split(',')]
					line_counts = [int(n) for n in counts_str.split(',')]
					self.combinations.append(zip(line_ids, line_counts))
	
	def gen_word(self):
		#random number of syllables, the last one is always appended
		num_syl = random.randint(self.min_syl, self.max_syl - 1)
		
		#turn ends list of tuples into a dictionary
		ends_dict = dict(self.ends)
		
		#start word with the first syllable
		syl = self.select_syllable(self.starts, 0)
		word = [self.syllables[syl]]
		
		for i in range(1, num_syl):
			#don't end yet if we don't have the minimum number of syllables
			if i < self.min_syl: end = 0
			else: end = ends_dict.get(syl, 0)  #probability of ending for this syllable
			
			#select next syllable
			syl = self.select_syllable(self.combinations[syl], end)
			if syl is None: break  #early end for this word, end syllable was chosen
			
			word.append(self.syllables[syl])
			
		else:  #forcefully add an ending syllable if the loop ended without one
			syl = self.select_syllable(self.ends, 0)
			word.append(self.syllables[syl])
		
		return ''.join(word)

	def select_syllable(self, counts, end_count):
		if len(counts) == 0: return None  #no elements to choose from
		
		#"counts" holds cumulative counts, so take the last element in the list
		#(and 2nd in that tuple) to get the sum of all counts
		chosen = random.randint(0, counts[-1][1] + end_count)
		
		for (syl, count) in counts:
			if count >= chosen:
				return syl
		return None

