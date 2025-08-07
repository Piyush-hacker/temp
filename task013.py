def p(g):
    h,w=len(g),len(g[0])
    r=[[0]*w for _ in range(h)]
    
    # Find non-zero elements and their positions
    colors = []
    for i in range(h):
        for j in range(w):
            if g[i][j] != 0:
                colors.append((j, g[i][j]))
    
    colors.sort()  # Sort by column position
    
    if len(colors) >= 2:
        # Create pattern where each color appears at its original position + every 2 positions after
        for i in range(h):
            for j in range(w):
                for orig_pos, color in colors:
                    if j >= orig_pos and (j - orig_pos) % 2 == 0:
                        r[i][j] = color
    
    return r