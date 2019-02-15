#!/usr/bin/python2.7 

import cgi
import cgitb
import json
import re

cgitb.enable()

print "Content-type: application/json"
print
formData = cgi.FieldStorage()

# Get data from fields
search_string = formData.getvalue('search_string')

class RolepointFinder(object):

	def __init__(self,data_file,search_string):
		self.data_file     = data_file
		self.search_string = search_string
		self.matches       = []

	def run(self):
		self.loadData()
		self.returnResults()

	# Load data from Json file
	def loadData(self):

		regexp = re.compile(self.search_string)

		with open(self.data_file, 'r') as data_file:
			raw_content = data_file.read()

		content = json.loads(raw_content)

		while (content):
			row = content.pop()

			# This contains the real data
			string_list = []

			for key in row.keys():

				# Check if it is a list (job_history)
				if (type(row[key])) == list:
					for i in range(len(row[key])):
						string_list.append(row[key][i])
				# Check it's a string
				elif (isinstance(row[key], basestring)):
					string_list.append(row[key])

			for i in range(len(string_list)):
				if regexp.search(string_list[i]):
					self.matches.append(row)
					break

	def returnResults(self):
		print json.dumps(self.matches)



if __name__ == '__main__':
	rolePointFinder = RolepointFinder('data.json',search_string)
	rolePointFinder.run()
