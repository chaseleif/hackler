# clptext.py

import random
import requests
import discord
import asyncio

random.seed()


videonames = ["cute puppies","cute kitties","western techno","crab rave",
        "mowday","Sunday drive","study music","Sunday cartoons",
        "Internet","Cantina band","MC Hammer","Bob the Builder","NIS"]
videodetails = ["relaxing with the dogs","relaxing with the cats",
        "chill western-electro","crab party!","relaxing lawnmowers",
        "relaxing drive","focus music","cartoons","old videos",
        "chill lounge","relaxing hammer time",
        "relaxing background work noise","relaxing with sirens"]
videourls = ["https://www.youtube.com/watch?v=CP-oVjj9Mp4&autoplay=1",
        "https://www.youtube.com/watch?v=ZQAxN97H9yo&autoplay=1",
        "https://www.youtube.com/watch?v=Qcp2W1-SFt4&autoplay=1",
        "https://www.youtube.com/watch?v=-50NdPawLVY&autoplay=1",
        "https://www.youtube.com/watch?v=BcxeZ4Wwdn0&autoplay=1",
        "https://www.youtube.com/watch?v=zLllPmzo3fU&autoplay=1",
        "https://www.youtube.com/watch?v=jrKVhw_RT3M&autoplay=1",
        "https://www.youtube.com/watch?v=eh7lp9umG2I&autoplay=1",
        "https://www.youtube.com/watch?v=SR9yWFspCYs&autoplay=1",
        "https://www.youtube.com/watch?v=VmUGe8KDdGI&autoplay=1",
        "https://www.youtube.com/watch?v=r_AJg5VYPPs&autoplay=1",
        "https://www.youtube.com/watch?v=aJCilj7qMGg&autoplay=1",
        "https://www.youtube.com/watch?v=rIos0ya-yss&autoplay=1"]

videosplayed = []
def getvideo():
    global videosplayed
    if len(videosplayed)==len(videonames):
        videosplayed = []
    choice = random.randint(0,len(videonames)-1)
    while True:
        if choice not in videosplayed:
            videosplayed.append(choice)
            return videonames[choice],videodetails[choice],videourls[choice]
        choice+=1
        if choice==len(videonames):
            choice=0

JOKEURL = "https://official-joke-api.appspot.com/random_joke"

async def getandprintjoke(userchannel):
    await asyncio.sleep(1)
    await userchannel.trigger_typing()
    fetchresult = requests.get(JOKEURL)
    setup = ""
    punchline = ""
    if fetchresult.status_code!=200:
        setup = "What did the joke server say to the Discord bot that asked for a random joke?"
        punchline = "They said " + str(fetchresult.status_code) + " and that is NOT ok!"
    else:
        joke = fetchresult.json()
        setup = joke['setup']
        punchline = joke['punchline']
    await asyncio.sleep(2)
    await userchannel.send(f"**{setup}**")
    await asyncio.sleep(5)
    await userchannel.trigger_typing()
    await asyncio.sleep(2)
    await userchannel.send(f"***{punchline}***")

addops = ['+','-']
mulops = ['*','/','%']
operators = [addops,mulops]

#return precedence level, or zero for not a math op
def ismathop(achar):
    for i in range(len(operators)):
        for x in range(len(operators[i])):
            if achar==operators[i][x]:
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
            if rhi>=0:
                break
        if rhs in operators[i]:
            rhi=i
            if lhi>=0:
                break
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

def getoutputfromnumba(output, numba, negmul, numdiv):
    if negmul<0:
        numba*=negmul
        output+="("
    while numdiv>0:
        numba/=10
        numdiv-=1
    output+=str(numba)
    if negmul<0:
        output+=")"
    output+=" "
    return output

def parsemathstring(opstring :str):
    ops = ["("]
    output = ""
    opstring += ")"
    doingneg=False
    for i in range(len(opstring)):
        if opstring[i].isnumeric() or opstring[i].isalpha() or opstring[i]=='.':
            output+=opstring[i]
            for z in range(i+1,len(opstring)):
                if opstring[z].isalpha() or opstring[z].isnumeric() or opstring[z]=='.':
                    break
                else:
                    if doingneg==True:
                        output+=")"
                        doingneg=False
                    output+=" "
                    break
        elif opstring[i]=='(':
            ops.append(opstring[i])
        elif ismathop(opstring[i])>0 or opstring[i]==')': #math op
            # catch negative numbers
            if opstring[i]=='-':
                doingneg=True
                for z in range(i-1,-1,-1):
                    if opstring[z]=='(' or ismathop(opstring[z])>0:
                        break
                    if opstring[z].isalpha() or opstring[z].isnumeric():
                        doingneg=False
                        break
                if doingneg==True:
                    output+='(' # closing neg numbers in parenthesis
                    output+=opstring[i]
                    continue
            if output=="" or len(ops)==0 or (len(ops)>0 and ops[-1]=='(' or ismathop(opstring[i])>ismathop(ops[-1])):
                ops.append(opstring[i])
            else: # also with opstring[i]==')'
                while len(ops)>0:
                    if ops[-1]=='(':
                        break
                    if opstring[i]==')' or ismathop(opstring[i])<=ismathop(ops[-1]):
                        output+=ops.pop() + " "
                    else:
                        break
                if opstring[i]==')':
                    if len(ops)>0 and ops[-1]=='(': # if the right one isn't matched it is mismatched
                        ops.pop()
#                    elif (len(ops)>0 and ops[-1]!='(') or len(ops)==0):
                else:
                    ops.append(opstring[i])
    while len(ops)>1:
        if ops[-1]==")" or ops[-1]=="(":
            ops.pop()
            continue
        output+=str(ops.pop())
        if len(ops)>0:
            output+=" "
    return output









