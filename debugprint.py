__author__ = 'chozabu'

#based on http://stackoverflow.com/a/1620686/445831
import sys
import traceback

printcount = 0

class TracePrints(object):
	def __init__(self):
		self.stdout = sys.stdout
		self.newline = True
	def write(self, s):
		global printcount
		from settings import machine_name
		if self.newline:
			#self.stdout.write(s+"\n")
			stack = traceback.extract_stack()
			stackout = stack[-2]#[0:10]
			#self.stdout.write('--"'+machine_name+'"'+stackout[0]+'", line '+str(stackout[1])+', in '+stackout[2]+'\n')
			filename = stackout[0].split('/')[-1]
			ministack = filename + ':' + str(stackout[1])
			printcount +=1
			prefix = "(" + machine_name + " - " + str(printcount) + ' ' + ministack + ")"
			prefix+= " " * (40-len(prefix))
			strs = prefix + str(s)#+"\n"
		else:
			strs = s
		self.stdout.write(strs)
		if s == '\n':
			self.newline=True
		else:
			self.newline=False

sys.stdout = TracePrints()
