def p(g):
    h,w=len(g),len(g[0])
    r=[[0]*w*3 for _ in range(h*3)]
    for i in range(h):
        for j in range(w):
            if g[i][j]:
                for di in range(h):
                    for dj in range(w):
                        r[i*h+di][j*w+dj]=g[di][dj]
    return r