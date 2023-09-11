import ctypes

# Array

class Array :
    def __init__ (self , size) :
        assert size > 0 , "Array size must be > 0"
        self._size = size 
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        self.clear ( None )

    def __len__(self):
        return self._size
    
    def __getitem__ ( self , index) :
        assert index >= 0 and index < len(self) , "Array subscript out of range"
        return self._elements[ index ]
    
    def __setitem__ ( self , index , value):
        assert index >= 0 and index < len(self) , "Array subscript out of range"
        self._elements[ index ] = value

    def clear(self , value):
        for i in range(len(self)):
            self._elements[i] = value

    def __repr__(self):
        s = '[ '
        for x in self._elements:
            s = s + str(x) + ", "
        s = s[:-2] + " ]"
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
        

# Array 2D 

class Array2D(Array):
    def __init__(self,numRows,numCols):
        self._theRows = Array(numRows)
        for i in range(numRows):
            self._theRows[i] = Array(numCols)

    # Getter (receive tuple)
    def __getitem__(self,indexTuple):
        assert len(indexTuple) == 2, "Invalid number of array subscripts."
        row = indexTuple[0]
        col = indexTuple[1]
        assert (row >= 0) and (row < self.numRows()) and (col >= 0) and (col < self.numCols()) , \
                "Array subscript out of range."
        return self._theRows[row][col]
        
    def __setitem__(self , indexTuple, value):
        assert len(indexTuple) == 2, "Invalid number of array subscripts."
        row = indexTuple[0]
        col = indexTuple[1]
        assert (row >= 0) and (row < self.numRows()) and (col >= 0) and (col < self.numCols()) \
            , "Array subscript out of range."
        self._theRows[row][col] = value

    def numRows(self):
        return len(self._theRows)
    
    def numCols(self):
        return len(self._theRows[0])
    
    def clear(self,value):
        for row in self._theRows:
            row.clear(value)

    def __repr__(self):
        '''
        Output
        [1,2,3,4]
        [5,6,7,8]
        '''
        
        s = ''
        for row in self._theRows:
            s += str(row) + '\n'
        return s[:-1]


# Matrix 

class Matrix(Array2D):
    
    def scaleBy(self,scalar):
        for i in range( self.numRows()):
            for j in range( self.numCols()):
                self[i,j] *= scalar

    
    def transpose(self):
        newMatrix = Matrix(self.numCols() , self.numRows())
        for i in range( self.numRows()):
            for j in range( self.numCols()):
                newMatrix[j,i] = self[i,j]
        return newMatrix

    def __add__ ( self , rhsMatrix ) :
        assert rhsMatrix.numRows() == self.numRows() and rhsMatrix.numCols() == self.numCols() ,\
            "Matrix size not compatible for the add operation."
        newMatrix = Matrix( self.numRows() , self.numCols() )
        for i in range( self.numRows() ):
            for j in range( self.numCols() ) :
                newMatrix[i,j] = self[i,j] + rhsMatrix[i,j]
        return newMatrix
        
    def __sub__ ( self , rhsMatrix ) :
        assert rhsMatrix.numRows() == self.numRows() and rhsMatrix.numCols() == self.numCols() ,\
            "Matrix size not compatible for the add operation."
        newMatrix = Matrix( self.numRows() , self.numCols() )
        for i in range( self.numRows() ):
            for j in range( self.numCols() ) :
                newMatrix[i,j] = self[i,j] - rhsMatrix[i,j]
        return newMatrix
    
    def __mul__(self,rhsMatrix):
        assert self.numCols() == rhsMatrix.numRows() , "Cannot multiply these matrices."
        newMatrix = Matrix( self.numRows() , rhsMatrix.numCols())
        for i in range(self.numRows()):
            for j in range(rhsMatrix.numCols()):
                total = 0 
                for k in range(rhsMatrix.numRows()):
                     total += self[i,k] * rhsMatrix[k,j]
                newMatrix[i,j] = total
        return newMatrix
    
# Stack with List 

class Stack:
    def __init__(self):
        self._theItems = list()

    def isEmpty(self):
        return len(self) == 0
    
    def __len__(self):
        return len(self._theItems)
    
    def peek(self):
        assert not self.isEmpty() , "Cannot peek at an empty stack"
        return self._theItems[-1]

    def pop(self):
        assert not self.isEmpty() , "Cannot pop at an empty stack"
        return self._theItems.pop()

    def push(self,item):
        self._theItems.append(item)

    def __repr__(self):
        s =""
        for item in reversed(self._theItems):
            s =  s + "| "+str(item) +"\t|" + "\n"
        s = s + "---------"
        return s
    
# Queue with List

class Queue :
    def __init__(self):
        self._qList = list()

    def isEmpty(self): 
        return len(self) == 0

    def __len__(self): 
        return len(self._qList)

    def enqueue(self,item): 
        self._qList.append(item)

    def dequeue(self):
        assert not self.isEmpty(), "Cannot dequeue from an empty queue"
        return self._qList.pop(0)

    def __repr__(self):
        s = ""

        for item in self._qList:
            s = s + "-" * (len(str(item)) + 1 )
        s += "\n"

        for item in self._qList:
            s = s + str(item) + " "

        s += "\n"
        for item in self._qList:
            s = s + "-" * (len(str(item))+1)
        return s

# Queue with Circular Array

class CQueue():
    def __init__(self, maxSize):
        self._count = 0
        self._front = 0
        self._back = maxSize - 1
        self._qArray = Array( maxSize )

    def isEmpty(self):
        return self._count == 0

    def isFull(self):
        return len(self) == len(self._qArray)

    def __len__(self):
        return self._count

    def enqueue(self,item):
        assert not self.isFull() , "Cannot enqueue to a full queue."
        maxSize = len(self._qArray)
        self._back = (self._back + 1) % maxSize
        self._qArray[self._back] = item
        self._count += 1

    def dequeue(self):
        assert not self.isEmpty() , "Cannot dequeue from an empty queue."
        item = self._qArray[self._front] 
        maxSize = len(self._qArray)
        self._qArray[self._front] = None 
        self._front = (self._front + 1) % maxSize
        self._count -= 1
        return item

    def __repr__(self):
        s = str(self._qArray) + "\n"
        s = s + "Front index : " + str(self._front) + "\n"
        s = s + "Back index : " + str(self._back) + "\n"
        return s

# Double Queue (Deque)

class Deque():
    def __init__(self):
        self._dList = []

    def AddFirst(self,item):
        self._dList.insert(0,item)

    def AddRear(self,item):
        self._dList.append(item)

    def DeleteFirst(self):
        assert not self.isEmpty() , "Cannot delete first because the deque is empty."
        return self._dList.pop(0)
    
    def DeleteRear(self):
        assert not self.isEmpty() , "Cannot delete rear because the deque is empty."
        return self._dList.pop()
    
    def First(self):
        assert not self.isEmpty() , "The deque is empty. There's no data in the deque."
        return self._dList[0]
    
    def Rear(self):
        assert not self.isEmpty() , "The deque is empty. There's no data in the deque."
        return self._dList[-1]
    
    def isEmpty(self):
        return len(self._dList) == 0
    
    def __len__(self):
        return len(self._dList)
    
    def __repr__(self):
        s = ""
        # Header
        for item in self._dList:
            s = s + "-" * (len(str(item)) + 1 )
        s += "\n"
        # Content 
        for item in self._dList:
            s = s + str(item) + " "
        # Footer
        s += "\n"
        for item in self._dList:
            s = s + "-" * (len(str(item))+1)
        return s
    
# Link Node and Singly Linked List

class _SLinkNode:
    def __init__(self,item):
        self._item = item
        self._next = None
#-------------------------------
class SLinkedlist:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def prepend(self,item):
        newNode = _SLinkNode(item) #1
        if self.isEmpty():
            self._tail = newNode
        else:
            newNode._next = self._head #2
        self._head = newNode #3
        self._size += 1

    def append(self,item):
        newNode = _SLinkNode(item)
        if self.isEmpty():
            self._head = newNode
        else:
            self._tail._next = newNode
        self._tail = newNode
        self._size += 1

    def __contains__(self, target):
        curNode = self._head
        while curNode is not None and curNode._item != target:
            curNode = curNode._next
        return curNode is not None
    
    def isEmpty(self):
        return len(self) == 0

    def remove(self,item):
        predNode = None
        curNode = self._head
        while curNode is not None and curNode._item != item:
            predNode = curNode
            curNode = curNode._next
            #print("Now predNode is {0} and curNode is {1}".format(predNode._item,curNode._item))
        assert curNode is not None, "The item must be in this linked list"
        self._size -= 1

        if curNode is self._head:
            self._head = curNode._next
        # do not remember if curNode = self._tail
        # shift tail to predNode
        elif curNode is self._tail:
            self._tail = predNode
            self._tail._next = None
        else:
            predNode._next = curNode._next
        return curNode._item

    def __iter__(self):
        self._curNode = self._head
        return self

    def __next__(self):
        if self._curNode is None:
            raise StopIteration
        else:
            item = self._curNode._item
            self._curNode = self._curNode._next
            return item
    
    def __repr__(self):
        curNode = self._head
        s = "["
        while curNode is not None:
            s = s + str(curNode._item)+ "->"
            curNode = curNode._next
        s = s[:-2] + "]"
        return s
    
# Stack with LinkList and Link Node
class Stack(_SLinkNode):
    def __init__(self):
        self._head = None
        self._size = 0

    def isEmpty(self):
        return len(self) == 0
    
    def __len__(self):
        return self._size

    def push(self,item):
        newNode = _SLinkNode(item)
        if self.isEmpty():
            self._head = newNode
        else:
            newNode._next = self._head # เชื่อมต่อ next ของตัวที่ ไปที่ตัวล่าสุด
            self._head = newNode
        self._size += 1

    def pop(self):
        assert not self.isEmpty() , "Cannot pop the empty stack."
        temp = self._head
        self._head = self._head._next
        temp._next = None
        self._size -= 1
        return temp._item
        
    
    def peek(self):
        assert not self.isEmpty() , "Cannot peek the empty stack."
        return self._head._item
    
    def __repr__(self):
        assert not self.isEmpty() , "There's no member to show in stack."
        curNode = self._head
        s = ""
        while curNode is not None:
            s = s + "| \t" + str(curNode._item) + "\t|\n"
            curNode = curNode._next
        s = s + "-----------------"
        return s
        

# Queue with Linked List and Link Node
class LQueue(SLinkedlist,_SLinkNode): # Note ว่า เราจะต้อง Inheritance SLinkedlist ก่อน _SLinkNode เพราะ มันจะเรียกใช้ __init__ จาก left to right
    def enqueue(self,item):
        super().append(item)
    def dequeue(self):
        head_item = self._head._item
        super().remove(head_item)
        return head_item
    def __repr__(self):
        curNode = self._head
        s = "["
        while curNode is not None:
            s = s + str(curNode._item)+ "<-"
            curNode = curNode._next
        s = s[:-2] + "]"
        return s
    
# Doubly Linked List and Doubly List Node

class _DLinkNode(object):
    def __init__(self,item,prev,next):
        self._item = item
        self._prev = prev
        self._next = next

class DLinkedList:
    # Construct an empty Deque.
    def __init__(self):
        self._header = _DLinkNode(None,None,None)
        self._trailer = _DLinkNode(None,None,None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0
    
    def insert_between(self,item,predecessor,successor):
        newNode = _DLinkNode(item,predecessor,successor)
        predecessor._next = newNode
        successor._prev = newNode
        self._size += 1
    
    def delete_node(self,node):
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        item = node._item
        node._prev = node._next = node._item = None
        return item

# Dequeue with Double Linked List
class DDeque(DLinkedList , _DLinkNode):
    def isEmpty(self):
        return len(self) == 0
    
    def __len__(self):
        return self._size
    
    def AddFirst(self,item):
        self.insert_between(item,self._header,self._header._next)

    def AddRear(self,item):
        self.insert_between(item,self._trailer._prev , self._trailer)

    def First(self):
        assert not self.isEmpty() , "The Deque is empty."
        return self._header._next._item

    def Rear(self): 
        assert not self.isEmpty() , "The Deque is empty."
        return self._trailer._prev._item
    
    def DeleteFirst(self):
        assert not self.isEmpty() , "Cannot remove object. The deque is empty."
        return self.delete_node(self._header._next)

    def DeleteRear(self):
        assert not self.isEmpty() , "Cannot remove object. The deque is empty."
        return self.delete_node(self._trailer._prev)

    def __repr__(self):
        curNode = self._header._next
        s = "["
        while curNode is not self._trailer :
            s = s + str(curNode._item)+ "<->"
            curNode = curNode._next
        s = s[:-2] + "]"
        return s