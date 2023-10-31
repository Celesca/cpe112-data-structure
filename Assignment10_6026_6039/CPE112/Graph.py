from CPE112.Array import Matrix


class Graph:
    def __init__(self, maxVertices, directed=False):
        self._Vertices = list()
        self._MATRIX = Matrix(maxVertices, maxVertices)
        self._MATRIX.clear(None)
        self._directed = directed
# ------------------------- Vertex class -----------------------

    class Vertex:
        __slots__ = '_element'

        def __init__(self, x):
            self._element = x

        def element(self):
            return self._element

        def __repr__(self):
            return str(self._element)
# ------------------------- Edge class -------------------------

    class Edge:
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, w):
            self._origin = u
            self._destination = v
            self._element = w

        def endpoints(self):
            return (self._origin, self._destination)

        def opposite(self, v):
            return self._destination if v is self._origin else self._origin

        def element(self):
            return self._element

        def __repr__(self):
            return str(self._element)
# -----------------------------------------------------------

    def is_directed(self):
        return self._directed

    def findindex(self, v):
        if v in self._Vertices:
            return self._Vertices.index(v)
# -------------------------------------------------------------------------

    def vertex_count(self):
        return len(self._Vertices)

    def vertices(self):
        return self._Vertices

    def edge_count(self):
        total = 0
        for row in range(self.vertex_count()):
            for col in range(self.vertex_count()):
                if self._MATRIX[row, col] is not None:
                    total += 1
        return total if self.is_directed() else total // 2

    def edges(self):
        edges_list = list()
        for row in range(self.vertex_count()):
            for col in range(self.vertex_count()):
                if (self._MATRIX[row, col] not in edges_list) and (self._MATRIX[row, col] is not None):
                    edges_list.append(self._MATRIX[row, col])
        return edges_list

    def get_edge(self, u, v):
        return self._MATRIX[self.findindex(u), self.findindex(v)]

    def degree(self, v, outgoing=True):
        total = 0
        if outgoing:
            for col in range(self.vertex_count()):
                if self._MATRIX[self.findindex(v), col] is not None:
                    total += 1
        # incoming
        else:
            for row in range(self.vertex_count()):
                if self._MATRIX[row, self.findindex(v)] is not None:
                    total += 1

        return total

    def incident_edges(self, v, outgoing=True):
        adj = list()
        if outgoing:
            for col in range(self.vertex_count()):
                if self._MATRIX[self.findindex(v), col] is not None:
                    adj.append(self._MATRIX[self.findindex(v), col])
        # incoming
        else:
            for row in range(self.vertex_count()):
                if self._MATRIX[row, self.findindex(v)] is not None:
                    adj.append(self._MATRIX[row, self.findindex(v)])
        return adj

    def insert_vertex(self, x):
        v = self.Vertex(x)
        self._Vertices.append(v)
        return v

    def insert_edge(self, u, v, x):
        # u is origin
        # v is destination
        e = self.Edge(u, v, x)
        if self.is_directed():
            self._MATRIX[self.findindex(u), self.findindex(v)] = e
        else:
            self._MATRIX[self.findindex(u), self.findindex(v)] = e
            self._MATRIX[self.findindex(v), self.findindex(u)] = e
        return e

###################### Assignment 1 #############################

    def remove_vertex(self,v):
        assert v in self.vertices() ,"There is no this vertex in graph"
        if self.incident_edges(v):
            TEMP_MATRIX = Matrix(self._MATRIX.numRows(),self._MATRIX.numCols())
            TEMP_MATRIX.clear(None)
            R, C = 0, 0
            for row in [ r for r in range(self._MATRIX.numRows()) if r != self.findindex(v)]:
                for col in [ c for c in range(self._MATRIX.numCols()) if c != self.findindex(v)]:
                    TEMP_MATRIX[R,C] = self._MATRIX[row,col]
                    C += 1
                C = 0
                R += 1
            self._MATRIX = TEMP_MATRIX
        self._Vertices.pop(self.findindex(v))
        del(v)
        
    def remove_edge(self,e):
        assert e in self.edges(), "There is no this edge in graph"
        if self.is_directed():
            self._MATRIX[self.findindex(e.endpoints()[0]),self.findindex(e.endpoints()[1])] = None
        else:
            self._MATRIX[self.findindex(e.endpoints()[0]),self.findindex(e.endpoints()[1])] = None
            self._MATRIX[self.findindex(e.endpoints()[1]),self.findindex(e.endpoints()[0])] = None
        del(e)

    ##################################################################
    ###################### Assignment 2 #############################
    
    def DFS(self,u,discovered = {}):
        #print(u)
        if not discovered:
            discovered[u] = None
        for e in self.incident_edges(u):
            v = e.opposite(u)
            if v not in discovered:
                discovered[v] = e
                self.DFS(v,discovered)
        return discovered


    def BFS(self, s):
        discovered = {s:None}
        level = [s]
        while len(level) > 0:
            next_level= []
            for u in level:
                #print(u)
                for e in self.incident_edges(u):
                    v = e.opposite(u)
                    if v not in discovered:
                        discovered[v] = e
                        next_level.append(v)
                level = next_level
        return discovered
    
    ################################################################## 
    def __repr__(self):
        s = '['
        for r in range(self._MATRIX.numRows()):
            for c in self._MATRIX._theRows[r]:
                if c is None:
                    c = 0
                s = s + str(c) + ', '
            s = s[:-2] + ' \n '
        s = s[:-3] + ' ]'
        return s

###################### Assignment 3 #############################
def Warshall(g):
    # Change the Adjacency matrix to reachablity matrix 
    R = Matrix(g.vertex_count(),g.vertex_count())
    for r in range(R.numRows()):
        for c in range(R.numCols()):
            if g._MATRIX[r,c]:
                R[r,c] = 1
            else:
                R[r,c] = 0

    # Warshall algorithm
    for k in range(g.vertex_count()):
        for i in range(g.vertex_count()):
            for j in range(g.vertex_count()):
                if R[i,j] or (R[i,k] and R[k,j]):
                    R[i,j] = 1 # Update R
    return R
##################################################################    