# hkcalc.py

import hktext

def str2num(numstr):
    if type(numstr)==int or type(numstr)==float:
        return numstr
    returnval = 0
    multiplier=1
    dodivide=False
    numdivisions=0
    for c in numstr:
        if c == '-':
            multiplier=-1
        elif c=='.':
            dodivide=True
        elif c.isnumeric():
            returnval*=10
            returnval+=ord(c)-ord('0')
            if dodivide==True:
                numdivisions+=1
    returnval*=multiplier
    while numdivisions>0:
        returnval/=10
        numdivisions-=1
    return returnval

def domath(message :str):
    postfixstr = hktext.parsemathstring(message)
    vals = []
    numba=0
    dodivide=False
    havenum=False
    numdivisions=0
    multiplier=1
    matherror=""
    skipminus=False
    for i in range(len(postfixstr)):
        # negative numbers are surrounded by parenthesis
        # user can also add extra parenthesis, correction attempt currently limited
        if skipminus==True:
            skipminus=False
            if postfixstr[i]=='-':
                multiplier=-1
                continue
        if postfixstr[i]=='(':
            skipminus=True
            continue
        if postfixstr[i].isnumeric():
            havenum=True
            numba*=10
            numba+=ord(postfixstr[i])-ord('0')
            if dodivide==True:
                numdivisions+=1
        elif postfixstr[i]=='.':
            dodivide=True
        elif postfixstr[i]==' ' or postfixstr[i]==')': # space after every number
            if havenum==True:
                havenum=False
                numba*=multiplier
                multiplier=1
                while numdivisions>0:
                    numdivisions-=1
                    numba/=10
                dodivide=False
                vals.append(numba)
                numba=0
        elif hktext.ismathop(postfixstr[i])>0 and len(vals)>1:
            rhs=vals.pop()
            lhs=vals.pop()
            if postfixstr[i]=='+':
                vals.append(str2num(lhs)+str2num(rhs))
            elif postfixstr[i]=='-':
                vals.append(str2num(lhs)-str2num(rhs))
            elif postfixstr[i]=='*':
                vals.append(str2num(lhs)*str2num(rhs))
            elif postfixstr[i]=='/':
                if str2num(rhs)==0:
                    if len(matherror)>0:
                        matherror+=", "
                    matherror+="**Divide by zero**"
                    vals.append(0)
                else:
                    vals.append(str2num(lhs)/str2num(rhs))
            elif postfixstr[i]=='%':
                if str2num(rhs)==0:
                    if len(matherror)>0:
                        matherror+=", "
                    matherror+="**Divide by zero**"
                    vals.append(0)
                else:
                    vals.append(str2num(lhs)%str2num(rhs))
    numba=0
    if len(vals)>0:
        numba=vals[0]
    if type(numba)==float and numba.is_integer()==True:
        numba = int(numba)
    return postfixstr,numba,matherror

