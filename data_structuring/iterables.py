def intersection(it1, it2):
    '''
    Return list of intersecting elements. (Tired of writing this code out)
    
    it1 - iterable able to be casted into a set
    it2 - iterable able to be casted into a set
    '''
    return (list(set(it1).intersection(set(it2))))

def find_duplicates(x):
    '''
    Return list of elements appearing more than once
    
    x - iterable
    '''
    a = set()
    repeated = set()
    
    for element in x:
        if element in a:
           repeated.add(element)
        else:
           a.add(element)

    return (list(repeated))
