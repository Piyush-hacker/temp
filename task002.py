def p(g):
    r=[r[:] for r in g]
    h,w=len(g),len(g[0])
    for i in range(1,h-1):
        for j in range(1,w-1):
            if g[i][j]==0 and g[i-1][j]==3 and g[i+1][j]==3 and g[i][j-1]==3 and g[i][j+1]==3:
                r[i][j]=4
    return r