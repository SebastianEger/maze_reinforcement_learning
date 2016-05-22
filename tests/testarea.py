actions = [-1,0,-0.5,-0.3]

indices = [i[0] for i in sorted(enumerate(actions), key=lambda x:x[1],reverse=True)]

print indices