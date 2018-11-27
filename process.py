import numpy as np
import time

infile = 'example/example.txt'
outfile = infile.replace('.txt','.npy')

print('loading')
start = time.time()
with open(infile, 'r') as f:
    grid = np.array([[int(val) for val in line.split()] for line in f.readlines()], dtype=np.uint8)
end = time.time()
print('time elapsed', end-start)

def complete(grid):
    m,n = grid.shape
    grid = np.pad(grid, ((0, n), (0, 0)), mode='constant')

    for i in range(n):
        grid[:,i] = np.roll(grid[:,i], i)

    quarter = np.zeros([m, m], dtype=np.uint8)
    quarter[:m,:n] = grid[:m,:n]
    quarter = quarter + np.tril(quarter,k=-1).transpose()
    half = np.concatenate([np.fliplr(quarter), quarter[:,1:]],axis=1)
    whole = np.concatenate([np.flipud(half), half[1:,:]])

    return whole

print('processing')
start = time.time()
grid = complete(grid)
end = time.time()
print('time elapsed', end-start)

print('saving')
start = time.time()
np.save(outfile, grid)
end = time.time()
print('time elapsed', end-start)

