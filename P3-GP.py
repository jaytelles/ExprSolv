from random import choice
import random
import math
import copy
import sys

unaryOperators = ['sin', 'cos', 'tan', 'neg']
binaryOperators = ['+', '-', '*', '/', '^']

def isNumber(exp):
  dummy = [1,2]
  if type(exp) == type(dummy):
    return False

  if exp in binaryOperators:
    return False

  if exp in unaryOperators:
    return False

  if exp == 'x':
    return False

  return True

def firstIndexOfExpressionAfterUnary(exp):
  x = 1
  unaryFound = False
  for x in xrange(1, len(exp)):
    if exp[x] in unaryOperators:
      unaryFound = True
    elif not(exp[x] in unaryOperators) and not(exp[x] in binaryOperators) and unaryFound == True:
      return x

def createPop(a):
  exp = []
  exp.append(choice(binaryOperators))
  exp.append(makeNewSub(a))
  exp.append(makeNewSub(a))
  return exp
  
def makeNewSub(a):
  if a==0:
    return random.randrange(1,1000,1)
  
  n = random.randrange(1,100,1)
  if n>=1 and n<35:
    #make a new expression
    sub = createPop(a-1)
    if n>=30 and n<35:
      sub.insert(1, choice(unaryOperators))
  elif n>=35 and n<75:
    #make a number from 1 to 100
    sub = str(random.randrange(1,100,1))
  else:
    #add an x
    sub = 'x'
    
  return sub

def findExpResult(atom, xVal):
#atom is either a number, another expression, a unary operator, or x
  if isNumber(atom):
    return int(atom)
  elif atom == 'x':
    return xVal
  else:
    return solveBinary(atom, xVal)
    
def solveUnary(exp, xVal):
  expIndex = firstIndexOfExpressionAfterUnary(exp)
  unaryIndex = expIndex - 1
  if exp[unaryIndex] in unaryOperators:
    if exp[unaryIndex] == 'sin':
      try:
        res = int(math.sin(math.radians(findExpResult(exp[expIndex], xVal))))
      except OverflowError:
        res = 0
      exp.pop(expIndex)
      exp.pop(unaryIndex)
      exp.insert(unaryIndex, res)
      return solveBinary(exp, xVal)
      
    elif exp[unaryIndex] == 'cos':
      try:
        res = int(math.cos(math.radians(findExpResult(exp[expIndex], xVal))))
      except OverflowError:
        res = 0
      exp.pop(expIndex)
      exp.pop(unaryIndex)
      exp.insert(unaryIndex, res)
      return solveBinary(exp, xVal)

    elif exp[unaryIndex] == 'tan':
      try:
        res = int(math.tan(math.radians(findExpResult(exp[expIndex], xVal))))
      except OverflowError:
        res = 0
      exp.pop(expIndex)
      exp.pop(unaryIndex)
      exp.insert(unaryIndex, res)
      return solveBinary(exp, xVal)
    
    elif exp[unaryIndex] == 'neg':
      res = -1 * findExpResult(exp[expIndex], xVal)
      exp.pop(expIndex)
      exp.pop(unaryIndex)
      exp.insert(unaryIndex, res)
      return solveBinary(exp, xVal)
      
def solveBinary(exp, xVal):
  #exp is a list
  numUnaries = len(exp)-3
  if numUnaries > 0:    #thus ensuring that only one unary operator can be present in a single expression
    return solveUnary(exp, xVal)
        
  else:
    exp1 = int(findExpResult(exp[1], xVal))
    exp2 = int(findExpResult(exp[2], xVal))
    
    if exp[0] == '+':
      res = exp1 + exp2
    elif exp[0] == '-':
      res = exp1 - exp2
    elif exp[0] == '*':
      res = exp1 * exp2
    elif exp[0] == '/':
      if not(exp2 == 0):
        res = exp1/exp2
      else:
        return int(816032569874212484785703145698620508)
    elif exp[0] == '^':
      if not(exp1==0 and exp2<0):
        try:
          if exp2 > 10:
            exp2 = 10
          if exp1 > 400:
            exp1 = 400
          res = exp1 ** exp2
        except OverflowError:
          return int(816032569874212484785703145698620508)
      else:
        return int(816032569874212484785703145698620508)
        
    return res   
    
def numX(exp):
  if exp=='x':
    return 1
  elif isNumber(exp):
    return 0
  elif exp in binaryOperators:
    return 0
  elif exp in unaryOperators:
    return 0
  else:
    sum = 0
    for sub in xrange(0,len(exp)):
      if exp[sub]=='x':
        sum+=1
      else:
        if not(isNumber(exp[sub]) or exp[sub] in unaryOperators or exp[sub] in binaryOperators):
          #its a function, do recursion
          sum+=numX(exp[sub])
    return sum

def findRandomExp(exp):
    a = random.randrange(1,100,1) 
    if a > 0 and a<=40:
      #exp[1]
      if isNumber(exp[1]) or exp[1] == 'x':
        b = random.randrange(1,10,1)
        if b <5:
          return exp[1]
        else:
          return findRandomExp(exp)
        
      elif exp[1] in unaryOperators:
        newExp.pop(1)
        return findRandomExp(newExp)
      else:
        b = random.randrange(1,10,1)
        if b<=4:
          return exp[1]
        else:
          return findRandomExp(exp[1])
        
    elif a>40 and a<=80:
      #exp2
      if isNumber(exp[2]) or exp[2] == 'x':
        return exp[2]
      elif exp[2] in unaryOperators:
        newExp.pop(2)
        return findRandomExp(newExp)
      else:
        b = random.randrange(1,10,1)
        if b<=5:
          return exp[2]
        else:  
          return findRandomExp(exp[2])
        
    elif a>80 and a<=100:
      return exp[0]

def swap(exp, searchVal, newVal):
#takes an expression, the value to replace, and the value to replace it with
#returns a list that represents the swapped expression
  
  found = False
  index = 0
  while index<len(exp) and found==False:
    if exp[index] == searchVal:
      found = True
      exp[index]= newVal
    else:
        if not(isNumber(exp[index]) or exp[index] in binaryOperators or exp[index] in unaryOperators or exp[index]=='x'):
          swap(exp[index], searchVal, newVal)
    index+=1    
        
  return exp

def typeOf(exp):
  ret = -1
  if isNumber(exp) or exp=='x':
    ret = 1
  elif exp in binaryOperators:
    ret = 2
  elif exp in unaryOperators:
    ret = 3
  else:
    ret = 4
 
  return ret
 
def typesValid(exp1, exp2):
  if exp1==1:
    if exp2==1:
      return True
    elif exp2==2:
      return False
    elif exp2==3:
      return False
    elif exp2==4:
      return True

  if exp1==2:
    if exp2==1:
      return False
    elif exp2==2:
      return True
    elif exp2==3:
      return False
    elif exp2==4:
      return False

  if exp1==3:
    if exp2==1:
      return False
    elif exp2==2:
      return False
    elif exp2==3:
      return True
    elif exp2==4:
      return False

  if exp1==4:
    if exp2==1:
      return True
    if exp2==2:
      return False
    if exp2==3:
      return False
    if exp2==4:
      return True

  return False
   
   
def doMutation(exp, count):
  if count == 0:
    return None
  
  a = random.randrange(1,100,1)
  if a<=5:
    b = random.randrange(1,10,1)
    if b>0 and b<=4:
      #change exp[1]
      c = random.randrange(1,2,1)
      if c==1:
        newVal = makeNewSub(count-1)
        if isNumber(newVal):
          if numX(exp[1])>=1 or numX(exp[2])>0:
            exp[1] = newVal
            return exp
          else:
            return None
        else:
          exp[1] = newVal
        return exp
      else:
        return doMutation(exp[1])
        
    elif b>4 and b<=8:
      #change exp[2]
      c = random.randrange(1,2,1)
      if c==1:
        newVal = makeNewSub(count-1)
        if isNumber(newVal):
          if numX(exp[2])>=1 or numX(exp[1])>0:
            exp[1] = newVal
            return exp
          else:
            return None
        else:
          exp[2] = newVal
        return exp
      else:
        return doMutation(exp[2])
        
    elif b>8 and b<=10:
      #change the operator
      exp[0] == choice(binaryOperators)
      return exp
      
  else:
    return None
  
def doCrossover(exps, counter):
  if counter == 3:
    return []
    
  exp1 = copy.deepcopy(exps[0])
  exp2 = copy.deepcopy(exps[1])
 
  swap1 = findRandomExp(exp1)
  swap2 = None
  loops = 0
  
  while swap2 == None and loops<10:
    swap2 = findRandomExp(exp2)

    if typesValid(typeOf(swap1), typeOf(swap2)):
      if swap1!=swap2:
        if numX(swap1)>0:
          if numX(exp1)>=1 and numX(swap2)>0:
            sol1 = swap(exp1, swap1, swap2)
            sol2 = swap(exp2, swap2, swap1)
            retlist = [sol1, sol2]
            return retlist
          else:
            swap2 =  None
            loops += 1
            
        elif numX(swap2)>0:
          if numX(exp2)>=1 and numX(swap1)>0:
            sol1 = swap(exp1, swap1, swap2)
            sol2 = swap(exp2, swap2, swap1)
            retlist = [sol1, sol2]
            return retlist
          else:
            swap2 = None
            loops += 1
        
        else:
          sol1 = swap(exp1, swap1, swap2)
          sol2 = swap(exp2, swap2, swap1)
          retlist = [sol1, sol2]
          return retlist
      else:
        swap2 = None
        loops += 1
    else:
      swap2 = None
      loops += 1
  if loops == 10:
    return doCrossover(exps, counter+1)
 
def doGenetics(exps, values, popsize):
  ress = []
  for x in xrange(0,popsize):
    ress.append([])
    for value in values:
      ress[len(ress)-1].append(solveBinary(exps[x],value[0]))

  errs = None
  errs = []
  for res in ress:
    totalSum = 0
    for x in xrange(0, len(res)):
      #predicted val - observed val
      try:
        totalSum+= values[x][1] - res[x]
      except OverflowError:
        totalSum = int(10000000000)
    try:
      err = math.sqrt((totalSum ** 2) / len(res))
    except OverflowError:
      err = int(816032569874212484785703145698620508)
    errs.append(err)
  
  
  sortederrs = sorted(copy.deepcopy(errs))
  if len(sortederrs)>=50:  
    lowestErr = sortederrs[0]
    nextLowestErr = sortederrs[1]
    lowestErrIndex = errs.index(lowestErr)
    nextLowestErrIndex = errs.index(nextLowestErr)
    lowestErrExp = exps[lowestErrIndex]
    nextLowestErrExp = exps[nextLowestErrIndex]  
  elif len(sortederrs)==1:
    lowestErr = sortederrs[0]
    lowestErrIndex = errs.index(lowestErr)
    lowestErrExp = exps[lowestErrIndex]
    nextLowestErrExp = lowestErrExp
  else:
    lowestErr = nestLowestErr = None
  
  print lowestErr
  
  if lowestErr < 500:
    print "FOUND SOLUTION"
    print "solution: " + str(lowestErrExp)
    return lowestErrExp
   
  exps = []
  exps.append(lowestErrExp)
  exps.append(nextLowestErrExp)
  more = doCrossover(copy.deepcopy(exps), 0)
  
  
  mutt = doMutation(copy.deepcopy(exps)[0], 4)
  if mutt != None:
    exps.append(mutt)
    
  
  for exp in more:
    exps.append(exp)
  
  while len(exps) < 100:
    exps.append(createPop(4))
  
  doGenetics(exps, values, len(exps))
 

  
if __name__ == "__main__":
  if len(sys.argv) == 2:
    f = open(str(sys.argv[1]), 'r')
  else:
    f = open('fn1.csv', 'r')
    
  values = []
  counter = 0
  for line in f:
    if counter<1000:
      value = []
      dex = line.find(',')
      value.append(int(line[0:dex]))
      value.append(int(line[dex+1:len(line)-1]))
      values.append(value)
      value = []
      counter += 1


  #create random populations
  popsize = 100
  exps = []
  ress = []
  errs = []
  xVal = 1
  fxVal = 2
  counter = 0 
  while counter<popsize:
    exp = createPop(4)
    if numX(exp)>0:
      counter+=1
      exps.append(exp)
    
  doGenetics(exps, values, popsize)