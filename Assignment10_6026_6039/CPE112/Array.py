# %%
import ctypes

class Array:
    def __init__(self,size):
        assert size > 0, "Array size must be > 0"
        self._size = size
        PyArrayType = ctypes.py_object*size
        self._elements = PyArrayType()
        self.clear(None)
                
    def __len__(self):
        return self._size

    def __getitem__(self,index):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        return self._elements[index]

    def __setitem__(self,index,value):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        self._elements[index] = value

    def clear(self,value):
        for i in range(len(self)):
            self._elements[i] = value
    
    #def __str__(self):
            
    def __repr__(self):
        s = '[ '
        for x in self._elements:
            s = s + str(x) + ', '
        s = s[:-2] + ' ]'
        return s
    
    def __iter__(self):
        self._curIndex = 0
        return self

    def __next__(self):
        if self._curIndex < len(self._elements):
            entry = self._elements[self._curIndex]
            self._curIndex += 1
            return entry
        else:
            raise StopIteration  

# %% [markdown]
# 

# %%
class Array2D:
    def __init__(self,numRows,numCols):
        self._theRows = Array(numRows)
        for i in range(numRows):
            self._theRows[i] = Array(numCols)
            
    def numRows(self):
        return len(self._theRows)

    def numCols(self):
        return len(self._theRows[0])
    
    def clear(self,value):
        for row in self._theRows:
            row.clear(value)

    def __getitem__(self,indexTuple):
        assert len(indexTuple) == 2, "Invalid number of array subscripts."
        row = indexTuple[0]
        col = indexTuple[1] 
        assert (row >= 0) and (row < self.numRows()) and (col >= 0) and (col < self.numCols()), "Array subscript out of range."
        return self._theRows[row][col]
            
    def __setitem__( self, indexTuple, value ):
        assert len(indexTuple) == 2, "Invalid number of array subscripts."
        row = indexTuple[0]
        col = indexTuple[1]
        assert row >= 0 and row < self.numRows() and col >= 0 and col < self.numCols(), "Array subscript out of range."
        self._theRows[row][col] = value
    
    def __repr__(self):
        s = ''
        for i in self._theRows:
            s += str(i) + '\n'
        return s[:-1]

# %% [markdown]
# 

# %%
class Matrix(Array2D):
       
    def scaleBy(self,scalar):
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                self[r,c] *= scalar
                
    # Creates and returns a new matrix that is the transpose of this matrix.
    def transpose(self):
        newMatrix = Matrix(self.numCols(),self.numRows())
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                newMatrix[c,r] = self[r,c]
        return newMatrix
    
    def __add__(self,rhsMatrix):
        assert (rhsMatrix.numRows() == self.numRows()) and (rhsMatrix.numCols() == self.numCols()), \
        "Matrix sizes not compatible for the add operation."
        newMatrix = Matrix(self.numRows(),self.numCols())
        for r in range(self.numRows()) :
            for c in range(self.numCols()) :
                newMatrix[r,c] = self[r,c] + rhsMatrix[r,c]
        return newMatrix

    # Creates and returns a new matrix that results from matrix subtraction.
    def __sub__(self,rhsMatrix):
        assert (rhsMatrix.numRows() == self.numRows()) and (rhsMatrix.numCols() == self.numCols()), \
        "Matrix sizes not compatible for the substract operation."
        newMatrix = Matrix(self.numRows(),self.numCols())
        for r in range(self.numRows()) :
            for c in range(self.numCols()) :
                newMatrix[r,c] = self[r,c] - rhsMatrix[r,c]
        return newMatrix

    
    # Creates and returns a new matrix resulting from matrix multiplication.
    def __mul__(self, rhsMatrix):
        assert (rhsMatrix.numRows() == self.numCols()),\
        "Matrix sizes not compatible for the multplication operation."
        newMatrix = Matrix(self.numRows(),rhsMatrix.numCols())
        newMatrix.clear(0)
        for r in range(newMatrix.numRows()):
            for c in range(newMatrix.numCols()):
                for i in range(self.numCols()):
                    newMatrix[r,c] += self[r,i] * rhsMatrix[i,c]
        return newMatrix
        

# %% [markdown]
# 


