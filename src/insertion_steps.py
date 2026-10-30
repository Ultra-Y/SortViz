'''def insertion_steps(arr):
    sort = []
    for item in arr:
        pos = len(sort)
        for i in range(len(sort)):
            if sort[i] > item:
                pos = i
                break
        sort.insert(pos, item)
    return sort
'''
def insertion_steps(arr):
    pos = len(arr)
    a = list(arr)
    for j in range(pos):
        while j > 0:
            yield ("compare", j-1,j)
            if a[j-1] > a[j]:
                a[j], a[j-1] = a[j-1], a[j]
                yield ("swap", j-1,j)
                j = j - 1
            else:
                break
    yield ("done",)


