#!/usr/bin/python

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep
from operator import itemgetter
import sys

class MRMlens(MRJob):

	def mapper_arrange(self,_,line):
		line=line.strip()
		parts = line.split("::")
		user_id = parts[0]
		movie_id = parts[1]
		rating = parts[2]
		yield user_id, movie_id+','+rating
	def reducer_arrange(self,user_id,pairs):
		res = ""
		for pair in pairs:
			res = res+pair+' '
		yield user_id, res

	def steps(self):
		return [
			MRStep(mapper=self.mapper_arrange,reducer = self.reducer_arrange)
		]	
if __name__ == '__main__':
	MRMlens.run()	
