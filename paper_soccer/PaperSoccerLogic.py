import numpy as np
class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        w = width+1
        h = height+1
        wh = w*h
        self.size = wh+6
        
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.matrixNodes = [0] * self.size
        for i in range(wh):
            x = i//h
            y = i%h
            self.matrix[i][i] = (x<<8)+y
            
        self.matrix[wh][wh] = ((width//2-1)<<8) + 0xFF
        self.matrix[wh+1][wh+1] = ((width//2)<<8) + 0xFF
        self.matrix[wh+2][wh+2] = ((width//2+1)<<8) + 0xFF
        self.matrix[wh+3][wh+3] = ((width//2-1)<<8) + h
        self.matrix[wh+4][wh+4] = ((width//2)<<8) + h
        self.matrix[wh+5][wh+5] = ((width//2+1)<<8) + h
        
        for i in range(self.size):
            self.makeNeighbours(i)
            
        self.removeAdjacency(wh,h*(width//2-2))
        self.removeAdjacency(wh+2,h*(width//2+2))
        self.removeAdjacency(wh+3,h*(width//2-1)-1)
        self.removeAdjacency(wh+5,h*(width//2+3)-1)
        
        for i in range(wh-1):
            for j in range(i+1,wh):
                x, y = self.getPosition(i)
                x2, y2 = self.getPosition(j)
                
                if x == 0 and x2 == 0 and self.distance(x,y,x2,y2) <= 1: self.addEdge(i,j)
                elif x == width and x2 == width and self.distance(x,y,x2,y2) <= 1: self.addEdge(i,j)
                elif y == 0 and y2 == 0 and self.distance(x,y,x2,y2) <= 1:
                    if x < width//2 - 1 or x >= width//2+1: self.addEdge(i,j)
                elif y == height and y2 == height and self.distance(x,y,x2,y2) <= 1:
                    if x < width//2 - 1 or x >= width//2+1: self.addEdge(i,j)
                    
        self.addEdge(wh,wh+1);
        self.addEdge(wh+1,wh+2);
        self.addEdge(wh,h*(width//2-1));
        self.addEdge(wh+2,h*(width//2+1));
        self.addEdge(wh+3,wh+4);
        self.addEdge(wh+4,wh+5);
        self.addEdge(wh+3,h*(width//2)-1);
        self.addEdge(wh+5,h*(width//2+2)-1);
        
        self.matrixNeighbours = []
        
        for i in range(self.size):
            n = self.getNeighbours(i)
            self.matrixNeighbours.append(n)
            self.matrixNodes[i] |= len(n) << 4
            
        
        self.goalArray = [0] * self.size
        self.almostGoalArray = [0] * self.size
        self.cutOffGoalArray = [0] * self.size
        
        for i in range(wh,self.size):
            self.goalArray[i] = (i-wh)/3 + 1
            self.almostGoalArray[i] = (i-wh)/3 + 1
            self.cutOffGoalArray[i] = (i-wh)/3 + 1
            
        self.almostGoalArray[h*(width//2-1)] = 1
        self.almostGoalArray[h*(width//2+1)] = 1
        self.almostGoalArray[h*(width//2)-1] = 2
        self.almostGoalArray[h*(width//2+2)-1] = 2
                             
        self.cutOffGoalArray[h*(width//2-1)] = 1
        self.cutOffGoalArray[h*(width//2)] = 1
        self.cutOffGoalArray[h*(width//2+1)] = 1
        self.cutOffGoalArray[h*(width//2)-1] = 2
        self.cutOffGoalArray[h*(width//2+1)-1] = 2
        self.cutOffGoalArray[h*(width//2+2)-1] = 2
    
        self.ball = width//2 * h + h//2;
        
        #self.matrix[self.ball][self.ball] = 3
        
    def distance(self,x,y,x2,y2):
        return int(((x-x2)**2 + (y-y2)**2)**0.5)
        
    def makeNeighbours(self,index):
        x, y = self.getPosition(index)
        
        for i in range(self.size):
            if i == index: continue
            x2, y2 = self.getPosition(i)
            if self.distance(x,y,x2,y2) <= 1:
                self.matrixNodes[i] += 1
                self.matrix[i][index] = 1
                self.matrix[index][i] = 1
            
    
    def getPosition(self,index):
        x = (self.matrix[index][index]>>8)&0xFF;
        y = self.matrix[index][index]&0xFF;
        if y == 0xFF: y = -1;
        return (x,y);
    
    def removeAdjacency(self,a,b):
        self.matrixNodes[a] -= 1
        self.matrixNodes[b] -= 1
        self.matrix[a][b] = 0
        self.matrix[b][a] = 0
        
    def addEdge(self,a,b):
        self.matrix[a][b] = 2
        self.matrix[b][a] = 2
        self.matrixNodes[a] -= 1
        self.matrixNodes[b] -= 1
    
    def removeEdge(self,a,b):
        self.matrix[a][b] = 1
        self.matrix[b][a] = 1
        self.matrixNodes[a] += 1
        self.matrixNodes[b] += 1
        
    def getNeighbours(self,index):
        n = []
        for i in range(self.size):
            if i == index: continue
            if self.matrix[index][i] > 0: n.append(i)
        return n
    
    def getDistanceChar(self,a,b):
        x1, y1 = self.getPosition(a)
        x2, y2 = self.getPosition(b)
        dx = x2-x1
        dy = y2-y1
        if dx == 0:
            if dy == -1: return "0"
            return "4"
        elif dx == 1:
            if dy == -1: return "1"
            if dy == 0: return "2"
            return "3"
        else:
            if dy == -1: return "7"
            if dy == 0: return "6"
            if dy == 1: return "5"
        return ""
    
    def getFreeNeighbours(self,index):
        n = self.matrixNodes[index]&0x0F
        i = 0; j = 0
        ns = [0] * n
        while j < n:
            if self.matrix[index][self.matrixNeighbours[index][i]] == 1:
               ns[j] = self.matrixNeighbours[index][i]
               j += 1
            i += 1
        return ns
            
    def passNext(self,index):
        return (self.matrixNodes[index]&0x0F) < (self.matrixNodes[index]>>4)

    def exactlyOne(self,index):
        return (self.matrixNodes[index]&0x0F) == (self.matrixNodes[index]>>4)-1

    def exactlyOneForGoal(self,index):
        return (self.matrixNodes[index]&0x0F) == (self.matrixNodes[index]>>4)-3
   
    def isAlmostBlocked(self,index):
        return (self.matrixNodes[index]&0x0F) <= 1
    
    def isBlocked(self,index):
        return (self.matrixNodes[index]&0x0F) == 0
    
    def hashPaths(self,paths):
        output = 0
        for p in paths:
            if p[0] > p[1]:
                hashCode = (p[0] << 16) + p[1]
            else:
                hashCode = (p[1] << 16) + p[0]
            h = 78901 * hashCode
            h ^= h << 13
            h ^= h >> 17
            h &= 2**64-1
            output += h
        return output
    
    def getMoves(self):
        moves = []
        vertices = []
        pathCycles = []
        blockedMoves = []
        talia = []
        string = ""
        vertices.append(self.ball)
        talia.append((self.ball,[]))
        
        while len(talia) > 0 and len(moves) < 64:
            t = talia[-1][0]
            paths = talia[-1][1]
            talia.pop()
            
            for p in paths:
                string += self.getDistanceChar(p[0],p[1])
                self.addEdge(p[0],p[1])
                vertices.append(p[1])
            
            self.ball = t
                    
            ns = self.getFreeNeighbours(t)            
            for n in ns:
                g = self.goalArray[n]
                if g == 0 and self.passNext(n) and not self.isAlmostBlocked(n):
                    newPaths = paths.copy()
                    newPaths.append((t,n))
                    if n in vertices:
                        newPathsHash = self.hashPaths(newPaths)
                        if newPathsHash not in pathCycles:
                            pathCycles.append(newPathsHash)
                            talia.append((n,newPaths))
                    else:
                        talia.append((n,newPaths))
                else:
                    self.addEdge(t,n)
                    self.ball = n
                    if g == 0 and self.isBlocked(n):
                        newPaths = paths.copy()
                        newPaths.append((t,n))
                        newPathsHash = self.hashPaths(newPaths)
                        if newPathsHash in blockedMoves:
                            self.removeEdge(t,n)
                            self.ball = t
                            continue
                        blockedMoves.append(newPathsHash)
                    self.removeEdge(t,n)
                    self.ball = t
                    string += self.getDistanceChar(t,n)
                    moves.append(string)
                    string = string[:len(string)-1]
                    if len(moves) >= 64:
                        break
            
            vertices = vertices[:1]
            string = ""
            for p in paths:
                self.removeEdge(p[0],p[1])
            self.ball = vertices[0]
        
        return moves
    
    def getMatrix(self):
        matrix = [[0 for _ in range(2*self.width+1)] for _ in range(2*self.height+5)]
        for edge in self.getEdges():
            a = edge[0]
            b = edge[1]

            if a[0] < b[0]:
                if a[1] > b[1]:
                    x = 2 * b[0]
                    y = 2 * b[1] + 2
                    matrix[y][x] = 1
                else:
                    x = (2 * a[0] + 2 * b[0]) // 2
                    y = (2 * a[1] + 2 * b[1]) // 2 + 2
                    matrix[y][x] = 1
            elif b[0] < a[0]:
                if b[1] > a[1]:
                    x = 2 * a[0]
                    y = 2 * a[1] + 2
                    matrix[y][x] = 1
                else:
                    x = (2 * a[0] + 2 * b[0]) // 2
                    y = (2 * a[1] + 2 * b[1]) // 2 + 2
                    matrix[y][x] = 1
            else:
                x = (2 * a[0] + 2 * b[0]) // 2
                y = (2 * a[1] + 2 * b[1]) // 2 + 2
                matrix[y][x] = 1
        return np.copy(matrix)

    def getIndexByPosition(self,x,y):
        for i in range(self.size):
            mx = (self.matrix[i][i]>>8) & 0xFF;
            my = self.matrix[i][i] & 0xFF
            if my == 0xFF: my = -1;
            if x == mx and y == my:
                return i
    
    def setMatrix(self,matrix):
        for x in range(2*self.width+1):
            for y in range(2*self.height+5):
                if matrix[y][x] == 1:
                    if x % 2 == 0 and y % 2 == 0:
                        i = self.getIndexByPosition(x // 2 - 1, (y - 2) // 2 + 1)
                        j = self.getIndexByPosition(x // 2, (y - 2) // 2)
                        if (self.matrix[i][j] & 2) == 0: self.addEdge(i,j)
                    elif x % 2 == 1 and y % 2 == 0:
                        i = self.getIndexByPosition((x-1)//2, (y-2)//2)
                        j = self.getIndexByPosition((x+1)//2, (y-2)//2)
                        if (self.matrix[i][j] & 2) == 0: self.addEdge(i,j)
                    elif x % 2 == 0 and y % 2 == 1:
                        i = self.getIndexByPosition(x//2, (y-2-1)//2)
                        j = self.getIndexByPosition(x//2, (y-2+1)//2)
                        if (self.matrix[i][j] & 2) == 0: self.addEdge(i,j)
                    else:
                        i = self.getIndexByPosition((x-1)//2, (y-2-1)//2)
                        j = self.getIndexByPosition((x+1)//2, (y-2+1)//2)
                        if (self.matrix[i][j] & 2) == 0: self.addEdge(i,j)

        if self.passNext(self.width//2 * (self.height+1) + (self.height+1)//2):
            for i in range(self.size-6, self.size):
                if self.exactlyOneForGoal(i):
                    self.ball = i
                    return
            for i in range(self.size):
                if i == self.width//2 * (self.height+1) + (self.height+1)//2: continue
                if i > self.size-6: continue
                if self.exactlyOne(i):
                    self.ball = i
                    return
            for i in range(self.size):
                if i == self.width//2 * (self.height+1) + (self.height+1)//2: continue
                if i > self.size-6: continue
                if self.isBlocked(i):
                    self.ball = i
                    return
    
    def getNeighbour(self,dx,dy):
        x, y = self.getPosition(self.ball)
        for n in self.matrixNeighbours[self.ball]:
            x2, y2 = self.getPosition(n)
            if x+dx == x2 and y+dy == y2:
                return n
        return -1
    
    def nextNode(self,c):
        if c == "5": return self.getNeighbour(-1,1)
        elif c == "4": return self.getNeighbour(0,1)
        elif c == "3": return self.getNeighbour(1,1)
        elif c == "6": return self.getNeighbour(-1,0)
        elif c == "2": return self.getNeighbour(1,0)
        elif c == "7": return self.getNeighbour(-1,-1)
        elif c == "0": return self.getNeighbour(0,-1)
        elif c == "1": return self.getNeighbour(1,-1)
        return -1
        
    def doMove(self,move):
        for m in move:
            n = self.nextNode(m)
            self.addEdge(self.ball,n)
            self.ball = n
            
    def getWinner(self, currentPlayer):
        g = self.goalArray[self.ball]
        if g > 0:
            if currentPlayer == 1:
                if g == 1: return -1
                return 1
            else:
                if g == 1: return 1
                return -1
        if self.isBlocked(self.ball):
            return -currentPlayer
        return 0
    
    def __str__(self):
        matrix = self.getMatrix()
        out = str(self.ball)+"|"
        for i in range(self.size):
            line = ""
            for j in range(i+1):
                out += str(matrix[i][j])
        return out

    def getEdges(self):
        edges = []
        for i in range(1,self.size):
            for j in range(i):
                if (self.matrix[i][j] & 2) > 0:
                    edge = (self.getPosition(i), self.getPosition(j))
                    edges.append(edge)
        return edges

