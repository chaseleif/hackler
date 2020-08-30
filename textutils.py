# textutils.py

import random
import requests

random.seed()


videonames = ["cute puppies","cute kitties","western techno","crab rave","mowday","Sunday drive","study music","Sunday cartoons","Internet","Cantina band"]
videodetails = ["relaxing with the dogs","relaxing with the cats","chill western-electro","crab party!","relaxing lawnmowers","relaxing drive","focus music","cartoons","old videos","chill lounge"]
videourls = ["https://www.youtube.com/watch?v=CP-oVjj9Mp4&autoplay=1","https://www.youtube.com/watch?v=ZQAxN97H9yo&autoplay=1","https://www.youtube.com/watch?v=Qcp2W1-SFt4&autoplay=1","https://www.youtube.com/watch?v=-50NdPawLVY&autoplay=1","https://www.youtube.com/watch?v=BcxeZ4Wwdn0&autoplay=1","https://www.youtube.com/watch?v=zLllPmzo3fU&autoplay=1","https://www.youtube.com/watch?v=jrKVhw_RT3M?v=r_AJg5VYPPs&autoplay=1","https://www.youtube.com/watch?v=eh7lp9umG2I&autoplay=1","https://www.youtube.com/watch?v=SR9yWFspCYs&autoplay=1","https://www.youtube.com/watch?v=VmUGe8KDdGI&autoplay=1"]

def getvideo():
	choice = random.randint(0,len(videonames)-1)
	return videonames[choice],videodetails[choice],videourls[choice]

JOKEURL = "https://official-joke-api.appspot.com/random_joke"

def get_joke():
	request = requests.get(JOKEURL)
	if request.status_code==200:
		return request.json()
	return False

addops = ['+','-']
mulops = ['*','/','%']
operators = [addops,mulops]

#return precedence level, or zero for not a math op
def ismathop(achar):
	for i in range(len(operators)):
		for op in operators[i]:
			if achar==op:
				return i+1
	return 0

# return: -1 == lhs < rhs, 0 === equal, 1 == lhs>rhs
def mathnumcompare(lhs, rhs):
	try:
		lhnum = int(lhs) # try for ints
		rhnum = int(rhs)
		if lhnum<rhnum:
			return -1
		elif lhnum==rhnum:
			return 0
		else:
			return 1
	except ValueError: # have chars
		pass
	lhi=-1
	rhi=-1
	for i in range(len(operators)):
		if lhs in operators[i]:
			lhi=i
		if rhs in operators[i]:
			rhi=i
	if lhi<rhi:
		return -1
	if lhi==rhi:
		return 0
	return 1

class btree:
	def __init__(self,val):
		self.left = None
		self.right = None
		self.val = val

	def __init__(self):
		self.left = None
		self.right = None
		self.val = None

	def insert(self,val):
		if self.val is None:
			self.val = val
		elif mathnumcompare(val,self.val)==-1:
			if self.left is None:
				self.left = btree(val)
			else:
				self.left.insert(val)
		else:
			if self.right is None:
				self.right = btree(val)
			else:
				self.right.insert(val)

	def getpostorder(self):
		returnval = ""
		if self.val is None:
			return returnval
		if self.left is not None:
			returnval+=self.left.getpostorder()
		if self.right is not None:
			returnval+=self.right.getpostorder()
		returnval+=str(self.val)
		return returnval

def parsemathstring(opstring :str):
	ops = []
	numba=0
	dodivision=False
	numdivisions=0
	havenumber=False
	negmultiplier=1
	output = ""
	opstring+="#" # garbage character, so last number can get caught in the loop
	for i in range(len(opstring)):
		if opstring[i].isnumeric():
			if havenumber==True:
				numba*=10
				numba+=ord(opstring[i])-ord('0')
			else:
				havenumber=True
				numba=ord(opstring[i])-ord('0')
			if dodivision==True:
				numdivisions+=1
			continue
		if opstring[i]=='.':
			dodivision=True
			continue
		if havenumber==True:
			havenumber=False
			if negmultiplier<0:
				numba*=negmultiplier
				output+="("
			if dodivision==True:
				while numdivisions>0:
					numba/=10
					numdivisions-=1
				dodivision=False
			output+=str(numba)
			if negmultiplier<0:
				negmultiplier=1
				output+=")"
			output+=" "
			numba=0
		if opstring[i]=='-': #neg numbers
			isnegative=True
			for x in range(i-1,-1,-1):
				if opstring[x].isnumeric():
					isnegative=False
					break
				if ismathop(opstring[x])>0:
					isnegative=True
					break
			if isnegative==True:
				negmultiplier=-1
				continue
		if ismathop(opstring[i])>0: #math op
			if len(ops)==0 or (len(ops)>1 and ismathop(opstring[i])>=ismathop(ops[len(ops)-1])):
				ops.append(opstring[i])
			else:
				for x in range(len(ops)-1,-1,-1):
					if ismathop(ops[x])>=ismathop(opstring[i]):
						output+=str(ops.pop()) + " "
					else:
						break
				ops.append(opstring[i])
	while len(ops)>0:
		output+=str(ops.pop())
		if len(ops)>0:
			output+=" "
	return output









