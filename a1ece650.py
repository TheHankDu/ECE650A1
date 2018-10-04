#!/usr/bin/env python
import sys
import re

#Customized Dict Class to handle case
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
			
class Point(object):
	def __init__(self,x,y):
		self.x = float(x)
		self.y = float(y)
		
	def __repr__(self):
		return "({0:.2f},{1:.2f})".format(self.x,self.y)

#Data Processing Class
class CameraData(object):
	def __init__(self,db={}):
		self.re_coordinate = re.compile(r'\(-?[0-9 ]+,-?[0-9 ]+\)')
		self.re_street = re.compile(r'\"[a-z ]+\"',re.I)
		self.db = db
		
		self.intersections = set([])
		self.vertices = {}
		self.edges = set([])
		
	
	def add(self, arg):
		sresult = self.re_street.match(arg,2)
		
		if sresult != None:
			street = sresult.group().strip('"')
			if not self.db.has_key(street):
				coordinate_list = []
			else:
				errprt("Invalid 'add' Command","Street Exists in system")
				return
		else:
			errprt("Invalid 'add' Command","Cannot find street name")
			return
		
		vresult = self.re_coordinate.search(arg)
		if vresult != None:
			tmp_list.extend(self.re_coordinate.findall(arg.replace(' ',"")))
			for coordinate in tmp_list:
				x,y = coordinate.replace('(','').replace(')','').split(',')
				coordinate_list.extend(Point(x,y))
			print(coordinate_list)
		else:
			errprt("Invalid 'add' Command","The format of argument {0} is invalid".format(arg))
			return
				
		self.db[street] = coordinate_list

	def change(self, arg):
		sresult = self.re_street.match(arg,2)
		if sresult != None:
			street = sresult.group().strip('"')
			if self.db.has_key(street):
				coordinate_list = []
				vresult = self.re_coordinate.search(arg)
				if vresult != None:
					tmp_list.extend(self.re_coordinate.findall(arg.replace(' ',"")))
					for coordinate in tmp_list:
						x,y = coordinate.replace('(','').replace(')','').split(',')
						coordinate_list.extend(Point(x,y))
					self.db[street] = coordinate_list
				else:
					errprt("Invalid 'change' Command","The format of argument {0} is invalid".format(arg))
					return
			else:
				errprt("Street Not Found","Street {0} does NOT exist in the system or it has already been removed".format(street))
				return
		else:
			errprt("Invalid Argument", "Format for street argument is invalid")
			return


	def remove(self, arg):
		sresult = self.re_street.match(arg,2)
		if sresult != None:
			street = sresult.group().strip('"')
			if self.db.has_key(street):
				del self.db[street]
			else:
				errprt("Street Not Found","Street {0} does NOT exist in the system or it has already been removed".format(street))
		else:
			errprt("Invalid Argument", "Format for remove argument is invalid")

	def graph(self):
		#Find All Intersection
		#Find all vertex and edges
		
	def intersection(self,s1,d1,s2,d2):
		x1, y1 = s1.x, s1.y
		x2, y2 = d1.x, d1.y
		x3, y3 = s2.x, s2.y
		x4, y4 = d2.x, d2.y

		xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
		xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
		

		ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
		yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
		
		if xden!=0 and yden!=0:
			xcoor =  xnum / xden
			ycoor = ynum / yden
		else: 
			return errprt("Invalid Intersection Coordinates","Divide by zero")

    		return point(xcoor, ycoor)
    		
    	def is_vertex(l1,l2,intsec):
    		x1, y1 = l1.x, l1.y
		x2, y2 = l2.x, l2.y
		xi, yi = intsec.x, intsec.y
		
		if x1==x2:
			if(xi==x1 and yi<=max(y1,y2) and yi>=min(y1,y2)):
				return True
		else:
			m = (y2-y1)/(x2-x1)
			b = y1-m*x1
			if(yi = m*xi+b and xi<=max(x1,x2) and xi>=min(x1,x2) and yi<=max(y1,y2) and yi>=min(y1,y2):
				return True
				
		return False

	
#Global Function
#act like exception
def errprt(msg,reason):
	#TODO use exception instead
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
		command = raw_input('>> ').strip()
		cmd_list = command.split(' ')
		#for cmd in commands:
		#	cmd_list = list.append(cmd)
		
		if((cmd_list[0]=='a') and (len(cmd_list)>2)):
			data.add(command)
		elif((cmd_list[0]=='c') and (len(cmd_list)>2)):
			data.change(command)
		elif(cmd_list[0]=='r'):
			data.remove(command)
		elif((cmd_list[0]=='g') and (len(cmd_list)==1)):
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
