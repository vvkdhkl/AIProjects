def moveN(x_,y_):
  return(x_-1,y_)

def moveS(x_,y_):
  return(x_+1,y_)

def moveE(x_,y_):
  return(x_,y_+1)

def moveW(x_,y_):
  return(x_,y_-1)

def heur(x_,y_):
  global goalX,goalY
  return(((x_-goalX)**2+(y_-goalY)**2)**.5)

def getMove(x1_,y1_,x2_,y2_):
  if moveN(x1_,y1_)==(x2_,y2_):
      return('N')
  elif moveS(x1_,y1_)==(x2_,y2_):
      return('S')
  elif moveE(x1_,y1_)==(x2_,y2_):
      return('E')
  elif moveW(x1_,y1_)==(x2_,y2_):
      return('W')
  else:
      return(None)

def moves(x_, y_):
  allowed=list()
  if y_>0:
      allowed.append(moveW(x_,y_))
  if x_<11:
      allowed.append(moveS(x_,y_))
  if x_>0:
      allowed.append(moveN(x_,y_))
  if y_<11:
      allowed.append(moveE(x_,y_))
  return(allowed)

def getNext(x_, y_):
  global maze
  poss = moves(x_,y_)
  nextS = filter(lambda p: maze[p[0]][p[1]] is not True, poss)
  return(nextS)

astar_type = 1 #use 0 for basic, 1 for dynamic A* algorithm

goalX = 11
goalY = 11
origX = 0
origY = 0

file = open('map.txt','r')

maze=list()
for line in file:
    tmp = [bool(int(ch)) if not ch=='\n' else None for ch in line]
    maze.append(list(filter(lambda x: x is not None, tmp)))

stateQ = [((origX,origY),heur(origX, origY), 0)]

opened = 1
path = {}
costdict = {}

while (len(stateQ)>0 and not( stateQ[0][0] == (goalX, goalY)) and opened<100000 ):
  opened += 1

  currX, currY = stateQ[0][0]
  cost = stateQ[0][2]
  costdict[(currX,currY)] = cost


  stateQ = list(stateQ[1:])

  nextStates = list(getNext(currX,currY))
  for state in nextStates:

    fn = (cost+1) + heur(state[0], state[1])

    if astar_type == 0:
        stateQ.append((state, fn, cost+1))
        path[state] = (currX, currY)
    else:
        if state not in costdict:
            path[state] = (currX, currY)
            stateQ.append((state, fn, cost+1))
            costdict[state] = cost+1
        else:
             if (cost+1)<costdict[state]:

                 stateQ.remove((state, costdict[state]+heur(state[0], state[1]), costdict[state] ))
                 costdict[state] = cost+1
                 stateQ.append((state, fn, cost+1))
                 path[state] = (currX, currY)

  stateQ.sort(key = lambda x: x[1])
  
print(opened)
if astar_type == 1:
    thisState = (goalX, goalY)
    pathlist = []

    while not thisState==(origX,origY):
        if thisState in moves(path[thisState][0], path[thisState][1]):
            pathlist.append(thisState)
        thisState = path[thisState]
    pathlist.append(thisState)
    pathstr = ''
    pathlist = list(reversed(pathlist))
    for k in pathlist[:-1]:
        pathstr = pathstr + getMove(k[0],k[1],pathlist[pathlist.index(k)+1][0],pathlist[pathlist.index(k)+1][1])
    print(pathstr)
