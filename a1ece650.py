#!/usr/bin/env python
import sys
import re

class CaseInsensitiveDict(dict):
	@classmethod
	def _k(cls, key):
		return key.lower() if isinstance(key, basestring) else key

	def __init__(self, *args, **kwargs):
		super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
		self._convert_keys()
	def __getitem__(self, key):
		return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))
	def __setitem__(self, key, value):
		super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)
	def __delitem__(self, key):
		return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))
	def __contains__(self, key):
		return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))
	def has_key(self, key):
		return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))
	def pop(self, key, *args, **kwargs):
		return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)
	def get(self, key, *args, **kwargs):
		return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)
	def setdefault(self, key, *args, **kwargs):
		return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)
	def update(self, E={}, **F):
		super(CaseInsensitiveDict, self).update(self.__class__(E))
		super(CaseInsensitiveDict, self).update(self.__class__(**F))
	def _convert_keys(self):
		for k in list(self.keys()):
			v = super(CaseInsensitiveDict, self).pop(k)
			self.__setitem__(k, v)

class CameraData(object):
	def __init__(self,db={}):
		self.re_vertex = re.compile('\(-?[0-9]+,-?[0-9]+\)')
		self.re_street = re.compile('\"[a-z ]+\"')
		self.db = db
	
	def add(self, arg_list):
		street = self.re_street.match(arg_list)
		print(street)
		if street != None:
			vertex_list = []
		else:
			errprt("Invalid 'add' Command","The format of argument {0} is invalid".format(arg_list))
			return
		
		if self.re_vertex.match(arg_list):
			vertex_list.extend(self.re_vertex.finditer(arg_list))
		else:
			errprt("Invalid 'add' Command","The format of argument {0} is invalid".format(arg_list))
			return
				
		self.db[street] = vertex_list

	def change(self, arg_list):
		street = self.re_street.match(arg_list)
		if street != None:
			if self.db.has_key(street):
				vertex_list = []
				if self.re_vertex.match(arg):
					vertex_list.extend(self.re_vertex.finditer(arg))
				else:
					errprt("Invalid 'add' Command","The format of argument {0} is invalid".format(arg))
					db[street] = vertex_list
			else:
				errprt("Street Not Found","Street {0} does NOT exist in the system or it has already been removed".format(street))
		else:
			errprt("Invalid Argument", "Format for street argument is invalid")


	def remove(self, street):
		if self.re_street.match(street):
			if self.db.has_key(street):
				del self.db[street]
			else:
				errprt("Street Not Found","Street {0} does NOT exist in the system or it has already been removed".format(street))
		else:
			errprt("Invalid Argument", "Format for street argument is invalid")

	def graph(self):
		print("???")

	
#Global Function
def errprt(msg,reason):
	print("Error: {0}. Possible Reason: {1}".format(msg,reason))
	
def helpprt():
	#TODO
	print("HELP ME PLEASE")

def initialization():
	#menu = {"a","c","r","g"}
	db = CaseInsensitiveDict({})
	data = CameraData(db)
	return data

def main_loop(data):
	is_quit = False
	while not is_quit:
		
		command = raw_input('>> ')
		cmd_list = command.split(' ')
		#for cmd in commands:
		#	cmd_list = list.append(cmd)
		
		print(cmd_list)
		if((cmd_list[0]=='a') & (len(cmd_list)>2)):
			data.add(command)
		elif((cmd_list[0]=='c') & (len(cmd_list)>2)):
			data.change(command)
		elif((cmd_list[0]=='r') & (len(cmd_list)==2)):
			data.remove(command)
		elif((cmd_list[0]=='g') & (len(cmd_list)==1)):
			data.graph()
		elif(cmd_list[0]=='q'):
			is_quit = True
		else:
			errprt("Command [{0}] is not valid".format(cmd_list),"Wrong command name or incorrect arguments")
	# return exit code 0 on successful termination
	sys.exit(0)

if __name__ == '__main__':
	data = initialization()
	try:	
		main_loop(data)
	except KeyboardInterrupt:
		clear
		sys.exit(0)
