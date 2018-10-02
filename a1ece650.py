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
		return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key)
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

def initialization():
	#menu = {"a","c","r","g"}
	re_vertex = re.compile('\(-?[0-9]+,-?[0-9]+\)')
	re_street = re.compile('\"[ a-z]+\"')
	db = CaseInsensitiveDict()
	
	return menu

def add(self, arg_list[]):
	if re_street.match(arg_list[0]):
		street = cmd
			
	for arg in arg_list[1:]:
		if re_vertex.match(arg):
			#TODO Distinguish no space between 
			vertex_list.extend(re_vertex.finditer(arg))
		else:
			errprt("Invalid 'add' Command","The format of argument {0} is invalid".format(cmd))
			return
			
	db[street] = vertex_list

def change(self, arg_list[]):
	if re_street.match(arg_list[0]):
		if db.has_key(arg_list[0])
			for arg in arg_list[1:]:
				if re_vertex.match(arg):
					#TODO Distinguish no space between 
					vertex_list.extend(re_vertex.finditer(arg))
				else:
					errprt("Invalid 'add' Command","The format of argument {0} is invalid".format(cmd))
				db[street] = vertex_list
		else:
			errprt("Street Not Found","Street {0} does NOT exist in the system or it has already been removed".format(street))
	else:
		errprt("Invalid Argument", "Format for street argument is invalid")


def remove(self, street):
	if re_street.match(street):
		if db.has_key(street)
			del db[street]
		else:
			errprt("Street Not Found","Street {0} does NOT exist in the system or it has already been removed".format(street))
	else:
		errprt("Invalid Argument", "Format for street argument is invalid")

def graph(self):

def errprt(msg,reason):
	print("Error: {0}. Possible Reason: {1}".format(msg,reason))
	
def helpprt():
	#TODO
	print("HELP ME PLEASE")

def main_loop(init):
	menu = {"a","c","r","g"}
	is_quit = False
	while not is_quit:
		commands = raw_input('>> ').strip().split()
		for cmd in commands:
			cmd_list = list(cmd)
		
		if(cmd_list[0]=='a'):
			add(cmd_list[1:])
		elif(cmd_list[0]=='c'):
			change(cmd_list[1:])
		elif(cmd_list[0]=='r' && len(cmd_list)==2):
			remove(cmd_list[1])
		elif(cmd_list[0]=='g' && len(cmd_list)==1):
			graph()
		elif(cmd_list[0]=='q'):
			is_quit = True
		else:
			errprt("Command [{0}] is not valid".format(cmd_list[0]),"Wrong command name or incorrect arguments")
		
		#original code from Prof
		line = sys.stdin.readline()
		if line == '':
		break
		print 'read a line:', line

    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
	init = initialization()
	try:	
		main_loop(init)
	except KeyboardInterrupt:
		clear
		sys.exit(0)
