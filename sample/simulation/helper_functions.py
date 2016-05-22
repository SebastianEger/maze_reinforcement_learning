def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

if __name__ == '__main__':
    a = [0, 2, 1, 0]
    b = [i[0] for i in sorted(enumerate(a), key=lambda x:x[1])]
    print b