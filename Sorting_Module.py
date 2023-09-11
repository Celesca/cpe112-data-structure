def bubbleSort(seq):
    n = len(seq) - 1
    for i in range(n,0,-1): 
        for j in range(i):
            if seq[j] > seq[j+1]:
                seq[j], seq[j+1] = seq[j+1], seq[j]
    return seq

def selectionSort(seq):
    n = len(seq)
    for i in range(n-1):
        smallNdx = i
        for j in range(i+1, n):
            if seq[j] < seq[smallNdx]:
                smallNdx = j
        if smallNdx != i:
            seq[i], seq[smallNdx] = seq[smallNdx], seq[i]
    return seq 

def insertionSort(seq):
    n = len(seq)
    for i in range(1, n):
        value = seq[i]
        pos = i
        while pos > 0 and value < seq[pos - 1]:
            seq[pos] = seq[pos - 1]
            pos -= 1
        seq[pos] = value
    return seq