def p(g):
    r=[[2 if c==1 else 0 for c in row] for row in g]
    # Find the row to use for position 7
    # Try to find a row that's different from row 0 and appears less frequently
    row_counts = {}
    for i, row in enumerate(r):
        key = tuple(row)
        if key not in row_counts:
            row_counts[key] = []
        row_counts[key].append(i)
    
    # Use row 1 by default, but if there's a unique pattern, use that
    row7_idx = 1
    for key, indices in row_counts.items():
        if len(indices) == 1 and indices[0] > 0:  # unique and not row 0
            row7_idx = indices[0]
            break
    
    r.extend([r[0][:],r[row7_idx][:],r[0][:]])
    return r