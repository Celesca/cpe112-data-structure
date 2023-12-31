class PriorityQueueBase:
    # Abstract base class for a priority queue.
    class Item:
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key  # compare items based on their keys

        def is_empty(self):  # concrete method assuming abstract len
            return len(self) == 0
# -------------------------------------------


class HeapPriorityQueue(PriorityQueueBase):  # base class defines Item
    # Use Heap to implement PriorityQueue
    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        return 2*j + 1

    def _right(self, j):
        return 2*j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)  # index beyond end of list?

    def _has_right(self, j):
        return self._right(j) < len(self._data)  # index beyond end of list?

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _siftup(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._siftup(parent)  # recur at position of parent

    def _siftdown(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left  # although right may be smaller
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._siftdown(small_child)  # recur at position of small child

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):  # concrete method assuming abstract len
        return len(self) == 0

    def add(self, key, value):
        self._data.append(self.Item(key, value))
        self._siftup(len(self._data) - 1)  # upheap newly added position

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        self._swap(0, len(self._data) - 1)  # put minimum item at the end
        item = self._data.pop()  # and remove it from the list;
        self._siftdown(0)  # then fix new root
        return (item._key, item._value)
# ---------------------------------------------------------------------------------


class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    # A locator-based priority queue implemented with a binary heap.
    # ------------------------------ nested Locator class --------------------------
    class Locator(HeapPriorityQueue.Item):
        # Token for locating an entry of the priority queue.
        __slots__ = '_index'  # add index as additional field

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j
# ------------------------------ nonpublic behaviors ------------------------------
# override swap to record new indices

    def _swap(self, i, j):
        super()._swap(i, j)  # perform the swap
        self._data[i]._index = i  # reset locator index (post-swap)
        self._data[j]._index = j  # reset locator index (post-swap)

    def _bubble(self, j):
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._siftup(j)
        else:
            self._siftdown(j)

    def add(self, key, value):
        # Add a key-value pair
        token = self.Locator(key, value, len(self._data))  # initiaize locator index
        self._data.append(token)
        self._siftup(len(self._data) - 1)
        return token

    def update(self, loc, newkey, newval):
        # Update the key and value for the entry identified by Locator loc
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        loc._key = newkey
        loc._value = newval
        self._bubble(j)

    def remove(self, loc):
        # Remove and return the (k,v) pair identified by Locator loc.”””
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        if j == len(self) - 1:  # item at last position
            self._data.pop()  # just remove it
        else:
            self._swap(j, len(self)-1)  # swap item to the last position
            self._data.pop()  # remove it from the list
            self._bubble(j)  # fix item displaced by the swap
        return (loc._key, loc._value)
