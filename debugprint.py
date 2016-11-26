__author__ = 'chozabu'

#based on http://stackoverflow.com/a/1620686/445831
import sys
import traceback

printcount = 0

class TracePrints(object):
	def __init__(self):
		self.stdout = sys.stdout
	def write(self, s):
		global printcount
		printcount +=1
		from settings import machine_name
		#self.stdout.write(s+"\n")
		strs = "(" + machine_name + " - " + str(printcount) + ")" + str(s)#+"\n"
		self.stdout.write(strs)
		#stack = traceback.extract_stack()
		#stackout = stack[-2]#[0:10]
		#self.stdout.write('--"'+machine_name+'"'+stackout[0]+'", line '+str(stackout[1])+', in '+stackout[2]+'\n')

sys.stdout = TracePrints()
