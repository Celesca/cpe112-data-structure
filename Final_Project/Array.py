import ctypes

class Array :
    # Creates an array with size elements.
    def __init__ (self , size):
        assert size > 0 , "Array size must be > 0"
        self._size = size # Instant Variables
        
        # Create the array structure using the ctypes module.
        PyArrayType = ctypes.py_object * size
        # elements = [ , , , ,]
        self._elements = PyArrayType()
        # Initialize each element กำหนดค่าให้ทุกตัวเป็น None
        self.clear ( None )
    
    # length of list
    def __len__(self):
        return self._size
    
    # (Getter) Gets the contents of the index element. 
    def __getitem__ ( self , index) :
        assert index >= 0 and index < len(self) , "Array subscript out of range"
        return self._elements[ index ]
    
    # (Setter) Puts the value in the array element at index position
    def __setitem__ ( self , index , value):
        assert index >= 0 and index < len(self) , "Array subscript out of range"
        self._elements[ index ] = value

    # Clears the array by setting each element to the given value
    def clear(self , value):
        for i in range(len(self)):
            self._elements[i] = value

    # Represent value (string)
    def __repr__(self):
        s = '[ '
        for x in self._elements:
            s = s + str(x) + ", "
        s = s[:-2] + " ]"# เอาทั้งชุดจนถึงตำแหน่ง -2
        return s
    
    # เมื่อมีการเรียก Iteration มันจะเหมือนกับ init เหมือนกับของตัวคลาสนี้
    def __iter__(self):
        self._curIndex = 0
        return self
    
    def __next__(self):
        # Index ตัวปัจจุบัน ยังไม่ถึง Maximum
        if self._curIndex < len(self._elements): 
            entry = self._elements[self._curIndex]
            self._curIndex += 1
            return entry
        else:
            raise StopIteration


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
    
    # Assign value to Every Index
    def clear(self,value):
        # ใช้ของ Class Array มาช่วย
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
        return s[:-1] # เพราะตัวสุดท้ายเป็น \n ให้ลบออก