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

"""
name-gen: Free python name generator module that analyzes sample text and produces
	similar words.

Spartan example usage.
"""

from namegen import NameGen


#filename = 'greek2'
#filename = 'greek3'
#filename = 'hebrew2'
filename = 'hebrew3'
#filename = 'lusiadas2'
#filename = 'lusiadas3'


#load generator data from language file
language_file = 'Languages/' + filename + '.txt'

generator = NameGen(language_file)


#generate a few words
for i in range(20):
	print generator.gen_word()


#pause (wait for some input)
try:
	raw_input()
except EOFError:
	pass
