from math import exp
from random import random, randint

def pivals(arr):
  s = sum([exp(k) for k in arr])
  #print(arr)
  if (s==0):
    print(arr)
  ret = [exp(k)/s for k in arr]
  return(ret)

# 0: north, 1: east, 2: south, 3: west
def left(action):
  if (action==0):
    return(3)
  else:
    return(action-1)

def move(row, col, action):
  if (action==0):
    return(row+1, col)
  elif (action==1):
    return(row, col+1)
  elif (action==2):
    return(row-1, col)
  else:
    return(row, col-1)

def right(action):
  if (action==3):
    return(0)
  else:
    return(action+1)

def succ(row, col, action):
  rand = random()
  #print(rand)
  oldrow, oldcol = row, col
  if (rand<=0.8):
    nextr, nextc = move(row, col, action)
  elif (rand>0.9):
    nextr, nextc = move(row, col, left(action))
  else:
    nextr, nextc = move(row, col, right(action))
  if (nextr>2 or nextr<0):
    nextr = oldrow
  if (nextc>3 or nextc<0):
    nextc = oldcol
  if ((nextr, nextc)==(1,1)):
    nextr, nextc = oldrow, oldcol
  return(nextr, nextc)

def polgrad(arr, a):
  to_ret = [1 - pivals(arr) for k in arr]

'''def randmax(arr):
  max = arr[0]
  ret = 0
  for k in range(len(arr)):
    if (arr[k]>max):
      max = arr[k]
      ret = k
    elif (arr[k]==max):
      if (random()>0.5):
        ret = k
  #print(arr, ret)
  return(ret)'''

def randmax(arr):

    #[sum=sum+abs(i) for i in arr]
    #Sum=sum([abs(i) for i  in arr])
    #print("Sum",Sum)
    #prob=uniform(0,Sum)
    prob=random()

    if(prob<=arr[0]):
        return 0
    elif (prob<=arr[0]+arr[1]):
        return 1
    elif (prob<=arr[0]+arr[1]+arr[2]):
        return 2
    return 3

wall = [[1, 1, 1, 1, 1, 1],[1, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 1], [1, 0, 0, 0, 0, 1],[1, 1, 1, 1, 1, 1]]
terminal = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0], [ 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
nonterminal = [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0], [ 0, 1, 0, 1, 0, 0], [0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0]]
gamma = 1.0
theta  = [[[0]*4]*4]*3
#print(theta)
alphas = [0.01, 0.1, 1]
states = [(row, col) for row in range(3) for col in range(4)]

#print(pis)
u = 0

for alpha in alphas:
  print("alpha ", alpha)
  theta  = [[[0]*4]*4]*3
  pis = [[pivals(theta[i][j]) for j in range(4)] for i in range(3)]
  #pis = [[pivals(theta[i][j]) for j in range(4)] for i in range(3)]
  cumreward = 0
  for episode in range(1000):
    theta  = [[[0]*4]*4]*3
    print("   episode",episode)
    # for step in range(100):
    # actions = [max(pis[i][j]) for i in range(3) for j in range(4)]
    # states = [succ(states[i][j], actions[i][j]) for i in range(3) for j in range(4)]
    is_terminal = False
    count = 0
    row, col = 0, 0
    traversal = list()
    traversal.append(row)
    traversal.append(col)
    reward = 0
    traversal.append(reward)
    rewards = [[0]*4]*3
    counter = [[0]*4]*3
    pis = [[pivals(theta[i][j]) for j in range(4)] for i in range(3)]
    #print(pis)
    while ((not is_terminal) and count<100):
      #print("  step", count)
      act = randmax(pis[row][col])
      row, col = succ(row, col, act)
      #print("state ", row, col, act)
      reward = -0.04
      if ((row, col)==(1,3)):
        is_terminal = True
        reward = -1
      elif ((row, col) == (2, 3)):
        is_terminal = True
        #print("happy")
        reward = 1
      #reward = reward - 0.04
      #reward = reward - 0.04
      #print("reward  ",reward)
      rewards[row][col] = (rewards[row][col] * counter[row][col] + reward)/(counter[row][col])
      traversal.append(act)
      traversal.append(row)
      traversal.append(col)
      traversal.append(reward)
      count = count+1
    sz = len(traversal)
    ind = 1
    treward = reward
    #rewards = [[0]*4]*3
    while (ind+3<=sz):
      reward = traversal[-ind]
      col = traversal[-ind-1]
      row = traversal[-ind-2]
      action = traversal[-ind-3]
      ind = ind + 4
      temp = [0] * 4
      #rewards[row][col] = max(reward, rewards[row][col])
      #print(traversal)
      temp[action] = 1
      #print("state ",row,col)
      pivalst = pivals(theta[row][col])
      #print(pivalst)
      theta[row][col] =  [(theta[row][col][k] + alpha * (temp[k] - pivalst[k]) * rewards[row][col]) for k in range(4)]
      #print(theta)

      #print(pis)
    cumreward = (cumreward * episode + treward)/(episode + 1)
    print("    cum. reward", cumreward)
    #print("    reward",reward)
    #print("    pis", pis)
